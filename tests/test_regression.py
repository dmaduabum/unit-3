"""
test_regression.py
Regression tests for the optimized BH (1995) simulation.

Author: Dili K. Maduabum
Last edit: November 2025
"""
import os
import numpy as np
from scipy.stats import ks_2samp
from baseline.simulation import run_single_simulation
from optimized.simulation_opt import run_single_sim_opt

def test_single_replicate_equivalence():
    """
    Compare baseline and optimized single replicates for distributional equivalence.
    """

    m = 500
    pi0 = 0.8
    eff = 2.5
    alpha = 0.05
    seed = 123

    base = run_single_simulation(m, pi0, eff, alpha, seed)
    opt  = run_single_sim_opt(m, pi0, eff, alpha, seed)

    # Compare metrics
    assert abs(base["fdr"] - opt["fdr"]) < 0.05
    assert abs(base["tpr"] - opt["tpr"]) < 0.05

def test_distribution_equivalence():
    """
    Monte Carlo comparison between baseline and optimized p-value distributions.
    """

    m = 1000
    pi0 = 0.8
    eff = 2.5
    alpha = 0.05

    from optimized.simulation_opt import generate_pvalues_vectorized
    from baseline.dgps import generate_pvalues as gen_base

    p1, _ = generate_pvalues_vectorized(m, pi0, eff, seed=1)
    p2 = gen_base(m, pi0, eff, seed=1)

    # KS test for distributional equivalence
    stat, p = ks_2samp(p1, p2)
    assert p > 0.05   # fail only if distribution meaningfully differs

