# ======================================================
# Makefile
# Author: Dili K. Maduabum
# Last edit: November 2025
# ======================================================

SHELL := /bin/bash

# ------------------------------------------------------
# 0. Convenience Targets
# ------------------------------------------------------

all: baseline optimized figures benchmark speedup compare stability-check
	@echo "Completed full Unit 3 workflow."

help:
	@echo "Unit 3 Makefile targets:"
	@echo "  make baseline         - Run baseline simulation"
	@echo "  make profile          - Profile baseline version"
	@echo "  make complexity       - Baseline complexity analysis"
	@echo "  make optimized        - Run optimized simulation"
	@echo "  make parallel         - Run optimized parallel simulation"
	@echo "  make figures          - Generate all final plots"
	@echo "  make benchmark        - Baseline vs optimized runtime"
	@echo "  make speedup          - Parallel speedup experiment"
	@echo "  make compare          - Baseline vs optimized complexity plot"
	@echo "  make stability-check  - Run regression tests"
	@echo "  make clean            - Remove outputs"

# ------------------------------------------------------
# 1. Baseline Targets
# ------------------------------------------------------

baseline:
	python baseline/simulation.py

profile:
	python baseline/profile_sim.py

complexity:
	python baseline/complexity_timing.py

# ------------------------------------------------------
# 2. Optimized Targets
# ------------------------------------------------------

optimized:
	python optimized/simulation_opt.py

parallel:
	python optimized/parallel_simulation.py --cores 4 --nsim 1000

# ------------------------------------------------------
# 3. Comparison + Benchmark Plots
# ------------------------------------------------------

benchmark:
	PYTHONPATH=. python src/benchmark_runtime.py

speedup:
	PYTHONPATH=. python src/parallel_speedup.py

compare:
	PYTHONPATH=. python src/complexity_compare.py

runtime-plot:
	PYTHONPATH=. python src/runtime_barplot.py

# ------------------------------------------------------
# 4. Figures (Unit 2 + Unit 3 Visualizations)
# ------------------------------------------------------

figures: runtime-plot compare speedup
	PYTHONPATH=. python baseline/visualize.py

# ------------------------------------------------------
# 5. Stability / Regression Testing
# ------------------------------------------------------

stability-check:
	PYTHONPATH=. python tests/test_regression.py

tests:
	PYTHONPATH=. pytest tests/ -v

# ------------------------------------------------------
# 6. Clean outputs
# ------------------------------------------------------

clean:
	rm -rf results/raw/*.csv results/figures/*.png results/figures/*.pdf

