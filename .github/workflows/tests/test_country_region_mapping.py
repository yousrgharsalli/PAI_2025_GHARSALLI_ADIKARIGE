import pandas as pd

INPUT_PATH = "happiness.csv"
OUTPUT_REPORT = "region_anomalies_report.csv"

df = pd.read_csv(INPUT_PATH, sep=";")

# 1) Détecter les années suspectes : une année est suspecte si, pour beaucoup de pays,
#    la région diffère à la fois de l'année précédente ET de l'année suivante.
df = df.sort_values(["Country", "Year"]).reset_index(drop=True)
df["PrevRegion"] = df.groupby("Country")["Region"].shift(1)
df["NextRegion"] = df.groupby("Country")["Region"].shift(-1)

df["MismatchPrev"] = df["PrevRegion"].notna() & (df["Region"] != df["PrevRegion"])
df["MismatchNext"] = df["NextRegion"].notna() & (df["Region"] != df["NextRegion"])

year_scores = df.groupby("Year")[["MismatchPrev", "MismatchNext"]].sum()
year_scores["TotalMismatch"] = year_scores["MismatchPrev"] + year_scores["MismatchNext"]

# Année suspecte 
SUSPECT_YEARS = year_scores[year_scores["TotalMismatch"] >= 5].index.tolist()

print("Années suspectes détectées:", SUSPECT_YEARS)
print(year_scores.sort_values("TotalMismatch", ascending=False).head(10))

# 2) Calculer la "région attendue" par pays en ignorant les années suspectes
clean_df = df[~df["Year"].isin(SUSPECT_YEARS)].copy()

# région attendue 
expected_region = (
    clean_df.groupby("Country")["Region"]
    .agg(lambda s: s.value_counts().index[0])  
)

df["ExpectedRegion"] = df["Country"].map(expected_region)

anomalies = df[df["Year"].isin(SUSPECT_YEARS) & df["ExpectedRegion"].notna() & (df["Region"] != df["ExpectedRegion"])][
    ["Year", "Country", "Region", "ExpectedRegion"]
].sort_values(["Year", "Country"])

print("\nExemple (France):")
print(df[df["Country"].str.lower() == "france"][["Year", "Country", "Region", "ExpectedRegion"]].sort_values("Year"))

print("\nNombre d'anomalies:", len(anomalies))

fixed = df.copy()
mask_fix = fixed["Year"].isin(SUSPECT_YEARS) & fixed["ExpectedRegion"].notna()
fixed.loc[mask_fix, "Region"] = fixed.loc[mask_fix, "ExpectedRegion"]

# Nettoyer les colonnes temporaires
fixed = fixed.drop(columns=["PrevRegion", "NextRegion", "MismatchPrev", "MismatchNext", "ExpectedRegion"])

# 5) Sauvegarder
anomalies.to_csv(OUTPUT_REPORT, sep=";", index=False)
fixed.to_csv(OUTPUT_FIXED, sep=";", index=False)

print(f"\n Rapport anomalies: {OUTPUT_REPORT}")
