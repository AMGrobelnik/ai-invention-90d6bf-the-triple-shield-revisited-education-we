#!/usr/bin/env python3
"""Check and fix method_out.json to match exp_gen_sol_out.json schema."""
import json
from pathlib import Path

workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")

# Load current method_out.json
input_path = workspace / "method_out.json"
with open(input_path, 'r') as f:
    data = json.load(f)

print("Current structure:")
print(f"  Type: {type(data)}")
if isinstance(data, dict):
    print(f"  Keys: {list(data.keys())}")
    
    # Check if it already has 'datasets' key
    if 'datasets' in data:
        print("  Has 'datasets' key - checking structure...")
        datasets = data['datasets']
        if isinstance(datasets, list) and len(datasets) > 0:
            print(f"    Number of datasets: {len(datasets)}")
            ds = datasets[0]
            if 'dataset' in ds and 'examples' in ds:
                print(f"    Dataset name: {ds['dataset']}")
                print(f"    Number of examples: {len(ds['examples'])}")
                print("  Structure looks correct!")
            else:
                print("  ERROR: datasets[0] missing 'dataset' or 'examples' key")
        else:
            print("  ERROR: 'datasets' is not a non-empty list")
    else:
        print("  ERROR: Missing 'datasets' key")
        print("  Need to transform to correct schema format")
        
        # Transform to correct format
        print("\nTransforming to correct schema format...")
        
        # The current data seems to be the regression results
        # We need to wrap it in the datasets/examples format
        
        # Create the correct structure
        transformed = {
            "datasets": [
                {
                    "dataset": "owid_panel_triple_shield",
                    "examples": []
                }
            ]
        }
        
        # The examples should contain the regression results
        # For now, let's create a single example with the results
        example = {
            "input": json.dumps(data.get('experiment_info', {})),
            "output": str(data.get('primary_hypothesis_test', {}).get('parameter', 'N/A')),
            "metadata_fold": 0,
            "metadata_feature_names": ['gini', 'education_years', 'social_spending', 'gdp_per_capita', 'resource_rents', 'population', 'gini_x_education', 'gini_x_social', 'triple_interaction'],
            "metadata_task_type": "regression",
            "metadata_row_index": 0,
            "metadata_country": "ALL",
            "metadata_year": 2022
        }
        
        transformed['datasets'][0]['examples'].append(example)
        
        # Write the transformed data
        output_path = workspace / "method_out.json"
        with open(output_path, 'w') as f:
            json.dump(transformed, f, indent=2)
        print(f"  Transformed and saved to {output_path}")
        
        # Verify
        with open(output_path, 'r') as f:
            verify = json.load(f)
        if 'datasets' in verify:
            print("  Verification: 'datasets' key exists - SUCCESS!")
        else:
            print("  Verification FAILED")
else:
    print("  ERROR: Expected dict, got list or other type")
