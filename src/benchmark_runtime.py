"""
benchmark_runtime.py
---------------------------------
Benchmark baseline vs optimized simulation runtimes.

This script runs:
1. Baseline simulation (unit-3/baseline/simulation.py)
2. Optimized simulation (unit-3/optimized/simulation_opt.py)

It measures wall-clock runtime using time.time()
and writes results to results/raw/benchmark_results.txt

Author: Dili K. Maduabum
Last edit: November 2025
"""

import time
import subprocess
import os

def run_and_time(cmd):
    """
    Run a shell command and measure its wall-clock time.

    Parameters
    ----------
    cmd : str
        Shell command string (e.g., 'python baseline/simulation.py').

    Returns
    -------
    float
        Wall-clock runtime in seconds.
    """
    start = time.time()
    subprocess.run(cmd, shell=True)
    end = time.time()
    return end - start


def main():
    """Run baseline and optimized simulations and compare runtimes."""

    print("Running baseline simulation...")
    baseline_time = run_and_time("python baseline/simulation.py")

    print("Running optimized simulation...")
    optimized_time = run_and_time("python optimized/simulation_opt.py")

    print("\n=== Benchmark Results ===")
    print(f"Baseline runtime:  {baseline_time:.3f} sec")
    print(f"Optimized runtime: {optimized_time:.3f} sec")

    # Ensure results directory exists
    os.makedirs("results/raw", exist_ok=True)

    # Save results
    with open("results/raw/benchmark_results.txt", "w") as f:
        f.write(f"Baseline: {baseline_time}\n")
        f.write(f"Optimized: {optimized_time}\n")


if __name__ == "__main__":
    main()
