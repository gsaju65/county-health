# Measurements are done differently and come from different scales so it is converted to a z-score
# and averaged within its group 

from pathlib import Path
import pandas as pd

source = Path("data/processed/county_health.csv")
out = Path("data/processed/county_features.csv")

barriers = ["uninsured", "no_checkup", "no_dental", "lacks_transportation", 
            "food_insecurity", "housing_insecurity"]

outcomes = ["diabetes", "high_blood_pressure", "heart_disease", "obesity", "poor_health"]

def zscore(s):
    return (s - s.mean()) / s.std()

def main():
    df = pd.read_csv(source)

    df["no_checkup"] = 100 - df["had_checkup"]
    df["no_dental"] = 100 - df["dental_visit"]

    df["access_barrier_score"] = df[barriers].apply(zscore).mean(axis=1)
    df["disease_burden_score"] = df[outcomes].apply(zscore).mean(axis=1)

    df["barrier_quartile"] = pd.qcut(
        df["access_barrier_score"], 4,
        labels=["fewest barriers", "some", "many", "most barriers"]
    )

    r = df["access_barrier_score"].corr(df["disease_burden_score"])
    print(f"correlation between barriers and disease burden: r = {r:.3f}")
    print()
    print(df.groupby("barrier_quartile", observed=True)[
        ["uninsured", "diabetes", "high_blood_pressure", "poor_health", "TotalPopulation"]
    ].median().round(1).to_string())

    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"\nwrote {out}")

if __name__ == "__main__":
    main()