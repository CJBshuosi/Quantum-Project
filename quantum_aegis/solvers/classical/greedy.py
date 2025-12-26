"""
Greedy Heuristic solver (approximate solution).

Selects the position with minimum combined cost (risk + distance).
"""

import numpy as np
import time
from typing import Dict, Any
from ...problem.qubo import QUBOProblem


class GreedySolver:
    """Greedy heuristic solver for QUBO problems (approximate solution)."""
    
    def solve(self, qubo_problem: QUBOProblem) -> Dict[str, Any]:
        """
        Solve QUBO problem using greedy heuristic.
        
        Args:
            qubo_problem: QUBO problem to solve
            
        Returns:
            Dictionary with solution information
        """
        start_time = time.time()
        
        # Greedy: select position with minimum combined cost
        costs = qubo_problem.alpha * qubo_problem.R + qubo_problem.beta * qubo_problem.D
        best_idx = np.argmin(costs)
        
        x = np.zeros(qubo_problem.N, dtype=int)
        x[best_idx] = 1
        
        energy = qubo_problem.evaluate(x)
        
        elapsed_time = time.time() - start_time
        
        return {
            'bitstring': x,
            'energy': energy,
            'elapsed_time': elapsed_time,
            'method': 'greedy'
        }

