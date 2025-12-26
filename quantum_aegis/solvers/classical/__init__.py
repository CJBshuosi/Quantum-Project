"""Classical solvers for QUBO problems."""

from .brute_force import BruteForceSolver
from .greedy import GreedySolver

__all__ = ["BruteForceSolver", "GreedySolver"]

