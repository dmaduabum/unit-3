"""
methods.py
-----------------
This file defines simple multiple-testing correction methods used in the
simulation study for Benjamini & Hochberg (1995) False Discovery Rate (FDR).

Author: Dili K. Maduabum
Last Edited: October 21, 2025
"""

import numpy as np

def bh_procedure(p_values, alpha=0.05):
    """
    Apply the Benjamini–Hochberg (BH) FDR procedure.

    Parameters
    ----------
    p_values : array-like
        List or numpy array of p-values.
    alpha : float
        Desired false discovery rate (default = 0.05).

    Returns
    -------
    rejects : numpy array of bool
        True if hypothesis is rejected, False otherwise.
    """
    p_values = np.asarray(p_values)
    m = len(p_values)
    sorted_idx = np.argsort(p_values)
    sorted_p = p_values[sorted_idx]

    # Compute BH threshold line
    thresholds = (np.arange(1, m + 1) / m) * alpha
    below = sorted_p <= thresholds

    # Find largest k that satisfies the condition
    if not np.any(below):
        rejects = np.zeros(m, dtype=bool)
    else:
        k = np.max(np.where(below))
        cutoff = sorted_p[k]
        rejects = p_values <= cutoff

    return rejects


def bonferroni_method(p_values, alpha=0.05):
    """
    Apply Bonferroni correction for multiple testing.

    Reject if p <= alpha / m.
    """
    p_values = np.asarray(p_values)
    m = len(p_values)
    threshold = alpha / m
    rejects = p_values <= threshold
    return rejects


def uncorrected_method(p_values, alpha=0.05):
    """
    Apply no correction (just compare p <= alpha).
    """
    p_values = np.asarray(p_values)
    rejects = p_values <= alpha
    return rejects


if __name__ == "__main__":
    # Simple test run to verify methods
    test_p = np.array([0.001, 0.02, 0.04, 0.06, 0.2, 0.9])
    print("Input p-values:", test_p)
    
    print("\nBH Procedure:")
    print(bh_procedure(test_p, alpha=0.05))
    
    print("\nBonferroni Method:")
    print(bonferroni_method(test_p, alpha=0.05))
    
    print("\nUncorrected:")
    print(uncorrected_method(test_p, alpha=0.05))
