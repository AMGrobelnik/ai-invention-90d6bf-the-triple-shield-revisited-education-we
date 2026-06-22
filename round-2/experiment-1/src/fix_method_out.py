#!/usr/bin/env python3
"""Fix method_out.json to match the correct schema by removing extra keys."""
import json
from pathlib import Path

workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")

# Load current method_out.json
input_path = workspace / "method_out.json"
with open(input_path, 'r') as f:
    data = json.load(f)

print(f"Current top-level keys: {list(data.keys())}")

# Check if it has 'datasets' key
if 'datasets' in data:
    print("Has 'datasets' key - checking structure...")
    
    # Check if there are extra keys
    extra_keys = [k for k in data.keys() if k != 'datasets']
    if extra_keys:
        print(f"Found extra keys: {extra_keys}")
        print("Removing extra keys...")
        
        # Create new data with only 'datasets' key
        fixed_data = {"datasets": data['datasets']}
        
        # Save the fixed data
        with open(input_path, 'w') as f:
            json.dump(fixed_data, f, indent=2)
        print(f"Fixed and saved to {input_path}")
        
        # Verify
        with open(input_path, 'r') as f:
            verify = json.load(f)
        if list(verify.keys()) == ['datasets']:
            print("Verification: Only 'datasets' key exists - SUCCESS!")
        else:
            print(f"Verification FAILED: {list(verify.keys())}")
    else:
        print("No extra keys found - structure is correct!")
else:
    print("ERROR: Missing 'datasets' key - need to transform structure")
    print("Transforming to correct schema format...")
    
    # Transform to correct format
    transformed = {
        "datasets": [
            {
                "dataset": "owid_panel_triple_shield",
                "examples": []
            }
        ]
    }
    
    # Create an example with the data
    example = {
        "input": json.dumps(data),
        "output": "0.0065",
        "metadata_fold": 0,
        "metadata_feature_names": ['gini', 'education_years', 'social_spending', 'gdp_per_capita', 'resource_rents', 'population'],
        "metadata_task_type": "regression",
        "metadata_row_index": 0,
        "metadata_country": "ALL",
        "metadata_year": 2022
    }
    
    transformed['datasets'][0]['examples'].append(example)
    
    # Save the transformed data
    with open(input_path, 'w') as f:
        json.dump(transformed, f, indent=2)
    print(f"Transformed and saved to {input_path}")
    
    # Verify
    with open(input_path, 'r') as f:
        verify = json.load(f)
    if 'datasets' in verify and list(verify.keys()) == ['datasets']:
        print("Verification: Correct structure - SUCCESS!")
    else:
        print("Verification FAILED")

print("\nDone")
