#!/usr/bin/env python3
"""Run panel regressions for the Triple Shield hypothesis."""
import json, sys
import warnings
warnings.filterwarnings('ignore')

# Load data iteratively
print("Loading data...")
with open('temp/datasets/full_panel_final.json', 'r') as f:
    data = json.load(f)

print(f"Loaded {len(data)} records")

# Check first record
print("First record keys:", list(data[0].keys()))

# Show available columns
if len(data) > 0:
    print("Columns:", list(data[0].keys()))
