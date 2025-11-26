import time
import matplotlib.pyplot as plt
import numpy as np

from simulation import run_single_simulation

def time_run(m, pi0=0.8, effect_size=2.5, alpha=0.05):
    """Time one simulation call (NOT full study)."""
    start = time.time()
    _ = run_single_simulation(m=m, pi0=pi0, effect_size=effect_size, alpha=alpha, seed=123)
    end = time.time()
    return end - start

def main():
    # Values of m to test
    m_values = [50, 100, 200, 400, 800, 1600]

    times = []
    print("Running timing experiments...")
    for m in m_values:
        t = time_run(m)
        times.append(t)
        print(f"m={m}, time={t:.4f} seconds")

    # Save results
    np.savetxt("results/raw/complexity_results.csv",
               np.column_stack([m_values, times]),
               delimiter=",",
               header="m,time",
               comments='')

    # Plot
    plt.figure(figsize=(8,6))
    plt.loglog(m_values, times, marker='o')
    plt.xlabel("m (number of hypotheses)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Baseline Runtime vs m")
    plt.grid(True, which="both", ls="--")

    plt.savefig("results/figures/baseline_complexity.png", dpi=150)
    plt.close()

    print("\nComplexity analysis complete.")
    print("Saved: results/raw/complexity_results.csv")
    print("Saved: results/figures/baseline_complexity.png")

if __name__ == "__main__":
    main()

