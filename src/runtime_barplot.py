"""
runtime_barplot.py
Create a bar plot of baseline vs optimized runtime.

Author: Dili K. Maduabum
Last edit: November 2025
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def main():
    # Manual values from benchmark_runtime.py
    baseline = 6.067
    optimized = 1.643

    names = ["Baseline", "Optimized"]
    values = [baseline, optimized]

    plt.figure(figsize=(7,5))
    plt.bar(names, values, color=["red","green"])
    plt.ylabel("Runtime (seconds)")
    plt.title("Baseline vs Optimized Runtime")

    os.makedirs("results/figures", exist_ok=True)
    plt.savefig("results/figures/runtime_comparison.png", dpi=150)
    plt.close()

    print("Saved bar plot to results/figures/runtime_comparison.png")

if __name__ == "__main__":
    main()

