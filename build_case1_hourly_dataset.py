import json
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent
params = json.loads((BASE / "case1_parameters.json").read_text(encoding="utf-8"))
lmp = pd.read_csv(BASE / "raw_template_pjm_lmp_dom.csv", parse_dates=["timestamp"])
stress = pd.read_csv(BASE / "raw_template_pjm_stress_hours.csv", parse_dates=["timestamp"])
em = pd.read_csv(BASE / "raw_template_hourly_emissions.csv", parse_dates=["timestamp"])
df = lmp.merge(stress, on="timestamp", how="inner").merge(em, on="timestamp", how="inner")
df["it_load_mw"] = params["planning_parameters"]["it_load_mw"]
df["pue"] = params["planning_parameters"]["pue"]
df["eta_compute_per_mwh_it"] = params["planning_parameters"]["eta_compute_per_mwh_it"]
df["carbon_shadow_price_usd_per_tco2"] = params["planning_parameters"]["carbon_shadow_price_usd_per_tco2"]
df["reliability_valuation_usd_per_compute_unit"] = params["planning_parameters"]["reliability_valuation_usd_per_compute_unit"]
df["location_based_emissions_baseline_tco2_per_mwh"] = params["planning_parameters"]["location_based_emissions_baseline_tco2_per_mwh"]
df.to_csv(BASE / "case1_hourly_dataset_built.csv", index=False)
print("Built case1_hourly_dataset_built.csv")
