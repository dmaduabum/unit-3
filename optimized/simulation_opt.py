"""
simulation_opt.py
----------------------------------------------
Optimized (vectorized) simulation for BH (1995)
FDR estimation study. Uses NumPy to eliminate
most Python loops.

Author: Dili K. Maduabum
Last edit: November 2025
"""

import numpy as np
import pandas as pd
from scipy.stats import norm


# -------------------------------------------------------
# Vectorized Data Generation
# -------------------------------------------------------

def generate_pvalues_vectorized(m, pi0, effect_size, seed=None):
    """
    Vectorized p-value generation.

    Under null: X ~ N(0,1)
    Under alt:  X ~ N(effect_size, 1)

    Returns
    -------
    pvals : np.ndarray  shape (m,)
    is_null : np.ndarray bool mask
    """
    if seed is not None:
        np.random.seed(seed)

    m0 = int(m * pi0)
    m1 = m - m0

    # Single vector of z-values
    z = np.empty(m)
    z[:m0] = np.random.normal(0, 1, m0)
    z[m0:] = np.random.normal(effect_size, 1, m1)

    pvals = 2 * (1 - norm.cdf(np.abs(z)))

    is_null = np.zeros(m, dtype=bool)
    is_null[:m0] = True

    return pvals, is_null


# -------------------------------------------------------
# Vectorized BH FDR Procedure
# -------------------------------------------------------

def benjamini_hochberg_vectorized(pvals, alpha=0.05):
    """
    Fully vectorized BH procedure.

    Returns
    -------
    rejected : boolean array
    """
    m = len(pvals)
    order = np.argsort(pvals)
    ordered_p = pvals[order]

    thresholds = (np.arange(1, m+1) / m) * alpha
    passed = ordered_p <= thresholds

    if not np.any(passed):
        return np.zeros(m, dtype=bool)

    k = np.max(np.where(passed))
    cutoff = ordered_p[k]

    return pvals <= cutoff


# -------------------------------------------------------
# Optimized Single Simulation
# -------------------------------------------------------

def run_single_sim_opt(m, pi0, effect_size, alpha=0.05, seed=None):
    """
    Run a single optimized simulation replicate.
    """
    pvals, is_null = generate_pvalues_vectorized(m, pi0, effect_size, seed)

    rejected = benjamini_hochberg_vectorized(pvals, alpha)

    v = np.sum(rejected & is_null)
    r = np.sum(rejected)
    fdr_hat = v / r if r > 0 else 0

    tpr = np.sum(rejected & ~is_null) / np.sum(~is_null)

    return {
        "m": m,
        "pi0": pi0,
        "effect_size": effect_size,
        "alpha": alpha,
        "fdr": fdr_hat,
        "tpr": tpr,
        "r": r
    }


# -------------------------------------------------------
# Full Optimized Simulation Study
# -------------------------------------------------------

def run_simulation_opt():
    """
    Run a small optimized simulation study.
    """
    conditions = [
        (100, 0.8, 2.5),
        (500, 0.8, 2.5),
        (1000, 0.8, 2.5)
    ]

    nsim = 1000
    all_results = []

    print("Running optimized (vectorized) simulation...")

    for m, pi0, eff in conditions:
        for i in range(nsim):
            seed = 1000 + i
            res = run_single_sim_opt(m, pi0, eff, 0.05, seed)
            all_results.append(res)

    df = pd.DataFrame(all_results)

    import os
    os.makedirs("results/raw", exist_ok=True)
    df.to_csv("results/raw/simulation_opt.csv", index=False)

    print("Optimized simulation complete.")


if __name__ == "__main__":
    run_simulation_opt()

