"""
QUBO problem formulation and Hamiltonian construction.

The problem is formulated as a QUBO model. We seek the bitstring x that minimizes 
the Hamiltonian H:

H(x) = Σ_{i=1}^{N} (αR_i + βD_i)x_i + P (Σ_{i=1}^{N} x_i - 1)^2

where:
- x_i ∈ {0,1}: Binary variable (1 if cover i is chosen, 0 otherwise)
- R_i, D_i: Normalized coefficients for Risk and Distance
- P: Penalty coefficient enforcing the constraint Σx_i = 1
"""

import numpy as np
from typing import Tuple, Optional
from qiskit.quantum_info import SparsePauliOp


class QUBOProblem:
    """Represents a QUBO problem for tactical position selection."""
    
    def __init__(
        self,
        risk_costs: np.ndarray,
        distance_costs: np.ndarray,
        alpha: float = 1.0,
        beta: float = 1.0,
        penalty: float = 10.0
    ):
        """
        Initialize QUBO problem.
        
        Args:
            risk_costs: Array of risk costs R_i for each position
            distance_costs: Array of distance costs D_i for each position
            alpha: Weight for risk term
            beta: Weight for distance term
            penalty: Penalty coefficient P for constraint enforcement
        """
        self.N = len(risk_costs)
        if len(distance_costs) != self.N:
            raise ValueError("Risk and distance costs must have same length")
        
        # Normalize costs
        self.R = self._normalize(risk_costs)
        self.D = self._normalize(distance_costs)
        self.alpha = alpha
        self.beta = beta
        self.penalty = penalty
        
        # Build QUBO matrix
        self.Q = self._build_qubo_matrix()
        
    def _normalize(self, arr: np.ndarray) -> np.ndarray:
        """Normalize array to [0, 1] range."""
        arr = np.array(arr)
        if arr.max() == arr.min():
            return np.ones_like(arr) / len(arr)
        return (arr - arr.min()) / (arr.max() - arr.min())
    
    def _build_qubo_matrix(self) -> np.ndarray:
        """
        Build QUBO matrix Q such that x^T Q x = H(x).
        
        The Hamiltonian is:
        H(x) = Σ_i (αR_i + βD_i)x_i + P(Σ_i x_i - 1)^2
        
        Expanding the constraint term:
        P(Σ_i x_i - 1)^2 = P(Σ_i x_i^2 + 2Σ_{i<j} x_i x_j - 2Σ_i x_i + 1)
        
        Since x_i^2 = x_i for binary variables:
        = P(Σ_i x_i + 2Σ_{i<j} x_i x_j - 2Σ_i x_i + 1)
        = P(2Σ_{i<j} x_i x_j - Σ_i x_i + 1)
        
        So the QUBO matrix has:
        - Diagonal: (αR_i + βD_i) - P
        - Off-diagonal: 2P
        """
        Q = np.zeros((self.N, self.N))
        
        # Diagonal terms: linear costs minus penalty
        for i in range(self.N):
            Q[i, i] = self.alpha * self.R[i] + self.beta * self.D[i] - self.penalty
        
        # Off-diagonal terms: penalty for constraint
        for i in range(self.N):
            for j in range(i + 1, self.N):
                Q[i, j] = 2 * self.penalty
                Q[j, i] = 2 * self.penalty
        
        return Q
    
    def evaluate(self, x: np.ndarray) -> float:
        """
        Evaluate Hamiltonian for given bitstring.
        
        Args:
            x: Binary array of length N
            
        Returns:
            Hamiltonian value H(x)
        """
        x = np.array(x)
        if len(x) != self.N:
            raise ValueError(f"Bitstring length {len(x)} != problem size {self.N}")
        
        # Linear terms
        linear = np.sum((self.alpha * self.R + self.beta * self.D) * x)
        
        # Constraint penalty
        constraint = self.penalty * (np.sum(x) - 1) ** 2
        
        return linear + constraint
    
    def get_optimal_solution(self) -> Tuple[np.ndarray, float]:
        """
        Find optimal solution by brute force (for small problems).
        
        Returns:
            Tuple of (optimal_bitstring, optimal_energy)
        """
        best_x = None
        best_energy = float('inf')
        
        for i in range(2 ** self.N):
            x = np.array([int(b) for b in format(i, f'0{self.N}b')])
            energy = self.evaluate(x)
            if energy < best_energy:
                best_energy = energy
                best_x = x
        
        return best_x, best_energy


def build_hamiltonian(qubo_problem: QUBOProblem) -> SparsePauliOp:
    """
    Convert QUBO problem to Ising Hamiltonian for quantum algorithms.
    
    QUBO: x^T Q x where x_i ∈ {0,1}
    Ising: Σ_i h_i Z_i + Σ_{i<j} J_{ij} Z_i Z_j where Z_i ∈ {-1,+1}
    
    Conversion: x_i = (1 - Z_i) / 2
    
    Args:
        qubo_problem: QUBOProblem instance
        
    Returns:
        SparsePauliOp representing the Ising Hamiltonian
    """
    N = qubo_problem.N
    Q = qubo_problem.Q
    
    # Convert QUBO to Ising
    # x_i = (1 - Z_i) / 2
    # After substitution and simplification:
    h = np.zeros(N)
    J = np.zeros((N, N))
    
    for i in range(N):
        # Linear terms
        h[i] = Q[i, i] / 2
        for j in range(N):
            if j != i:
                h[i] += Q[i, j] / 4
    
    for i in range(N):
        for j in range(i + 1, N):
            J[i, j] = Q[i, j] / 4
    
    # Build Pauli operators
    pauli_list = []
    
    # Single Z terms
    for i in range(N):
        if abs(h[i]) > 1e-10:
            pauli_str = 'I' * i + 'Z' + 'I' * (N - i - 1)
            pauli_list.append((pauli_str, h[i]))
    
    # Two-body Z terms
    for i in range(N):
        for j in range(i + 1, N):
            if abs(J[i, j]) > 1e-10:
                pauli_str = ['I'] * N
                pauli_str[i] = 'Z'
                pauli_str[j] = 'Z'
                pauli_str = ''.join(pauli_str)
                pauli_list.append((pauli_str, J[i, j]))
    
    # Constant term (can be ignored for optimization)
    constant = np.sum(Q) / 4 + np.sum(np.diag(Q)) / 4
    
    if len(pauli_list) == 0:
        # Return identity with constant
        return SparsePauliOp(['I' * N], [constant])
    
    return SparsePauliOp.from_list(pauli_list)

