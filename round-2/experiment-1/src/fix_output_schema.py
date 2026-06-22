#!/usr/bin/env python3
"""Fix method_out.json to use correct exp_gen_sol_out.json schema."""
import json
from pathlib import Path

# Load current method_out.json
workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
input_path = workspace / "method_out.json"

with open(input_path, 'r') as f:
    data = json.load(f)

# Create output in correct schema format
# Schema: { "datasets": [ { "dataset": "...", "examples": [...] } ] }
# Each example: { "input": "string", "output": "string", "metadata_*: ..." }

# Extract primary hypothesis test result
primary_test = data.get('primary_hypothesis_test', {})
triple_result = primary_test.get('pooled_result', {})

# Create examples array
examples = []

# Example 1: Primary hypothesis test (triple interaction)
if triple_result:
    example1 = {
        "input": json.dumps({
            "model": "triple_interaction",
            "n_countries": data.get('experiment_info', {}).get('n_countries', 50),
            "n_observations": data.get('experiment_info', {}).get('n_observations_total', 1641),
            "n_imputations": data.get('experiment_info', {}).get('n_imputations', 50)
        }),
        "output": str(triple_result.get('pooled_estimate', 0.0)),
        "metadata_fold": 0,
        "metadata_feature_names": [
            "gini_z", "education_years_z", "social_spending_z",
            "gini_x_edu", "gini_x_soc", "triple_int"
        ],
        "metadata_task_type": "regression",
        "metadata_row_index": 0,
        "metadata_country": "ALL",
        "metadata_year": 2022
    }
    examples.append(example1)

# Example 2: Main effects model
main_result = data.get('pooled_results', {}).get('main_gini_z', {})
if main_result:
    example2 = {
        "input": json.dumps({
            "model": "main_effects",
            "n_countries": data.get('experiment_info', {}).get('n_countries', 50)
        }),
        "output": str(main_result.get('pooled_estimate', 0.0)),
        "metadata_fold": 1,
        "metadata_feature_names": [
            "gini_z", "education_years_z", "social_spending_z"
        ],
        "metadata_task_type": "regression",
        "metadata_row_index": 1,
        "metadata_country": "ALL",
        "metadata_year": 2022
    }
    examples.append(example2)

# Construct final output
output_data = {
    "datasets": [
        {
            "dataset": "owid_panel_triple_shield",
            "examples": examples
        }
    ]
}

# Add full results as metadata (not in examples)
output_data['full_results'] = data

# Write fixed output
output_path = workspace / "method_out_fixed.json"
with open(output_path, 'w') as f:
    json.dump(output_data, f, indent=2, default=str)

print(f"Fixed output written to {output_path}")
print(f"Number of examples: {len(examples)}")

# Replace original with fixed version
import shutil
shutil.move(str(output_path), str(input_path))
print(f"Replaced {input_path} with fixed version")
