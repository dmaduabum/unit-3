"""
parallel_speedup.py
----------------------------------------------
Measure parallel speedup for the optimized BH (1995)
simulation using joblib-based parallelization.

This script runs the optimized joblib-parallel simulation
(`optimized/parallel_simulation.py`) with different numbers
of CPU cores (e.g., 1, 2, 4, 8) and records runtimes.

Outputs:
- CSV: results/raw/parallel_speedup.csv
- Plot: results/figures/parallel_speedup.png
    (Speedup = T(1 core) / T(k cores))

Author: Dili K. Maduabum
Last edit: November 2025
"""

import time
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt


# CPU core counts to test
CORES = [1, 2, 4, 8]


def run_parallel(n_cores, nsim=500):
    """
    Run the optimized parallel simulation using a specific number of cores.

    Parameters
    ----------
    n_cores : int
        Number of CPU cores for joblib.Parallel.
    nsim : int
        Number of replicates per condition in the simulation.

    Returns
    -------
    float
        Wall-clock runtime in seconds.
    """
    cmd = f"python optimized/parallel_simulation.py --cores {n_cores} --nsim {nsim}"
    start = time.time()
    subprocess.run(cmd, shell=True)
    end = time.time()
    return end - start


def main():
    """
    Run the parallel speedup experiment across multiple core counts.
    Save raw results and produce the parallel speedup plot.
    """
    times = []

    print("Running parallel speedup benchmark...\n")

    for c in CORES:
        print(f"Running with {c} cores...")
        t = run_parallel(c)
        times.append(t)
        print(f"Time with {c} cores: {t:.3f} sec\n")

    # Compute speedup S(k) = T(1) / T(k)
    speedup = np.array(times[0]) / np.array(times)

    # Ensure result folders exist
    os.makedirs("results/raw", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    # Save raw results
    np.savetxt(
        "results/raw/parallel_speedup.csv",
        np.column_stack([CORES, times, speedup]),
        delimiter=",",
        header="cores,time,speedup",
        comments=""
    )

    # Plot speedup curve
    plt.figure(figsize=(8, 5))
    plt.plot(CORES, speedup, marker='o')
    plt.xlabel("CPU Cores")
    plt.ylabel("Speedup (T1 / Tk)")
    plt.title("Joblib Parallel Speedup (Optimized Simulation)")
    plt.grid(True)

    plt.savefig("results/figures/parallel_speedup.png", dpi=150)
    plt.close()

    print("Saved speedup figure to results/figures/parallel_speedup.png")


if __name__ == "__main__":
    main()
