# County Health Access

**Where it is harder to get care, people are sicker.** 
This project uses CDC PLACES county-level estimates to build an *access barrier score* and a *disease burden score* for 2,299 US counties, and asks two questions about how they relate.

## The two questions

**Q1. Do counties where it is harder to get care carry more chronic disease?**
Answered by figures 1 and 2.

**Q2. What kind of counties face the most barriers, and where are they?**
Answered by figures 3 and 4.

**Why does it matter and who it is for.** 
Health-policy debates usually happen at the national or state level, but care is delivered county by county. This story is for general readers and local decision-makers who want to see, in plain terms, how tightly
everyday obstacles like being uninsured, lacking transportation, or not having enough food track with chronic illness across the country, and which places carry the most of both.

## Key findings

- **Q1:** The two scores are strongly associated (r = 0.88). Every one of the five
  disease measures rises step by step across the barrier quartiles. Comparing the
  quartile of counties with the most barriers to the quartile with the fewest, the
  median county has 1.5x the diabetes rate (13.7% vs 9.0%), 1.6x the share of adults
  reporting poor general health (25.9% vs 16.0%), and 1.3x the high blood pressure
  rate (39.6% vs 29.8%).
- **Q2:** The highest-barrier counties are small and Southern. Their median population
  is 19,631, about half that of the lowest-barrier quartile (36,775). Nearly every
  county in Mississippi (99%) falls in the top barrier quartile, along with most of
  New Mexico, Louisiana, Georgia, South Carolina, and Arkansas.
- These counties hold people, not just problems: the "most barriers" quartile is a
  quarter of the counties but only 15% of the population in the data, because it is
  made up of small counties.

## Dataset

**CDC PLACES: County Data (GIS Friendly Format), 2025 release.**
Centers for Disease Control and Prevention, Division of Population Health.
Retrieved from <https://data.cdc.gov/500-Cities-Places/PLACES-County-Data-GIS-Friendly-Format-2025-releas/i46a-9kgh/about_data>.

- 3,143 counties, 167 columns, 40 health measures. Each measure appears as a crude
  prevalence, an age-adjusted prevalence, and a 95% confidence interval for each.
- This analysis uses the **age-adjusted prevalence** (`_AdjPrev`) columns so that
  counties with older populations are not penalized for age alone.
- These are **model-based estimates, not direct measurements.** CDC produces them
  from the 2022 and 2023 BRFSS surveys combined with Census population estimates and
  2019-2023 ACS data. Counties that were never surveyed directly get values predicted
  from their demographic profile.

Raw file: `data/raw/places_county_2025.csv`

## How the scores are built

Each measure is a percentage of adults on a different scale (heart disease around 6%, obesity around 38%), so each is converted to a z-score across counties and the z-scores are averaged 
within each group. Counties are then split into quartiles on the barrier score.

| Score | Measures (age-adjusted % of adults) |
|---|---|
| Access barrier score | uninsured, no dental visit in past year, lacks reliable transportation, food insecurity, housing insecurity |
| Disease burden score | diabetes, high blood pressure, coronary heart disease, obesity, fair or poor general health |

"No routine checkup in the past year" was tested and left out: counties with more chronic disease have *more* checkups (r = -0.39 with the disease burden score), so it measures demand for care, 
not a barrier to it. `src/explore.py` prints this check.

## Reproducing the analysis

```bash
pip install -r requirements.txt
python src/clean_data.py      # raw -> data/processed/county_health.csv, reports what is dropped
python src/explore.py         # missingness tables + figures/00_correlation_heatmap.png
python src/features.py        # scores + quartiles -> data/processed/county_features.csv
python src/make_figures.py    # figures/01 .. 04
```

## Limitations

- **Eleven states are missing entirely.** Three of the barrier measures (transportation, food, housing) are not published for every state. Every county in Texas, Florida, Tennessee, Kentucky, Pennsylvania, Colorado, Washington, Oregon, South Dakota, Wyoming, and Vermont is blank for them, so the analysis covers 2,299 of 3,143 counties in 40 states and leaves out about 29% of the US population.
- **Association, not cause, and partly built in.** PLACES estimates come from a model that uses demographic and socioeconomic inputs, so two measures modeled from the same inputs will move together. The r = 0.88 means 
"these estimates move together," not a measured strength of effect.

## Deliverables

Infographic and the its explanation is in the deliverable folder.