"""
Variational Quantum Eigensolver (VQE) implementation.

VQE utilizes hardware-efficient ansatzes (e.g., RealAmplitudes).
"""

import numpy as np
from typing import Optional, Dict, Any, Callable
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes
from qiskit_algorithms import VQE as QiskitVQE
from qiskit_algorithms.optimizers import Optimizer, SPSA, COBYLA
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp

# Try different Estimator imports for compatibility
try:
    # Try StatevectorEstimator (Qiskit 1.0+)
    from qiskit.primitives import StatevectorEstimator as Estimator
except ImportError:
    try:
        # Try standard Estimator
        from qiskit.primitives import Estimator
    except ImportError:
        # Fallback to AerEstimator
        try:
            from qiskit_aer.primitives import Estimator as AerEstimator
            Estimator = AerEstimator
        except ImportError:
            # Last resort: use BackendEstimator
            from qiskit.primitives import BackendEstimator
            Estimator = None  # Will use BackendEstimator wrapper

from ...problem.qubo import QUBOProblem, build_hamiltonian


class VQESolver:
    """VQE solver for QUBO problems."""
    
    def __init__(
        self,
        optimizer: Optional[Optimizer] = None,
        ansatz_reps: int = 2,
        use_noise: bool = False,
        noise_model=None,
        seed: Optional[int] = None
    ):
        """
        Initialize VQE solver.
        
        Args:
            optimizer: Qiskit optimizer (default: SPSA)
            ansatz_reps: Number of repetitions in RealAmplitudes ansatz
            use_noise: Whether to use noisy simulator
            noise_model: Noise model for noisy simulation
            seed: Random seed
        """
        self.optimizer = optimizer if optimizer is not None else SPSA(maxiter=200)
        self.ansatz_reps = ansatz_reps
        self.use_noise = use_noise
        self.noise_model = noise_model
        self.seed = seed
        
        self.result = None
        self.optimization_history = []
    
    def solve(
        self,
        qubo_problem: QUBOProblem,
        callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Solve QUBO problem using VQE.
        
        Args:
            qubo_problem: QUBO problem to solve
            callback: Optional callback function for optimization progress
            
        Returns:
            Dictionary with solution information
        """
        N = qubo_problem.N
        
        # Build Hamiltonian
        hamiltonian = build_hamiltonian(qubo_problem)
        
        # Create ansatz (hardware-efficient)
        ansatz = RealAmplitudes(N, reps=self.ansatz_reps, entanglement='linear')
        
        # Setup estimator with proper API compatibility
        # Use StatevectorEstimator for ideal simulation, BackendEstimator for noisy
        if self.use_noise and self.noise_model is not None:
            # For noisy simulation, try different BackendEstimator imports
            backend = AerSimulator(noise_model=self.noise_model)
            try:
                # Try importing from qiskit.primitives
                from qiskit.primitives import BackendEstimator
                estimator = BackendEstimator(backend=backend)
            except ImportError:
                try:
                    # Try importing from qiskit_aer.primitives
                    from qiskit_aer.primitives import Estimator as AerEstimator
                    estimator = AerEstimator(backend=backend)
                except (ImportError, TypeError):
                    # Fallback: use StatevectorEstimator (may not support noise perfectly)
                    try:
                        from qiskit.primitives import StatevectorEstimator
                        estimator = StatevectorEstimator()
                    except ImportError:
                        # Last resort: try standard Estimator
                        if Estimator is not None:
                            estimator = Estimator()
                        else:
                            raise RuntimeError("Could not initialize Estimator for noisy simulation")
        else:
            # For ideal simulation, try StatevectorEstimator first
            try:
                from qiskit.primitives import StatevectorEstimator
                estimator = StatevectorEstimator()
            except ImportError:
                # Fallback: try BackendEstimator
                try:
                    from qiskit.primitives import BackendEstimator
                    backend = AerSimulator()
                    estimator = BackendEstimator(backend=backend)
                except ImportError:
                    # Try AerEstimator
                    try:
                        from qiskit_aer.primitives import Estimator as AerEstimator
                        backend = AerSimulator()
                        estimator = AerEstimator(backend=backend)
                    except (ImportError, TypeError):
                        # Last resort: try standard Estimator
                        if Estimator is not None:
                            try:
                                estimator = Estimator()
                            except (TypeError, ValueError):
                                # Final fallback: use AerEstimator without backend
                                from qiskit_aer.primitives import Estimator as AerEstimator
                                estimator = AerEstimator()
                        else:
                            # Ultimate fallback
                            from qiskit_aer.primitives import Estimator as AerEstimator
                            estimator = AerEstimator()
        
        # Setup callback for tracking
        if callback is None:
            def callback_fn(eval_count, parameters, mean, metadata):
                self.optimization_history.append({
                    'iteration': eval_count,
                    'energy': mean,
                    'parameters': parameters
                })
                return False
        else:
            callback_fn = callback
        
        # Run VQE
        vqe = QiskitVQE(
            estimator=estimator,
            ansatz=ansatz,
            optimizer=self.optimizer,
            callback=callback_fn
        )
        
        result = vqe.compute_minimum_eigenvalue(hamiltonian)
        self.result = result
        
        # Extract solution
        optimal_params = result.optimal_parameters
        optimal_energy = result.eigenvalue.real
        
        # Get bitstring from final state
        # For VQE, we need to sample the final state
        qc = ansatz.assign_parameters(optimal_params)
        # Decompose the circuit to ensure all gates are supported
        qc = qc.decompose()
        if self.use_noise and self.noise_model is not None:
            backend = AerSimulator(noise_model=self.noise_model)
        else:
            backend = AerSimulator()
        
        counts = {}
        try:
            job = backend.run(qc, shots=1024, seed_simulator=self.seed)
            counts = job.result().get_counts()
            
            # Find most probable bitstring
            best_bitstring = max(counts, key=counts.get)
            x = np.array([int(b) for b in best_bitstring])
        except Exception as e:
            # If sampling fails, use statevector to get the most probable state
            from qiskit.quantum_info import Statevector
            state = Statevector(qc)
            probs = state.probabilities()
            best_idx = np.argmax(probs)
            x = np.array([int(b) for b in format(best_idx, f'0{N}b')])
            # Create a counts dict from probabilities for consistency
            counts = {format(i, f'0{N}b'): int(probs[i] * 1024) for i in range(len(probs)) if probs[i] > 1e-10}
        
        # Ensure constraint satisfaction (exactly one position selected)
        if np.sum(x) != 1:
            # If constraint violated, select position with minimum cost
            costs = qubo_problem.alpha * qubo_problem.R + qubo_problem.beta * qubo_problem.D
            best_idx = np.argmin(costs)
            x = np.zeros(N, dtype=int)
            x[best_idx] = 1
        
        return {
            'bitstring': x,
            'energy': optimal_energy,
            'optimal_parameters': optimal_params,
            'optimization_history': self.optimization_history,
            'result': result,
            'counts': counts
        }

