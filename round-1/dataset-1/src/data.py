#!/usr/bin/env python3
"""Format panel dataset into exp_sel_data_out.json schema."""
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "loguru",
# ]
# ///

import json
from pathlib import Path
import pandas as pd
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

@logger.catch(reraise=True)
def main():
    workspace = Path(__file__).parent
    datasets_dir = workspace / "temp/datasets"
    output_file = workspace / "full_data_out.json"
    
    # Load final panel dataset
    logger.info("Loading final panel dataset...")
    df = pd.read_json(datasets_dir / "full_panel_final.json", orient='records')
    
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    
    # Format into exp_sel_data_out.json schema
    # Each row = 1 example
    examples = []
    
    for idx, row in df.iterrows():
        # Create input as JSON string of features
        input_features = {
            'gini': row.get('gini'),
            'education_years': row.get('education_years'),
            'social_spending': row.get('social_spending'),
            'gdp_per_capita': row.get('gdp_per_capita'),
            'resource_rents': row.get('resource_rents'),
            'population': row.get('population'),
            'gini_x_education': row.get('gini_x_education'),
            'gini_x_social': row.get('gini_x_social'),
            'triple_interaction': row.get('triple_interaction')
        }
        
        example = {
            'input': json.dumps(input_features),
            'output': str(row['vdem_electoral']),
            'metadata_fold': idx % 5,  # 5-fold CV
            'metadata_feature_names': list(input_features.keys()),
            'metadata_task_type': 'regression',
            'metadata_row_index': idx,
            'metadata_country': row['Code'],
            'metadata_year': int(row['Year'])
        }
        examples.append(example)
    
    # Wrap in datasets array format
    output = {
        'datasets': [
            {
                'dataset': 'owid_panel_triple_shield',
                'examples': examples
            }
        ]
    }
    
    # Save
    logger.info(f"Saving {len(examples)} examples to {output_file}")
    output_file.write_text(json.dumps(output, indent=2))
    
    # Save data dictionary
    data_dict = {
        'dataset_name': 'owid_panel_triple_shield',
        'n_examples': len(examples),
        'n_countries': len(df['Code'].unique()),
        'years': f"{df['Year'].min()}-{df['Year'].max()}",
        'task_type': 'regression',
        'target': 'vdem_electoral',
        'features': list(input_features.keys()),
        'missing_data': {col: int(df[col].isnull().sum()) for col in df.columns if df[col].isnull().sum() > 0}
    }
    (workspace / 'data_dictionary.json').write_text(json.dumps(data_dict, indent=2))
    
    logger.info(f"Output saved: {output_file}")
    logger.info(f"Data dictionary saved: {workspace / 'data_dictionary.json'}")
    
    return output

if __name__ == '__main__':
    result = main()
    logger.info("Done!")
