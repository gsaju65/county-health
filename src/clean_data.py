# Clean the CDC Places file into a usable table

from pathlib import Path
import pandas as pd

raw = Path("data/raw/places_county_2025.csv")
out = Path("data/processed/county_health.csv")

measures = {
    "ACCESS2": "uninsured",
    "CHECKUP": "had_checkup",
    
    "DENTAL": "dental_visit",
    "LACKTRPT": "lacks_transportation",
    "FOODINSECU": "food_insecurity",
    "HOUSINSECU": "housing_insecurity",
    
    "DIABETES": "diabetes",
    "BPHIGH": "high_blood_pressure",
    "CHD": "heart_disease",
    "OBESITY": "obesity",
    "GHLTH": "poor_health",
}

def main():
    df = pd.read_csv(raw, thousands=",")
    print(f"raw: {df.shape[0]} counties, {df.shape[1]} columns")

    keep = ["StateAbbr", "StateDesc", "CountyName", "CountyFIPS", "TotalPopulation", "TotalPop18plus"]

    rename = {f"{code}_AdjPrev": name for code, name in measures.items()}
    df = df[keep + list(rename)].rename(columns=rename)

    incomplete = df[df[list(rename.values())].isna().any(axis=1)]
    counties_per_state = df.groupby("StateAbbr").size()
    dropped_per_state = incomplete.groupby("StateAbbr").size()
    fully_dropped = sorted(dropped_per_state[dropped_per_state == counties_per_state[dropped_per_state.index]].index)
    pop_lost = incomplete["TotalPopulation"].sum() / df["TotalPopulation"].sum()

    print(f"counties missing at least one measure: {len(incomplete)}")
    print(f" states dropped entirely ({len(fully_dropped)}): {', '.join(fully_dropped)}")
    print(f" share of US population removed: {pop_lost:.1%}")
    print(f" median population of dropped counties: {incomplete['TotalPopulation'].median():,.0f}")
    print(f" median population overall: {df['TotalPopulation'].median():,.0f}")

    df = df.dropna(subset=list(rename.values()))
    print(f"clean: {df.shape[0]} counties, {df.shape[1]} columns")

    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"wrote {out}")

if __name__ == "__main__":
    main()