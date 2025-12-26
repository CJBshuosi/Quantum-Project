"""
Tactical Position Selection Problem definition.

Given a set of N available cover points, each with associated risk costs 
and travel distances, select exactly one optimal position.
"""

import numpy as np
from typing import Tuple, Optional
from .qubo import QUBOProblem


class TacticalPositionProblem:
    """Represents the tactical position selection problem."""
    
    def __init__(
        self,
        N: int,
        risk_costs: Optional[np.ndarray] = None,
        distance_costs: Optional[np.ndarray] = None,
        alpha: float = 1.0,
        beta: float = 1.0,
        seed: Optional[int] = None
    ):
        """
        Initialize tactical position problem.
        
        Args:
            N: Number of available cover points
            risk_costs: Risk costs for each position (if None, generated randomly)
            distance_costs: Distance costs for each position (if None, generated randomly)
            alpha: Weight for risk term
            beta: Weight for distance term
            seed: Random seed for reproducibility
        """
        self.N = N
        self.rng = np.random.default_rng(seed)
        
        if risk_costs is None:
            risk_costs = self.rng.uniform(0.1, 1.0, N)
        if distance_costs is None:
            distance_costs = self.rng.uniform(0.1, 1.0, N)
        
        self.risk_costs = np.array(risk_costs)
        self.distance_costs = np.array(distance_costs)
        self.alpha = alpha
        self.beta = beta
        
        # Create QUBO problem
        self.qubo = QUBOProblem(
            risk_costs=self.risk_costs,
            distance_costs=self.distance_costs,
            alpha=alpha,
            beta=beta
        )
    
    def get_qubo(self) -> QUBOProblem:
        """Get the QUBO problem instance."""
        return self.qubo
    
    def get_optimal_solution(self) -> Tuple[np.ndarray, float]:
        """Get optimal solution (for small problems)."""
        return self.qubo.get_optimal_solution()

