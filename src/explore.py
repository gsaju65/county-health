from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

raw = Path("data/raw/places_county_2025.csv")
clean = Path("data/processed/county_health.csv")
figdir = Path("figures")

def missingness(df):
    adj = [c for c in df.columns if c.endswith("_AdjPrev")]
    missing = df[adj].isna().sum().sort_values(ascending=False)
    print("missing counties per measure (top 10):")
    print(missing.head(10).to_string())
    print()

    counties_per_state = df.groupby("StateAbbr").size()
    for label, col in [("core health measures", "ACCESS2_AdjPrev"),
                       ("social-determinant measures", "LACKTRPT_AdjPrev")]:
        gone = df[df[col].isna()]
        per_state = gone.groupby("StateAbbr").size()
        whole = sorted(per_state[per_state == counties_per_state[per_state.index]].index)
        share = gone["TotalPopulation"].sum() / df["TotalPopulation"].sum()
        print(f"{label}: {len(gone)} counties missing, {share:.1%} of US population")
        print(f" states with every county missing: {', '.join(whole)}")
    print()

def correlations(df):
    df = df.copy()
    df["no_checkup"] = 100 - df["had_checkup"]
    df["no_dental"] = 100 - df["dental_visit"]

    candidates = ["uninsured", "no_checkup", "no_dental", "lacks_transportation",
                  "food_insecurity", "housing_insecurity"]
    outcomes = ["diabetes", "high_blood_pressure", "heart_disease", "obesity", "poor_health"]

    z = lambda s: (s - s.mean()) / s.std()
    burden = df[outcomes].apply(z).mean(axis=1)

    print("correlation of each candidate barrier with the disease-burden score:")
    for c in candidates:
        print(f"  {c:22s} {df[c].corr(burden):+.2f}")
    print("  -> no_checkup moves the wrong way and is excluded from the barrier score.")
    print()

    cols = candidates + outcomes
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticks(range(len(cols)))
    ax.set_yticklabels(cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(corr.iloc[i, j]) > 0.6 else "black")
    fig.colorbar(im, label="Pearson r")
    ax.set_title("How the barrier and disease measures move together")
    fig.savefig(figdir / "00_correlation_heatmap.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

def main():
    figdir.mkdir(exist_ok=True)
    print("=== missingness (raw file) ===")
    missingness(pd.read_csv(raw, thousands=","))
    print("=== correlations (cleaned file) ===")
    correlations(pd.read_csv(clean))
    print(f"wrote {figdir / '00_correlation_heatmap.png'}")

if __name__ == "__main__":
    main()