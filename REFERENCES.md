# 参考资料 (References)

本文档列出了在开发 Quantum-Aegis 项目时参考的主要资料和资源。

## 1. Qiskit 官方文档

### 核心文档
- **Qiskit Documentation**: https://docs.quantum.ibm.com/
- **Qiskit Algorithms**: https://docs.quantum.ibm.com/api/qiskit-algorithms
- **Qiskit Aer (Simulator)**: https://docs.quantum.ibm.com/api/qiskit-aer
- **Qiskit Primitives**: https://docs.quantum.ibm.com/api/qiskit/primitives

### 算法实现参考
- **VQE (Variational Quantum Eigensolver)**: 
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.minimum_eigensolvers.VQE
  - https://qiskit.org/ecosystem/algorithms/tutorials/01_algorithms_introduction.html

- **QAOA (Quantum Approximate Optimization Algorithm)**:
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.minimum_eigensolvers.QAOA
  - https://qiskit.org/ecosystem/algorithms/tutorials/04_qaoa.html

### 噪声模型
- **Qiskit Aer Noise Models**: 
  - https://docs.quantum.ibm.com/api/qiskit-aer/qiskit_aer.noise
  - https://qiskit.org/ecosystem/aer/tutorials/3_building_noise_models.html

### 优化器
- **Qiskit Algorithms Optimizers**:
  - https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers
  - SPSA: https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers.SPSA
  - COBYLA: https://docs.quantum.ibm.com/api/qiskit-algorithms/qiskit_algorithms.optimizers.COBYLA

## 2. 学术论文和理论基础

### VQE 算法
- Peruzzo, A., et al. (2014). "A variational eigenvalue solver on a photonic quantum processor." Nature Communications, 5(1), 4213.
- McClean, J. R., et al. (2016). "The theory of variational hybrid quantum-classical algorithms." New Journal of Physics, 18(2), 023023.

### QAOA 算法
- Farhi, E., et al. (2014). "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028
- Farhi, E., & Harrow, A. W. (2016). "Quantum Supremacy through the Quantum Approximate Optimization Algorithm." arXiv:1602.07674

### QUBO 问题
- Kochenberger, G., et al. (2014). "The unconstrained binary quadratic programming problem: a survey." Journal of Combinatorial Optimization, 28(1), 58-81.

## 3. Qiskit 教程和示例

### 官方教程
- **Qiskit Textbook**: https://qiskit.org/learn/
- **Qiskit Tutorials**: https://github.com/Qiskit/qiskit-tutorials
- **Variational Algorithms Tutorial**: https://qiskit.org/ecosystem/algorithms/tutorials/01_algorithms_introduction.html

### 代码示例
- VQE 示例: https://qiskit-community.github.io/qiskit-algorithms/tutorials/02_vqe_advanced_options.html
- QAOA 示例: https://qiskit-community.github.io/qiskit-algorithms/tutorials/05_qaoa.html
- 噪声模拟示例: https://qiskit.github.io/qiskit-aer/tutorials/1_aersimulator.html

## 4. Python 项目结构最佳实践

### 项目组织
- **Python Project Structure**: https://docs.python-guide.org/writing/structure/
- **Google Python Style Guide**: https://google.github.io/styleguide/pyguide.html
- **PEP 8 -- Style Guide for Python Code**: https://peps.python.org/pep-0008/

### 大厂项目结构参考
- **Apple's Python Style Guide**: 参考了模块化、清晰的目录结构
- **Google's Python Style Guide**: 参考了代码组织和命名规范

## 5. 量子计算基础理论

### 教材和课程
- Nielsen, M. A., & Chuang, I. L. (2010). "Quantum Computation and Quantum Information." Cambridge University Press.
- 课程教材: "Quantum Computation and Error Correction" (Course Code: 76636-01)

### 在线资源
- **IBM Quantum Learning**: https://learning.quantum.ibm.com/
- **Qiskit Global Summer School**: https://qiskit.org/events/summer-school/

## 6. 具体实现参考

### QUBO 到 Ising 转换
- 参考了 Qiskit Optimization 模块的实现
- https://docs.quantum.ibm.com/api/qiskit-optimization/

### Hamiltonian 构建
- 参考了 Qiskit 中 SparsePauliOp 的使用
- https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.SparsePauliOp

### 电路分解和编译
- Qiskit Circuit Library: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library
- Transpilation: https://docs.quantum.ibm.com/api/qiskit/qiskit.compiler

## 7. 版本兼容性参考

### Qiskit 版本迁移
- **Qiskit Migration Guides**: https://docs.quantum.ibm.com/migration-guides/
- **Qiskit 1.0 Migration**: https://docs.quantum.ibm.com/migration-guides/qiskit-1.0-migration-guide
- **Primitives Migration**: https://docs.quantum.ibm.com/migration-guides/qiskit-primitives

## 8. 可视化参考

### Matplotlib
- **Matplotlib Documentation**: https://matplotlib.org/stable/contents.html
- **Matplotlib Tutorials**: https://matplotlib.org/stable/tutorials/index.html

## 9. 项目计划书

- 课程项目计划书: "Quantum-Aegis: A Comparative Study of Quantum Variational Algorithms for Tactical Optimization in Gaming"
- 包含问题定义、Hamiltonian 公式、实验设计等核心内容

## 10. 代码实现细节

### 关键实现点
1. **QUBO 问题定义**: 参考了组合优化问题的标准 QUBO 形式
2. **约束处理**: 使用惩罚项方法 (Penalty Method) 处理约束条件
3. **噪声模拟**: 使用 Qiskit Aer 的噪声模型模拟 NISQ 设备
4. **优化器选择**: 参考了 Qiskit 文档中关于 SPSA 和 COBYLA 的对比


