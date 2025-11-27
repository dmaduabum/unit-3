# ======================================================
# Unit 3 – High Performance Simulation Study Makefile
# Author: Dili K. Maduabum
# Last edit: November 2025
# ======================================================

profile:
	python baseline/profile_sim.py

complexity:
	python baseline/complexity_timing.py

benchmark:
	python benchmark_runtime.py

parallel:
	python parallel_speedup.py

stability-check:
	PYTHONPATH=. python tests/test_regression.py

