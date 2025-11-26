"""
visualize.py
-----------------
Generate publication-quality visualizations for the Benjamini & Hochberg (1995)
False Discovery Rate (FDR) simulation study.

Produces:
1. FDR vs alpha (for each method)
2. Power vs pi0 (for each method)

Figures are saved as high-resolution PDFs.

Author: Dili K. Maduabum
Last Edited: October 21, 2025
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load simulation results
data_path = os.path.join("results", "raw", "simulation_results.csv")
df = pd.read_csv(data_path)

# Summarize average FDR and Power across replications
summary = (
    df.groupby(["method", "m", "pi0", "effect_size", "alpha"])
      .agg(
          FDR_mean=("FDR", "mean"),
          FDR_sd=("FDR", "std"),
          Power_mean=("Power", "mean"),
          Power_sd=("Power", "std")
      )
      .reset_index()
)

# Ensure figure directory exists
os.makedirs("results/figures", exist_ok=True)

# Set default plot style
sns.set_style("whitegrid")

# ----------------------------------------------------
# Figure 1: FDR vs Alpha
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4))

sns.lineplot(
    data=summary,
    x="alpha",
    y="FDR_mean",
    hue="method",
    style="method",
    markers=True,
    ax=ax
)

ax.set_title("Average FDR by Method and Alpha Level")
ax.set_xlabel("Nominal FDR Level (α)")
ax.set_ylabel("Mean False Discovery Rate")

# Reference line y = x
ax.plot([0, 0.1], [0, 0.1], 'k--', linewidth=1, label="y = x")
ax.legend(title="Method", loc="upper left")

plt.tight_layout()
plt.savefig("results/figures/fdr_vs_alpha.pdf", dpi=300, bbox_inches="tight")
plt.close()

print("Figure 1 saved: fdr_vs_alpha.pdf")

# ----------------------------------------------------
# Figure 2: Power vs pi0
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4))

sns.lineplot(
    data=summary,
    x="pi0",
    y="Power_mean",
    hue="method",
    style="method",
    markers=True,
    ax=ax
)

ax.set_title("Average Power by Method and Proportion of True Nulls")
ax.set_xlabel(r"Proportion of True Nulls ($\pi_0$)")
ax.set_ylabel("Mean Power")
ax.legend(title="Method", loc="upper right")

plt.tight_layout()
plt.savefig("results/figures/power_vs_pi0.pdf", dpi=300, bbox_inches="tight")
plt.close()

print("Figure 2 saved: power_vs_pi0.pdf")
print("\nAll figures saved in results/figures/")
