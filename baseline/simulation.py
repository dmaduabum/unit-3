"""
simulation.py
-----------------
Main simulation orchestration script for the Benjamini & Hochberg (1995)
False Discovery Rate (FDR) reproduction study.

This script:
- Generates simulated p-values under different parameter settings
- Applies multiple-testing correction methods
- Computes FDR and Power for each method
- Saves raw results to CSV for later analysis and visualization

Author: Dili K. Maduabum
Last Edited: October 21, 2025
"""

import os
import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm

from dgps import generate_pvalues
from methods import bh_procedure, bonferroni_method, uncorrected_method
from metrics import compute_fdr, compute_power

# ------------------------
# Simulation configuration
# ------------------------

N_REPS = 1000       # Number of Monte Carlo replications
SEED = 42           # Base random seed for reproducibility

# Design factors matching paper Section 4.1
m_values = [16, 32, 64]              # Number of hypothesis tests
pi0_values = [0.75, 0.50, 0.25]      # Proportion of true nulls
effect_sizes = [0.5, 1.0, 1.5]       # Small, Medium, Large signals
alpha_levels = [0.05]                # Nominal FDR level

# Ensure output directory exists
os.makedirs("results/raw", exist_ok=True)


def run_single_simulation(m, pi0, effect_size, alpha, seed):
    """
    Run one replicate of the simulation for a single combination of parameters.

    Parameters
    ----------
    m : int
        Number of hypothesis tests.
    pi0 : float
        Proportion of true null hypotheses.
    effect_size : float
        Mean of alternative distribution (Normal(effect_size, 1)).
    alpha : float
        Nominal FDR level.
    seed : int
        Random seed to ensure reproducibility.

    Returns
    -------
    dict
        Dictionary of FDR and Power for each method.
    """
    # Generate p-values for this replicate
    data = generate_pvalues(m=m, pi0=pi0, effect_size=effect_size, seed=seed)
    pvals = data["p_value"].values
    is_null = data["is_null"].values

    # Initialize dictionary for results
    results = {}

    # Define all methods to compare
    methods = {
        "BH": bh_procedure,
        "Bonferroni": bonferroni_method,
        "Uncorrected": uncorrected_method
    }

    # Apply each method and compute FDR + Power
    for name, method in methods.items():
        rejects = method(pvals, alpha=alpha)
        fdr = compute_fdr(rejects, is_null)
        power = compute_power(rejects, is_null)
        results[name] = {"FDR": fdr, "Power": power}

    return results


def run_simulation():
    """
    Run the full simulation across all design conditions.

    Returns
    -------
    DataFrame
        Complete set of simulation results.
    """
    print("Running simulation study...")
    results = []

    # Create all combinations of design parameters
    design_grid = list(itertools.product(m_values, pi0_values, effect_sizes, alpha_levels))

    # Outer loop: iterate over each condition
    for (m, pi0, effect_size, alpha) in tqdm(design_grid, desc="Conditions"):
        # Inner loop: replicate each condition N_REPS times
        for r in range(N_REPS):
            seed = SEED + r  # vary seed by replication
            sim_results = run_single_simulation(m, pi0, effect_size, alpha, seed)

            # Store each method's results
            for method, metrics in sim_results.items():
                results.append({
                    "method": method,
                    "m": m,
                    "pi0": pi0,
                    "effect_size": effect_size,
                    "alpha": alpha,
                    "rep": r,
                    "FDR": metrics["FDR"],
                    "Power": metrics["Power"]
                })

    # Convert list of dictionaries to DataFrame
    df_results = pd.DataFrame(results)

    # Save raw simulation output to disk
    out_path = os.path.join("results", "raw", "simulation_results.csv")
    df_results.to_csv(out_path, index=False)
    print(f"Simulation complete. Results saved to {out_path}")

    return df_results


if __name__ == "__main__":
    # Run simulation when executed directly (not during import)
    run_simulation()
