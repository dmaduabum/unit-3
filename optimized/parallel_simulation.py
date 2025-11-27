"""
parallel_simulation.py
----------------------------------------------
Parallelized simulation using joblib for BH (1995)
FDR simulation. Each replicate runs in parallel.

Author: Dili K. Maduabum
Last edit: November 2025
"""

import argparse
import numpy as np
import pandas as pd
import os
from joblib import Parallel, delayed

from simulation_opt import run_single_sim_opt


def run_parallel_simulation(n_cores=1, nsim=1000):
    """
    Run the optimized simulation in parallel.

    Parameters
    ----------
    n_cores : int
        Number of CPU cores to use.
    nsim : int
        Replicates per condition.

    Returns
    -------
    pd.DataFrame
    """

    conditions = [
        (100, 0.8, 2.5),
        (500, 0.8, 2.5),
        (1000, 0.8, 2.5)
    ]

    results = []

    print(f"Running parallel simulation with {n_cores} cores...")

    for m, pi0, eff in conditions:

        seeds = 2000 + np.arange(nsim)

        # >>> This is the joblib parallelism <<<
        out = Parallel(n_jobs=n_cores)(
            delayed(run_single_sim_opt)(
                m=m, pi0=pi0, effect_size=eff,
                alpha=0.05, seed=int(seeds[i])
            )
            for i in range(nsim)
        )

        results.extend(out)

    df = pd.DataFrame(results)

    os.makedirs("results/raw", exist_ok=True)
    df.to_csv("results/raw/parallel_opt_results.csv", index=False)

    print("Parallel simulation complete.")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", type=int, default=1,
                        help="Number of CPU cores to use.")
    parser.add_argument("--nsim", type=int, default=1000,
                        help="Replicates per condition.")
    args = parser.parse_args()

    run_parallel_simulation(args.cores, args.nsim)

