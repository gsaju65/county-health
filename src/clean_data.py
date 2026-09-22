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
    "DEPRESSION": "depression",
    "CSMOKING": "smoking",
    "LPA": "no_exercise",
}

def main():
    df = pd.read_csv(raw, thousands=",")
    print(f"raw: {df.shape[0]} counties, {df.shape[1]} columns")

    keep = ["StateAbbr", "StateDesc", "CountyName", "CountyFIPS", "TotalPopulation", "TotalPop18plus"]

    rename = {f"{code}_AdjPrev": name for code, name in measures.items()}
    df = df[keep + list(rename)].rename(columns=rename)

    missing = df[df["uninsured"].isna()]
    print(f"counties with no estimates: {len(missing)}")
    print(f" their median population: {missing['TotalPopulation'].median():,.0f}")
    print(f" median population overall: {df['TotalPopulation'].median():,.0f}")

    df = df.dropna(subset=list(rename.values()))
    print(f"clean: {df.shape[0]} counties, {df.shape[1]} columns")

    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"wrote {out}")

if __name__ == "__main__":
    main()