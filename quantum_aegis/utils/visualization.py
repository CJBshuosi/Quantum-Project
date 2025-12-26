"""
Visualization utilities for experimental results.

Includes functions for convergence plots, scaling graphs, and noise analysis.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any, Optional


def plot_convergence(
    vqe_history: List[Dict[str, Any]],
    qaoa_history: List[Dict[str, Any]],
    optimal_energy: Optional[float] = None,
    save_path: Optional[str] = None
):
    """
    Plot convergence curves: Energy vs. Iteration count for VQE and QAOA.
    
    Args:
        vqe_history: VQE optimization history
        qaoa_history: QAOA optimization history
        optimal_energy: Optimal energy (for reference line)
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 6))
    
    if vqe_history:
        vqe_iterations = [h['iteration'] for h in vqe_history]
        vqe_energies = [h['energy'] for h in vqe_history]
        plt.plot(vqe_iterations, vqe_energies, 'b-o', label='VQE', markersize=4, linewidth=2)
    
    if qaoa_history:
        qaoa_iterations = [h['iteration'] for h in qaoa_history]
        qaoa_energies = [h['energy'] for h in qaoa_history]
        plt.plot(qaoa_iterations, qaoa_energies, 'r-s', label='QAOA', markersize=4, linewidth=2)
    
    if optimal_energy is not None:
        plt.axhline(y=optimal_energy, color='g', linestyle='--', label='Optimal Energy', linewidth=2)
    
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Energy', fontsize=12)
    plt.title('Convergence: Energy vs. Iteration Count', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_scaling(
    problem_sizes: List[int],
    quantum_times: Dict[str, List[float]],
    classical_times: Dict[str, List[float]],
    save_path: Optional[str] = None
):
    """
    Plot scaling graphs: Computation time vs. Problem Size (N).
    
    Args:
        problem_sizes: List of problem sizes N
        quantum_times: Dictionary with 'VQE' and 'QAOA' as keys, lists of times as values
        classical_times: Dictionary with 'brute_force' and 'greedy' as keys, lists of times as values
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 6))
    
    # Plot quantum methods
    if 'VQE' in quantum_times:
        plt.plot(problem_sizes, quantum_times['VQE'], 'b-o', label='VQE', markersize=8, linewidth=2)
    if 'QAOA' in quantum_times:
        plt.plot(problem_sizes, quantum_times['QAOA'], 'r-s', label='QAOA', markersize=8, linewidth=2)
    
    # Plot classical methods
    if 'brute_force' in classical_times:
        plt.plot(problem_sizes, classical_times['brute_force'], 'g-^', label='Brute Force', markersize=8, linewidth=2)
    if 'greedy' in classical_times:
        plt.plot(problem_sizes, classical_times['greedy'], 'm-d', label='Greedy', markersize=8, linewidth=2)
    
    plt.xlabel('Problem Size (N)', fontsize=12)
    plt.ylabel('Computation Time (seconds)', fontsize=12)
    plt.title('Scaling Analysis: Computation Time vs. Problem Size', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Log scale for better visualization
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_noise_analysis(
    error_rates: List[float],
    success_rates: Dict[str, List[float]],
    save_path: Optional[str] = None
):
    """
    Plot noise analysis: Success probability rates under varying error rates.
    
    Args:
        error_rates: List of error rates (gate/readout error probabilities)
        success_rates: Dictionary with method names as keys, lists of success rates as values
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 6))
    
    for method, rates in success_rates.items():
        plt.plot(error_rates, rates, 'o-', label=method, markersize=8, linewidth=2)
    
    plt.xlabel('Error Rate', fontsize=12)
    plt.ylabel('Success Probability', fontsize=12)
    plt.title('Noise Analysis: Success Probability vs. Error Rate', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1.1])
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

