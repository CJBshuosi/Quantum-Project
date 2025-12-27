"""
Noise models for simulating NISQ device limitations.

Includes depolarizing errors and readout errors using Qiskit Aer.
"""

from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from typing import Optional


def create_depolarizing_noise_model(
    gate_error: float = 0.01,
    measurement_error: float = 0.01
) -> NoiseModel:
    """
    Create noise model with depolarizing errors.
    """
    noise_model = NoiseModel()
    
    # Add depolarizing error to single-qubit gates
    error_1q = depolarizing_error(gate_error, 1)
    noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'rz', 'sx', 'x', 'y', 'z', 'h', 'id'])
    
    # Add depolarizing error to two-qubit gates
    error_2q = depolarizing_error(gate_error, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz', 'swap'])
    
    # Add measurement error
    error_meas = ReadoutError([[1 - measurement_error, measurement_error],
                               [measurement_error, 1 - measurement_error]])
    noise_model.add_all_qubit_readout_error(error_meas)
    
    return noise_model


def create_readout_noise_model(
    readout_error: float = 0.01
) -> NoiseModel:
    noise_model = NoiseModel()
    
    # Add measurement error
    error_meas = ReadoutError([[1 - readout_error, readout_error],
                               [readout_error, 1 - readout_error]])
    noise_model.add_all_qubit_readout_error(error_meas)
    
    return noise_model


def create_combined_noise_model(
    gate_error: float = 0.01,
    readout_error: float = 0.01
) -> NoiseModel:

    noise_model = NoiseModel()
    
    # Add depolarizing error to single-qubit gates
    error_1q = depolarizing_error(gate_error, 1)
    noise_model.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3', 'rz', 'sx', 'x', 'y', 'z', 'h', 'id'])
    
    # Add depolarizing error to two-qubit gates
    error_2q = depolarizing_error(gate_error, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz', 'swap'])
    
    # Add measurement error
    error_meas = ReadoutError([[1 - readout_error, readout_error],
                               [readout_error, 1 - readout_error]])
    noise_model.add_all_qubit_readout_error(error_meas)
    
    return noise_model

