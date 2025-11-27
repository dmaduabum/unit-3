"""
complexity_compare.py
Generate a baseline vs optimized complexity comparison.

Author: Dili K. Maduabum
Last edit: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import time

def time_opt(m, reps=20):
    # Time optimized single replicate
    from optimized.simulation_opt import run_single_sim_opt
    start = time.time()
    for i in range(reps):
        run_single_sim_opt(m, pi0=0.8, effect_size=2.5, seed=100+i)
    end = time.time()
    return (end - start) / reps

def main():
    # Load baseline complexity results
    base = np.loadtxt("baseline/results/raw/complexity_results.csv", delimiter=",", skiprows=1)
    m_base = base[:,0]
    t_base = base[:,1]

    # Compute optimized complexity
    m_vals = np.array([50, 100, 200, 400, 800, 1600])
    t_opt = [time_opt(int(m)) for m in m_vals]

    # Plot baseline vs optimized
    plt.figure(figsize=(8,6))
    plt.loglog(m_base, t_base, marker='o', label="Baseline")
    plt.loglog(m_vals, t_opt, marker='o', label="Optimized")
    plt.xlabel("m (number of hypotheses)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Baseline vs Optimized Complexity")
    plt.grid(True, which="both", ls="--")
    plt.legend()

    os.makedirs("results/figures", exist_ok=True)
    plt.savefig("results/figures/complexity_comparison.png", dpi=150)
    plt.close()

    print("Saved complexity comparison to results/figures/complexity_comparison.png")

if __name__ == "__main__":
    main()

