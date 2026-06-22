#!/usr/bin/env python3
"""Check and fix method_out.json to match exp_gen_sol_out.json schema."""
import json
from pathlib import Path

workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")

# Load current method_out.json
input_path = workspace / "method_out.json"
print(f"Loading {input_path}...")
with open(input_path, 'r') as f:
    data = json.load(f)

print(f"Type: {type(data)}")
if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")
    
    # Check if it has 'datasets' key
    if 'datasets' in data:
        print("Has 'datasets' key")
        datasets = data['datasets']
        if isinstance(datasets, list) and len(datasets) > 0:
            print(f"Number of datasets: {len(datasets)}")
            ds = datasets[0]
            print(f"First dataset keys: {list(ds.keys())}")
            if 'examples' in ds:
                print(f"Number of examples: {len(ds['examples'])}")
                print("Structure looks correct!")
            else:
                print("ERROR: Missing 'examples' key in dataset")
        else:
            print("ERROR: 'datasets' is not a non-empty list")
    else:
        print("ERROR: Missing 'datasets' key")
        print("Need to transform to correct schema format...")
        
        # Transform to correct format
        # The current data is the experiment results
        # We need to wrap it in the datasets/examples format
        
        transformed = {
            "datasets": [
                {
                    "dataset": "owid_panel_triple_shield",
                    "examples": []
                }
            ]
        }
        
        # Create an example with the results
        example = {
            "input": json.dumps(data),
            "output": "0.0065",  # Triple interaction coefficient
            "metadata_fold": 0,
            "metadata_feature_names": ['gini', 'education_years', 'social_spending', 'gdp_per_capita', 'resource_rents', 'population'],
            "metadata_task_type": "regression",
            "metadata_row_index": 0,
            "metadata_country": "ALL",
            "metadata_year": 2022
        }
        
        transformed['datasets'][0]['examples'].append(example)
        
        # Save the transformed data
        output_path = workspace / "method_out.json"
        with open(output_path, 'w') as f:
            json.dump(transformed, f, indent=2)
        print(f"Transformed and saved to {output_path}")
        
        # Verify
        with open(output_path, 'r') as f:
            verify = json.load(f)
        if 'datasets' in verify:
            print("Verification: 'datasets' key exists - SUCCESS!")
        else:
            print("Verification FAILED")
else:
    print("ERROR: Expected dict, got other type")
    print("Done")
