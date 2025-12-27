# References

This document lists the main references and resources used in developing the Quantum-Aegis project.

## 1. Qiskit Official Documentation

### Core Documentation
- **Qiskit Documentation**: https://docs.quantum.ibm.com/
- **Qiskit Algorithms**: https://docs.quantum.ibm.com/api/qiskit-algorithms
- **Qiskit Aer (Simulator)**: https://docs.quantum.ibm.com/api/qiskit-aer
- **Qiskit Primitives**: https://docs.quantum.ibm.com/api/qiskit/primitives

### Algorithm Implementation References
- **VQE (Variational Quantum Eigensolver)**: 
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.minimum_eigensolvers.VQE
  - https://qiskit.org/ecosystem/algorithms/tutorials/01_algorithms_introduction.html

- **QAOA (Quantum Approximate Optimization Algorithm)**:
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.minimum_eigensolvers.QAOA
  - https://qiskit.org/ecosystem/algorithms/tutorials/04_qaoa.html

### Noise Models
- **Qiskit Aer Noise Models**: 
  - https://docs.quantum.ibm.com/api/qiskit-aer/qiskit_aer.noise
  - https://qiskit.org/ecosystem/aer/tutorials/3_building_noise_models.html

### Optimizers
- **Qiskit Algorithms Optimizers**:
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers
  - SPSA: https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers.SPSA
  - COBYLA: https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers.COBYLA

## 2. Academic Papers and Theoretical Foundations

### VQE Algorithm
- Peruzzo, A., et al. (2014). "A variational eigenvalue solver on a photonic quantum processor." Nature Communications, 5(1), 4213.
- McClean, J. R., et al. (2016). "The theory of variational hybrid quantum-classical algorithms." New Journal of Physics, 18(2), 023023.

### QAOA Algorithm
- Farhi, E., et al. (2014). "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028
- Farhi, E., & Harrow, A. W. (2016). "Quantum Supremacy through the Quantum Approximate Optimization Algorithm." arXiv:1602.07674

### QUBO Problems
- Kochenberger, G., et al. (2014). "The unconstrained binary quadratic programming problem: a survey." Journal of Combinatorial Optimization, 28(1), 58-81.

## 3. Qiskit Tutorials and Examples

### Official Tutorials
- **Qiskit Textbook**: https://qiskit.org/learn/
- **Qiskit Tutorials**: https://github.com/Qiskit/qiskit-tutorials
- **Variational Algorithms Tutorial**: https://qiskit.org/ecosystem/algorithms/tutorials/01_algorithms_introduction.html

### Code Examples
- VQE Example: https://qiskit-community.github.io/qiskit-algorithms/tutorials/02_vqe_advanced_options.html
- QAOA Example: https://qiskit-community.github.io/qiskit-algorithms/tutorials/05_qaoa.html
- Noise Simulation Example: https://qiskit.github.io/qiskit-aer/tutorials/1_aersimulator.html

## 4. Quantum Computing Fundamentals

### Textbooks and Course Materials
- Nielsen, M. A., & Chuang, I. L. (2010). "Quantum Computation and Quantum Information." Cambridge University Press.
- Course Textbook: "Quantum Computation and Error Correction" (Course Code: 76636-01)

### Online Resources
- **IBM Quantum Learning**: https://learning.quantum.ibm.com/
- **Qiskit Global Summer School**: https://qiskit.org/events/summer-school/

## 5. Implementation-Specific References

### QUBO to Ising Conversion
- Referenced implementation from Qiskit Optimization module
- https://docs.quantum.ibm.com/api/qiskit-optimization/

### Hamiltonian Construction
- Referenced usage of SparsePauliOp in Qiskit
- https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.SparsePauliOp

### Circuit Decomposition and Compilation
- Qiskit Circuit Library: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library
- Transpilation: https://docs.quantum.ibm.com/api/qiskit/qiskit.compiler

## 6. Version Compatibility References

### Qiskit Version Migration
- **Qiskit Migration Guides**: https://docs.quantum.ibm.com/migration-guides/
- **Qiskit 1.0 Migration**: https://docs.quantum.ibm.com/migration-guides/qiskit-1.0-migration-guide
- **Primitives Migration**: https://docs.quantum.ibm.com/migration-guides/qiskit-primitives


## 7. Code Implementation Details

### Key Implementation Points
1. **QUBO Problem Definition**: Referenced standard QUBO formulation for combinatorial optimization problems
2. **Constraint Handling**: Used penalty method to handle constraint conditions
3. **Noise Simulation**: Used Qiskit Aer noise models to simulate NISQ devices
4. **Optimizer Selection**: Referenced Qiskit documentation comparing SPSA and COBYLA


