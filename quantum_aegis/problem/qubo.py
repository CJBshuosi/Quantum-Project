"""
QUBO problem formulation and Hamiltonian construction.
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
        if isinstance(risk_costs, float):
            risk_costs = np.array([risk_costs])
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
        """Build QUBO matrix."""
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
    N = qubo_problem.N
    Q = qubo_problem.Q
    
    # Convert QUBO to Ising
    # x_i = (1 - Z_i) / 2
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
        return SparsePauliOp(['I' * N], [constant])
    
    return SparsePauliOp.from_list(pauli_list)

