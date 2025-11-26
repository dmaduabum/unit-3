"""
dgps.py
-----------------
Data-generating functions for BH (1995) FDR simulation.
normal means with varying signal strengths.

Author: Dili K. Maduabum
Last edit: October 21, 2025
"""

import numpy as np
import pandas as pd

def generate_pvalues(m=100, pi0=0.8, effect_size=1.0, seed=None):
    """
    Generate p-values from normal means model (matches paper).
    
    Under null: X ~ N(0, 1)
    Under alternative: X ~ N(effect_size, 1)
    Convert to two-sided z-test p-values.
    """
    if seed is not None:
        np.random.seed(seed)
    
    m0 = int(m * pi0)
    m1 = m - m0
    
    # Generate observations
    null_obs = np.random.normal(0, 1, m0)
    alt_obs = np.random.normal(effect_size, 1, m1)
    
    # Convert to p-values (two-sided z-test)
    from scipy.stats import norm
    p_null = 2 * (1 - norm.cdf(np.abs(null_obs)))
    p_alt = 2 * (1 - norm.cdf(np.abs(alt_obs)))
    
    # Combine
    p_values = np.concatenate([p_null, p_alt])
    is_null = np.array([True] * m0 + [False] * m1)
    
    # Shuffle
    idx = np.random.permutation(m)
    
    return pd.DataFrame({
        "p_value": p_values[idx],
        "is_null": is_null[idx]
    })

