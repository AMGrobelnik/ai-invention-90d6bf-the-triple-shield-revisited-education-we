#!/usr/bin/env python3
"""Quick test of the full pipeline with 100 examples."""
from loguru import logger
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import sys
import numpy as np
import pandas as pd
import gc

# Add current directory to path
sys.path.insert(0, '.')

# Import functions from method.py
from method import (
    load_and_verify_data,
    fix_gini_scaling,
    prepare_data_for_imputation,
    run_mice_imputation,
    create_interaction_terms,
    add_index_info,
    run_panel_regression,
    fallback_imputation
)

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

def main():
    # Load a subset of full data
    data_dir = Path('/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_1/gen_art/gen_art_dataset_1')
    full_path = data_dir / 'full_data_out.json'
    
    print('Loading 100 examples from full data...')
    with open(full_path, 'r') as f:
        data = json.load(f)
    
    examples_subset = data['datasets'][0]['examples'][:100]
    data_subset = {'datasets': [{'examples': examples_subset}]}
    
    temp_path = Path('temp_100.json')
    with open(temp_path, 'w') as f:
        json.dump(data_subset, f)
    
    # Load and process
    df = load_and_verify_data(temp_path, mini=False)
    print(f'Loaded {df.shape[0]} observations')
    
    # Fix Gini scaling
    df = fix_gini_scaling(df)
    
    # Prepare for imputation
    df_imp, df_index = prepare_data_for_imputation(df)
    print(f'Prepared: df_imp shape={df_imp.shape}, df_index shape={df_index.shape}')
    
    # Run MICE with 5 imputations
    print('\nRunning MICE with 5 imputations...')
    imp_result = run_mice_imputation(df_imp, n_imputations=5, n_iterations=5)
    print('MICE successful!')
    
    # Add index back and create interaction terms
    df_imputed = imp_result.imputed_datasets[0]
    df_with_index = add_index_info(df_imputed, df_index)
    df_interact = create_interaction_terms(df_with_index)
    print(f'Interaction terms created: {df_interact.shape}')
    
    # Run regression
    print('\nRunning panel regression...')
    result = run_panel_regression(df_interact, model_spec='triple')
    if result:
        print('Regression successful!')
        print(f'N obs: {result.n_obs}')
        print(f'R-squared: {result.r_squared:.4f}')
        print(f'Triple interaction coef: {result.coefficients.get("triple_int", "N/A")}')
        print(f'Triple interaction p-val: {result.p_values.get("triple_int", "N/A")}')
    else:
        print('Regression failed')

if __name__ == "__main__":
    main()
