import json
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent
params = json.loads((BASE / "case1_parameters.json").read_text(encoding="utf-8"))
df = pd.read_csv(BASE / "case1_hourly_dataset_built.csv", parse_dates=["timestamp"])
facility_electricity = params["planning_parameters"]["it_load_mw"] * params["planning_parameters"]["pue"]
potential_compute = params["planning_parameters"]["it_load_mw"] * params["planning_parameters"]["eta_compute_per_mwh_it"]
lam = params["planning_parameters"]["carbon_shadow_price_usd_per_tco2"]
nu = params["planning_parameters"]["reliability_valuation_usd_per_compute_unit"]
comp=[]
summary=[]
for opt, vals in params["options"].items():
    tmp = df[["timestamp","lmp_usd_per_mwh","emissions_tco2_per_mwh","stress_indicator"]].copy()
    alpha = 1 - vals["stress_severity_kappa"] * tmp["stress_indicator"]
    tmp["option"] = opt
    tmp["availability_alpha"] = alpha
    tmp["facility_electricity_mwh"] = facility_electricity
    tmp["potential_compute"] = potential_compute
    tmp["delivered_compute"] = alpha * potential_compute
    tmp["electricity_component_usd"] = tmp["lmp_usd_per_mwh"] * vals["price_multiplier"] * facility_electricity
    tmp["carbon_component_usd"] = lam * tmp["emissions_tco2_per_mwh"] * facility_electricity
    tmp["reliability_component_usd"] = nu * (1 - alpha) * potential_compute
    comp.append(tmp)
    total_delivered = tmp["delivered_compute"].sum()
    elec = tmp["electricity_component_usd"].sum() / total_delivered
    carb = tmp["carbon_component_usd"].sum() / total_delivered
    rel = tmp["reliability_component_usd"].sum() / total_delivered
    summary.append({"option": opt,"electricity_component_usd_per_delivered_compute": round(elec,2),"carbon_component_usd_per_delivered_compute": round(carb,2),"reliability_component_usd_per_delivered_compute": round(rel,2),"crcc_total_usd_per_delivered_compute": round(elec+carb+rel,2)})
pd.concat(comp, ignore_index=True).to_csv(BASE / "case1_option_hourly_components.csv", index=False)
pd.DataFrame(summary).to_csv(BASE / "case1_option_summary.csv", index=False)
print("Wrote case1_option_hourly_components.csv and case1_option_summary.csv")
