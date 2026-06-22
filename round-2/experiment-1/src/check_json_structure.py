#!/usr/bin/env python3
"""Check method_out.json structure."""
import json
from pathlib import Path

workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
input_path = workspace / "method_out.json"

print(f"Loading {input_path}...")
with open(input_path, 'r') as f:
    data = json.load(f)

print(f"\nType: {type(data)}")
if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")
    for key in list(data.keys())[:5]:
        print(f"  {key}: {type(data[key])}")
        if isinstance(data[key], dict):
            print(f"    Sub-keys: {list(data[key].keys())[:5]}")
        elif isinstance(data[key], list):
            print(f"    List length: {len(data[key])}")
            if len(data[key]) > 0:
                print(f"    First item type: {type(data[key][0])}")
else:
    print("Not a dict - might be a list")
    if isinstance(data, list):
        print(f"List length: {len(data)}")
        if len(data) > 0:
            print(f"First item: {data[0]}")

print("\nDone")
