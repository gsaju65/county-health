# County Health Access

This project uses CDC PLACES county-level data to compare a composite

**access barrier score** against a composite **disease burden score** across 2,299
US counties.

**Key finding:** the two are strongly associated (r = 0.81). In the quartile of counties
facing the most barriers, adults are 1.8x as likely to be uninsured and 1.6x as likely
to report poor general health as in the quartile facing the fewest.

## Dataset

**CDC PLACES: County Data (GIS Friendly Format), 2025 release**
Centers for Disease Control and Prevention, Division of Population Health.
Downloaded from https://data.cdc.gov

Raw file: `data/raw/places_county_2025.csv`

## Reproducing the analysis

```bash
pip install -r requirements.txt
python src/clean_data.py      # -> data/processed/county_health.csv
python src/features.py        # -> data/processed/county_features.csv
python src/make_figures.py    # -> figures/*.png
```

## Limitations
- **Two entire states are missing.** All 120 Kentucky counties and all 67 Pennsylvania
  counties have no estimates for any measure. This could impact the national average depending on what the average in those states looks like.
- **The newest measures have the worst coverage.** The seven social-determinant measures
  (food insecurity, housing insecurity, transportation, and others) are missing for 844
  counties, while the 33 established health measures are missing for only 187. The barrier score uses three of measures so the analysis only covers 2,299 of 3,143 counties.
