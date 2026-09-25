import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

source = Path("data/processed/county_features.csv")
figdir = Path("figures")

quartile_colors = ["#BFDBFE", "#60A5FA", "#2563EB", "#1E3A8A"]
ink = "#0F172A"
muted = "#475569"

#Figure 1
def figure_scatter(df):
    fig, ax = plt.subplots(figsize=(9,6))
    ax.scatter(df["access_barrier_score"], df["disease_burden_score"], s=14, alpha=0.35, color="#2563EB")

    r = df["access_barrier_score"].corr(df["disease_burden_score"])
    ax.set_title("Counties with more barriers to get care have more chronic disease", fontsize=12, fontweight="bold", loc="left", pad=40)
    ax.text(0, 1.03,
            f"Each dot is one US county (n = {len(df):,}). correlation r = {r:.2f}.",
            transform=ax.transAxes, fontsize=10, color=muted)

    ax.set_xlabel("Access barrier score (higher = harder to get care)", fontsize=10, color=muted)
    ax.set_ylabel("Disease burden score (higher = more chronic disease)", fontsize=10, color=muted)

    ax.grid(color="#E2E8F0", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)

    fig.savefig(figdir / "01_barriers_vs_disease.png", dpi=200,bbox_inches="tight")
    plt.close(fig)

#Figure 2
def figure_quartiles(df):
    outcomes = ["heart_disease", "diabetes", "poor_health", "high_blood_pressure", "obesity"]
    order = ["fewest barriers", "some", "many", "most barriers"]
    med = df.groupby("barrier_quartile", observed=True)[outcomes].median()
    med = med.reindex(order)

    med = med.rename(columns={"heart_disease": "Heart disease",
                                "diabetes": "Diabetes",
                                "poor_health": "Poor general health",
                                "high_blood_pressure": "High blood pressure",
                                "obesity": "Obesity"})

    ax = med.T.plot(kind="bar", figsize=(9, 5.5),
                    color=quartile_colors, rot=0)
    ax.set_title("Every chronic-disease measure gets worse as barriers to care rise\n"
                 "Median % of adults, by county barrier quartile")
    ax.set_ylabel("% of adults")
    ax.legend(frameon=False, ncol=4)
    ax.figure.savefig(figdir / "02_outcomes_by_quartile.png",
                      dpi=200, bbox_inches="tight")
    plt.close(ax.figure)

#Figure 3
def figure_population(df):
    order = ["fewest barriers", "some", "many", "most barriers"]
    med = df.groupby("barrier_quartile", observed=True)["TotalPopulation"].median()
    med = med.reindex(order)

    ax = med.plot(kind="barh", figsize=(9, 4.5), color=quartile_colors)
    ax.bar_label(ax.containers[0], fmt="{:,.0f}", padding=4, fontweight="bold")

    ax.set_title("The counties facing the most barriers are the smallest\n"
                 "Median county population by barrier quartile")
    ax.set_xlabel("Median population")
    ax.set_ylabel("")
    ax.invert_yaxis()

    ax.figure.savefig(figdir / "03_population_by_quartile.png",
                      dpi=200, bbox_inches="tight")
    plt.close(ax.figure)

#Figure 4
def figure_states(df):
    per_state = df.groupby("StateAbbr").size()
    top = df[df["barrier_quartile"] == "most barriers"].groupby("StateAbbr").size()
    share = (top / per_state).fillna(0) * 100
    share = share[per_state >= 10].sort_values(ascending=False).head(10)

    ax = share.plot(kind="barh", figsize=(9, 5), color="#1E3A8A")
    ax.bar_label(ax.containers[0], fmt="{:.0f}%", padding=4, fontweight="bold")

    ax.set_title("The highest-barrier counties cluster in the South\n"
                 "Share of each state's counties in the 'most barriers' quartile (top 10 states)")
    ax.set_xlabel("% of the state's counties")
    ax.set_ylabel("")
    ax.invert_yaxis()

    ax.figure.savefig(figdir / "04_top_quartile_by_state.png",
                      dpi=200, bbox_inches="tight")
    plt.close(ax.figure)

def main():
    figdir.mkdir(exist_ok=True)
    df = pd.read_csv(source)
    figure_scatter(df)
    figure_quartiles(df)
    figure_population(df)
    figure_states(df)
    print(f"wrote 4 figures to {figdir}")

if __name__ == "__main__":
    main()
