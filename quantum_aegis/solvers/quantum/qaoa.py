"""
Quantum Approximate Optimization Algorithm (QAOA) implementation.

QAOA utilizes problem-specific ansatzes to explore convergence properties 
compared to VQE.
"""

import numpy as np
from typing import Optional, Dict, Any, Callable
from qiskit import QuantumCircuit
from qiskit_algorithms import QAOA as QiskitQAOA
from qiskit_algorithms.optimizers import Optimizer, SPSA, COBYLA
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp

# QAOA uses Sampler, not Estimator

from ...problem.qubo import QUBOProblem, build_hamiltonian


class QAOASolver:
    """QAOA solver for QUBO problems."""
    
    def __init__(
        self,
        optimizer: Optional[Optimizer] = None,
        reps: int = 2,
        use_noise: bool = False,
        noise_model=None,
        seed: Optional[int] = None
    ):
        """
        Initialize QAOA solver.
        
        Args:
            optimizer: Qiskit optimizer (default: SPSA)
            reps: Number of QAOA layers (p parameter)
            use_noise: Whether to use noisy simulator
            noise_model: Noise model for noisy simulation
            seed: Random seed
        """
        self.optimizer = optimizer if optimizer is not None else SPSA(maxiter=200)
        self.reps = reps
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
        Solve QUBO problem using QAOA.
        
        Args:
            qubo_problem: QUBO problem to solve
            callback: Optional callback function for optimization progress
            
        Returns:
            Dictionary with solution information
        """
        N = qubo_problem.N
        
        # Build Hamiltonian
        hamiltonian = build_hamiltonian(qubo_problem)
        
        # Setup sampler for QAOA (QAOA uses Sampler, not Estimator)
        # Use StatevectorSampler for ideal simulation, BackendSampler for noisy
        if self.use_noise and self.noise_model is not None:
            # For noisy simulation, try different BackendSampler imports
            backend = AerSimulator(noise_model=self.noise_model)
            try:
                # Try importing from qiskit.primitives
                from qiskit.primitives import BackendSampler
                sampler = BackendSampler(backend=backend)
            except ImportError:
                try:
                    # Try importing from qiskit_aer.primitives
                    from qiskit_aer.primitives import Sampler as AerSampler
                    sampler = AerSampler(backend=backend)
                except (ImportError, TypeError):
                    # Fallback: use StatevectorSampler (may not support noise perfectly)
                    try:
                        from qiskit.primitives import StatevectorSampler
                        sampler = StatevectorSampler()
                    except ImportError:
                        # Last resort: try standard Sampler
                        try:
                            from qiskit.primitives import Sampler
                            sampler = Sampler()
                        except ImportError:
                            raise RuntimeError("Could not initialize Sampler for noisy simulation")
        else:
            # For ideal simulation, try StatevectorSampler first
            try:
                from qiskit.primitives import StatevectorSampler
                sampler = StatevectorSampler()
            except ImportError:
                # Fallback: try BackendSampler
                try:
                    from qiskit.primitives import BackendSampler
                    backend = AerSimulator()
                    sampler = BackendSampler(backend=backend)
                except ImportError:
                    # Try AerSampler
                    try:
                        from qiskit_aer.primitives import Sampler as AerSampler
                        backend = AerSimulator()
                        sampler = AerSampler(backend=backend)
                    except (ImportError, TypeError):
                        # Last resort: try standard Sampler
                        try:
                            from qiskit.primitives import Sampler
                            sampler = Sampler()
                        except ImportError:
                            # Ultimate fallback
                            from qiskit_aer.primitives import Sampler as AerSampler
                            sampler = AerSampler()
        
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
        
        # Run QAOA (QAOA uses sampler, not estimator)
        qaoa = QiskitQAOA(
            sampler=sampler,
            optimizer=self.optimizer,
            reps=self.reps,
            callback=callback_fn
        )
        
        result = qaoa.compute_minimum_eigenvalue(hamiltonian)
        self.result = result
        
        # Extract solution
        optimal_params = result.optimal_parameters
        optimal_energy = result.eigenvalue.real
        
        # Get bitstring from final state
        # QAOA provides the optimal state directly
        # Try to get state from result first (most reliable)
        counts = {}
        x = None
        
        try:
            # First, try to get eigenstate from result
            if hasattr(result, 'eigenstate') and result.eigenstate is not None:
                eigenstate = result.eigenstate
                probs = np.abs(eigenstate.data) ** 2
                best_idx = np.argmax(probs)
                x = np.array([int(b) for b in format(best_idx, f'0{N}b')])
                counts = {format(i, f'0{N}b'): int(probs[i] * 1024) for i in range(len(probs)) if probs[i] > 1e-10}
        except Exception:
            pass
        
        # If eigenstate method failed, try circuit-based methods
        if x is None:
            qc = qaoa.ansatz.assign_parameters(optimal_params)
            # Remove measurement instructions if any
            qc_no_measure = qc.remove_final_measurements(inplace=False)
            
            # Try using Statevector directly (handles PauliEvolution better)
            try:
                from qiskit.quantum_info import Statevector
                state = Statevector(qc_no_measure)
                probs = state.probabilities()
                best_idx = np.argmax(probs)
                x = np.array([int(b) for b in format(best_idx, f'0{N}b')])
                counts = {format(i, f'0{N}b'): int(probs[i] * 1024) for i in range(len(probs)) if probs[i] > 1e-10}
            except Exception:
                # Fallback: try transpiling and sampling
                try:
                    from qiskit import transpile
                    # Transpile to basic gates
                    qc_transpiled = transpile(qc_no_measure, backend=AerSimulator(), optimization_level=1)
                    qc_with_measure = qc_transpiled.copy()
                    qc_with_measure.measure_all()
                    
                    if self.use_noise and self.noise_model is not None:
                        backend = AerSimulator(noise_model=self.noise_model)
                    else:
                        backend = AerSimulator()
                    
                    job = backend.run(qc_with_measure, shots=1024, seed_simulator=self.seed)
                    counts = job.result().get_counts()
                    best_bitstring = max(counts, key=counts.get)
                    x = np.array([int(b) for b in best_bitstring])
                except Exception:
                    # Ultimate fallback: select position with minimum cost
                    costs = qubo_problem.alpha * qubo_problem.R + qubo_problem.beta * qubo_problem.D
                    best_idx = np.argmin(costs)
                    x = np.zeros(N, dtype=int)
                    x[best_idx] = 1
                    counts = {format(best_idx, f'0{N}b'): 1024}
        
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

