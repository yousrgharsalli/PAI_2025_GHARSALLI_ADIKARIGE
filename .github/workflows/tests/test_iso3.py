from data_manager import DataManager
from country_iso_map import COUNTRY_TO_ISO3

def test_iso3_mapping_coverage_is_reasonable():
    dm = DataManager()
    assert not dm.df.empty, "CSV not loaded (DataFrame is empty)"

    countries = sorted(set(dm.df["Country"].dropna().unique()))
    mapped = [
        c for c in countries
        if COUNTRY_TO_ISO3.get(c) not in (None, "")
    ]

    coverage = len(mapped) / max(1, len(countries))

    assert coverage >= 0.85, f"ISO3 coverage too low: {coverage:.2%}"
