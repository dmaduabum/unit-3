"""
metrics.py
-----------------
This file defines simple functions to calculate performance measures
for the Benjamini & Hochberg (1995) False Discovery Rate (FDR) study.

Metrics include:
- False Discovery Rate (FDR)
- Power

Author: Dili K. Maduabum
Lasted Edited: October 21, 2025
"""

import numpy as np
import pandas as pd

def compute_fdr(rejects, is_null):
    """
    Calculate the False Discovery Rate (FDR).

    Parameters
    ----------
    rejects : array-like of bool
        True if the hypothesis was rejected.
    is_null : array-like of bool
        True if the hypothesis is actually null.

    Returns
    -------
    fdr : float
        Estimated false discovery rate (V/R).
        Returns 0.0 if there are no rejections.
    """
    rejects = np.asarray(rejects)
    is_null = np.asarray(is_null)

    # False discoveries = rejected but actually null
    false_discoveries = np.sum(rejects & is_null)
    total_rejections = np.sum(rejects)

    if total_rejections == 0:
        return 0.0  # avoid division by zero
    else:
        return false_discoveries / total_rejections


def compute_power(rejects, is_null):
    """
    Calculate the statistical power.

    Parameters
    ----------
    rejects : array-like of bool
        True if the hypothesis was rejected.
    is_null : array-like of bool
        True if the hypothesis is actually null.

    Returns
    -------
    power : float
        Estimated power = (true rejections / total false nulls).
        Returns 0.0 if there are no false nulls.
    """
    rejects = np.asarray(rejects)
    is_null = np.asarray(is_null)

    # True positives = rejected and actually false nulls
    true_positives = np.sum(rejects & ~is_null)
    total_false_nulls = np.sum(~is_null)

    if total_false_nulls == 0:
        return 0.0
    else:
        return true_positives / total_false_nulls


