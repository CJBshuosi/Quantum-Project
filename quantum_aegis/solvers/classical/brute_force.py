"""
Brute Force solver (exact solution).

Exhaustively searches all possible solutions to find the optimal one.
"""

import numpy as np
import time
from typing import Dict, Any
from ...problem.qubo import QUBOProblem


class BruteForceSolver:
    """Brute force solver for QUBO problems (exact solution)."""
    
    def solve(self, qubo_problem: QUBOProblem) -> Dict[str, Any]:
        """
        Solve QUBO problem using brute force.
        
        Args:
            qubo_problem: QUBO problem to solve
            
        Returns:
            Dictionary with solution information
        """
        start_time = time.time()
        
        best_x, best_energy = qubo_problem.get_optimal_solution()
        
        elapsed_time = time.time() - start_time
        
        return {
            'bitstring': best_x,
            'energy': best_energy,
            'elapsed_time': elapsed_time,
            'method': 'brute_force'
        }

