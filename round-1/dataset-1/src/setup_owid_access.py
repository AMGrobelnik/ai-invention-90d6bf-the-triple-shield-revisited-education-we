#!/usr/bin/env python3
"""Setup script to access OWID data directly via their public endpoints."""
import requests
import json
from pathlib import Path
import time

# OWID public endpoints
OWID_API = "https://api.ourworldindata.org/v1"
OWID_GRAPHER = "https://ourworldindata.org/grapher"

# Create output directory
output_dir = Path("temp/tables")
output_dir.mkdir(parents=True, exist_ok=True)

# Key datasets to search for based on the plan
datasets_to_find = [
    ("V-Dem", "electoral democracy index v2x_polyarchy"),
    ("Gini", "gini coefficient inequality"),
    ("Education", "mean years of schooling"),
    ("Social protection", "social protection spending"),
    ("GDP", "gdp per capita"),
    ("Population", "population total"),
    ("Resource rents", "natural resource rents"),
]

print("Setting up OWID data access...")
print("Will search OWID grapher for required variables")

# Search OWID grapher for each dataset
base_url = "https://ourworldindata.org/grapher"

# Known OWID dataset slugs for key variables
known_datasets = {
    "vdem_electoral": "electoral-democracy-index-v-dem",
    "gini": "gini-index-worldbank",
    "gini_aftertax": "gini-index-after-taxes-and-transfers",
    "education": "mean-years-of-schooling",
    "social_protection": "social-protection-spending-oecd",
    "gdp_per_capita": "gdp-per-capita-worldbank",
    "population": "population",
    "resource_rents": "natural-resource-rents",
}

print("\nKnown OWID dataset endpoints:")
for name, slug in known_datasets.items():
    url = f"{base_url}/{slug}"
    print(f"  {name}: {url}")

# Save the dataset mapping
mapping_file = output_dir / "owid_dataset_mapping.json"
mapping_file.write_text(json.dumps(known_datasets, indent=2))
print(f"\nSaved dataset mapping to {mapping_file}")
