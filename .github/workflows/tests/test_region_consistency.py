from data_manager import DataManager

def test_each_country_has_single_region():
    dm = DataManager()
    assert not dm.df.empty, "CSV not loaded (DataFrame is empty)"

    region_counts = (
        dm.df.dropna(subset=["Country", "Region"])
            .groupby("Country")["Region"]
            .nunique()
    )

    offenders = region_counts[region_counts > 1]
    assert offenders.empty, (
        "Some countries are associated with multiple regions:\n"
        + offenders.to_string()
    )
