#!/usr/bin/env python3
"""Convert panel dataset to exp_sel_data_out.json schema for experiment pipeline."""

import pandas as pd
import json
from pathlib import Path

# Load the merged panel dataset
df = pd.read_json('data_out.json', orient='records', lines=True)

# Define the task: Predict V-Dem democracy index from inequality + controls
# Input: Gini coefficient, education, social spending, region dummies
# Output: V-Dem Electoral Democracy Index (v2x_polyarchy)

feature_cols = ['gini', 'education', 'social_spending'] + \
              [c for c in df.columns if c.startswith('region_')]

# Create examples
examples = []
for idx, row in df.iterrows():
    # Skip rows with missing values in key variables
    if pd.isna(row['v2x_polyarchy']) or pd.isna(row['gini']):
        continue
        
    # Input: JSON string of feature values
    input_features = {col: float(row[col]) for col in feature_cols if pd.notna(row[col])}
    input_str = json.dumps(input_features)
    
    # Output: V-Dem index as string
    output_str = str(row['v2x_polyarchy'])
    
    # Metadata
    example = {
        'input': input_str,
        'output': output_str,
        'metadata_country': row['country'],
        'metadata_country_code': row['country_code'],
        'metadata_year': int(row['year']),
        'metadata_fold': idx % 5,  # 5-fold CV
        'metadata_feature_names': list(input_features.keys()),
        'metadata_task_type': 'regression',
        'metadata_n_classes': None
    }
    examples.append(example)

# Group by dataset name
output = {
    'datasets': [
        {
            'dataset': 'post1990_democratizers_panel',
            'examples': examples
        }
    ],
    'metadata': {
        'description': 'Post-1990 democratizers panel (1990-2022)',
        'source': 'OWID (World Bank PIP, V-Dem, Barro-Lee, OECD)',
        'n_countries': df['country'].nunique(),
        'years': f"{df['year'].min()}-{df['year'].max()}",
        'feature_cols': feature_cols,
        'target_col': 'v2x_polyarchy'
    }
}

# Save in exp_sel_data_out.json format
output_path = Path('full_data_out.json')
output_path.write_text(json.dumps(output, indent=2))
print(f"Saved {len(examples)} examples to {output_path}")
print(f"Dataset: {output['datasets'][0]['dataset']}")
print(f"Task: {examples[0]['metadata_task_type']}")
print(f"Sample input keys: {list(json.loads(examples[0]['input']).keys())}")
print(f"Sample output: {examples[0]['output']}")
