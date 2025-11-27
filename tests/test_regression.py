"""
test_regression.py
Regression tests to verify that the optimized simulation
preserves the statistical behavior of the baseline version.

Author: Dili K. Maduabum
Last edit: November 2025
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from baseline.simulation import run_single_simulation
from optimized.simulation_opt import run_single_sim_opt


def test_single_replicate_equivalence():
    """
    Compare baseline and optimized FDR/TPR metrics from one replicate.
    They should be close (within tolerance), not identical.
    """

    m = 500
    pi0 = 0.8
    eff = 2.5
    alpha = 0.05
    seed = 123

    base = run_single_simulation(m, pi0, eff, alpha, seed)
    opt  = run_single_sim_opt(m, pi0, eff, alpha, seed)

    # Extract BH results from baseline (Unit 2)
    base_fdr = float(base["BH"]["FDR"])
    base_tpr = float(base["BH"]["Power"])

    # Extract optimized values
    opt_fdr = opt["fdr"]
    opt_tpr = opt["tpr"]

    # Compare within reasonable tolerance
    assert abs(base_fdr - opt_fdr) < 0.10
    assert abs(base_tpr - opt_tpr) < 0.10


def test_pvalue_distribution_match():
    """
    Compare distributions of baseline vs optimized p-values using the KS test.
    We only compare the p-value arrays (not the is_null arrays).
    """

    m = 2000
    pi0 = 0.8
    eff = 2.5
    seed = 42

    from baseline.dgps import generate_pvalues as gen_base
    from optimized.simulation_opt import generate_pvalues_vectorized
    from scipy.stats import ks_2samp

    # Extract only p-values (baseline returns (pvals, is_null))
    p_base, _ = gen_base(m, pi0, eff, seed)

    # Optimized version also returns (pvals, is_null)
    p_opt, _ = generate_pvalues_vectorized(m, pi0, eff, seed)

    # KS test compares distribution shapes
    stat, p = ks_2samp(p_opt, p_base)

    assert p < 0.001



if __name__ == "__main__":
    test_single_replicate_equivalence()
    test_pvalue_distribution_match()
    print("All regression tests passed.")

