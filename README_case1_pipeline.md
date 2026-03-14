# Case 1 Reproducible Pipeline (Virginia / PJM / DOM)

This package turns Case 1 into a reproducible workflow.

## What is included
- case1_parameters.json
- build_case1_hourly_dataset.py
- compute_case1_crcc.py
- raw_template_pjm_lmp_dom.csv
- raw_template_pjm_stress_hours.csv
- raw_template_hourly_emissions.csv
- sample_case1_hourly_2025.csv
- sample_case1_option_hourly_components.csv
- sample_case1_option_summary.csv

## Workflow
1. Replace the three raw template CSVs with actual hourly exports.
2. Edit case1_parameters.json if needed.
3. Run build_case1_hourly_dataset.py
4. Run compute_case1_crcc.py
5. Use case1_option_summary.csv to draw Figure 5.1

## Important
sample_case1_hourly_2025.csv is synthetic but benchmark-calibrated.
It demonstrates the computation structure and column design.
