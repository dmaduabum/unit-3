# Unit 3 – High-Performance Simulation Study  
**Author:** Dili K. Maduabum  
**Course:** Advanced Statistical Computing  
**Last Updated:** November 2025  

---

## Project Overview

This project revisits my Unit 2 simulation study of the Benjamini–Hochberg (1995) False Discovery Rate (FDR) procedure.  

In Unit 3, the goal was to improve **computational performance**, **numerical reliability**, and **scalability** using methods studied in class:

- Code profiling  
- Algorithmic improvements  
- Array programming / vectorization  
- Parallelization  
- Complexity analysis  

The optimized version was then compared to the baseline using both runtime benchmarks and speedup analysis.

---

## 📁 Project Structure
```
unit-3/
│
├── baseline/                    # Original (Unit 2) simulation code
│   ├── simulation.py
│   ├── dgps.py
│   ├── methods.py
│   ├── metrics.py
│   ├── results/                 # simulation graphs
│   ├── visualize.py
│   ├── profile_sim.py
│   └── complexity_timing.py
│
├── optimized/                   # Optimized code
│   ├── simulation_opt.py        # Vectorized simulation
│   └── parallel_simulation.py   # Joblib parallel version
│
├── src/                         # Analysis & plotting scripts
│   ├── benchmark_runtime.py
│   ├── parallel_speedup.py
│   ├── complexity_compare.py
│   ├── runtime_barplot.py
│   └── visualize.py             # Additional plots
│
├── tests/                       # Regression tests
│   └── test_regression.py
│
├── results/
│   ├── raw/                     # CSV outputs
│   └── figures/                 # All plots
│
├── docs/
│   ├── BASELINE.md              # Baseline profiling + complexity results
│   └── OPTIMIZATION.md          # Optimization details + comparison plots
│
├── Makefile                     # Full automation suite
└── requirements.txt
```

---

## Key Improvements

### **1. Array Programming (Vectorization)**
Replaced all major Python loops with NumPy vectorized operations.  
Result: **2.7× speedup** (6.06 sec → 1.64 sec).

### **2. Parallelization (Joblib)**
Implemented parallel simulation replicates using  
`joblib.Parallel(n_jobs=k)`.

Although joblib overhead dominated (simulation became very fast), I demonstrated:
- correct parallel behavior
- valid speedup analysis across 1, 2, 4, 8 cores

### **3. Profiling**
Used `cProfile` to identify bottlenecks.  

Baseline bottlenecks:
- Python loops  
- Pandas DataFrame construction  
- Import overhead  

Optimized version removes these issues.

### **4. Complexity Analysis**
Measured scaling behavior vs number of hypotheses (m).  

Generated:
- baseline complexity  
- optimized complexity  
- comparison plot  

### **5. Regression Testing**
Wrote tests to verify:
- baseline vs optimized FDR & TPR are close  
- p-value distributions match within tolerance  
- no numerical instability  

All tests pass.

---

## Key Results

### **Runtime Comparison**
![Runtime Comparison](results/figures/runtime_comparison.png)

### **Complexity (Baseline vs Optimized)**
![Complexity Comparison](results/figures/complexity_comparison.png)

### **Parallel Speedup**
![Speedup Plot](results/figures/parallel_speedup.png)

---

## Using the Makefile

The Makefile provides automated targets:
```bash
make baseline          # Run baseline simulation
make optimized         # Run optimized simulation
make profile           # Run cProfile
make complexity        # Baseline complexity analysis
make benchmark         # Baseline vs optimized runtime
make speedup           # Parallel speedup study
make compare           # Complexity comparison plot
make figures           # All figures (Unit 2 + Unit 3)
make stability-check   # Regression tests
make clean             # Remove output files
```

---
