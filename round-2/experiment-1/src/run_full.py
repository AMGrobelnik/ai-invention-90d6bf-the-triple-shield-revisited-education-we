#!/usr/bin/env python3
"""Run full analysis on complete dataset."""
from loguru import logger
from pathlib import Path
import sys
import json

# Add current directory to path
sys.path.insert(0, '.')

from method import (
    load_and_verify_data,
    fix_gini_scaling,
    prepare_data_for_imputation,
    run_mice_imputation,
    create_interaction_terms,
    add_index_info,
    run_panel_regression,
    pool_results_rubins_rules,
    export_results,
    fallback_imputation
)

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/full_run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
    data_dir = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
    full_data_path = data_dir / "full_data_out.json"
    output_path = workspace / "method_out.json"
    
    logger.info("=" * 80)
    logger.info("FULL ANALYSIS: Running on full dataset (N=1,641)")
    logger.info("=" * 80)
    
    # Load full data
    df_full = load_and_verify_data(full_data_path, mini=False)
    logger.info(f"Full data loaded: {df_full.shape}")
    
    # Fix Gini scaling
    df_full = fix_gini_scaling(df_full)
    
    # Prepare for imputation (returns df_imp, df_index)
    df_full_imp, df_full_index = prepare_data_for_imputation(df_full)
    logger.info(f"Prepared for imputation: df_imp shape={df_full_imp.shape}")
    
    # Run MICE with 50 imputations
    logger.info("Running MICE on full data (50 imputations)...")
    try:
        imp_result_full = run_mice_imputation(df_full_imp, n_imputations=50, n_iterations=10)
    except Exception as e:
        logger.warning(f"MICE failed on full data: {e}")
        logger.info("Using fallback imputation...")
        imp_result_full = fallback_imputation(df_full_imp, n_imputations=20)
    
    # Run regression analysis on all imputed datasets
    logger.info("\n" + "=" * 80)
    logger.info("REGRESSION ANALYSIS: Running on all imputed datasets")
    logger.info("=" * 80)
    
    all_results = {
        'main': [],
        'two_way': [],
        'triple': []
    }
    
    for i, imp_df in enumerate(imp_result_full.imputed_datasets):
        logger.info(f"Processing imputation {i+1}/{len(imp_result_full.imputed_datasets)}")
        
        # Add index info back before creating interaction terms
        imp_df_with_index = add_index_info(imp_df, df_full_index)
        
        # Create interaction terms
        imp_df_interact = create_interaction_terms(imp_df_with_index)
        
        # Run all three models
        for model_spec in ['main', 'two_way', 'triple']:
            result = run_panel_regression(imp_df_interact, model_spec)
            if result:
                all_results[model_spec].append(result)
    
    # Pool results using Rubin's Rules
    logger.info("\n" + "=" * 80)
    logger.info("POOLING RESULTS: Applying Rubin's Rules")
    logger.info("=" * 80)
    
    pooled_results = {}
    params_of_interest = ['gini_z', 'education_years_z', 'social_spending_z', 
                           'gini_x_edu', 'gini_x_soc', 'triple_int']
    
    for param in params_of_interest:
        for model_spec in ['main', 'two_way', 'triple']:
            if all_results[model_spec]:
                key = f"{model_spec}_{param}"
                pooled = pool_results_rubins_rules(all_results[model_spec], param)
                if pooled:
                    pooled_results[key] = pooled
    
    # Export results
    logger.info("\n" + "=" * 80)
    logger.info("EXPORTING RESULTS")
    logger.info("=" * 80)
    
    final_results = {
        'experiment_info': {
            'hypothesis': 'Triple interaction: inequality × education × welfare spending on democracy',
            'method': 'MICE multiple imputation (50 imputations) + Fixed-effects panel regression',
            'n_countries': int(df_full.index.get_level_values('Code').nunique()),
            'n_years': int(df_full.index.get_level_values('Year').max() - df_full.index.get_level_values('Year').min() + 1),
            'n_observations_total': len(df_full),
            'n_imputations': imp_result_full.n_imputations,
        },
        'gini_scaling_fix': {'applied': True, 'description': 'Divided Gini values > 1 by 100'},
        'imputation_diagnostics': {
            'original_missing_pattern': imp_result_full.original_missing_pattern,
            'imputed_missing_pattern': imp_result_full.imputed_missing_pattern,
            'n_imputations': imp_result_full.n_imputations
        },
        'regression_results': {
            model_spec: [r.__dict__ for r in results] if results else []
            for model_spec, results in all_results.items()
        },
        'pooled_results': pooled_results,
        'primary_hypothesis_test': {
            'parameter': 'triple_int',
            'pooled_result': pooled_results.get('triple_triple_int', None),
            'interpretation': 'Positive coefficient supports triple shield hypothesis'
        }
    }
    
    export_results(final_results, output_path)
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("ANALYSIS COMPLETE")
    logger.info("=" * 80)
    
    triple_result = pooled_results.get('triple_triple_int', {})
    if triple_result:
        coef = triple_result.get('pooled_estimate', 0)
        pval = triple_result.get('pooled_pvalue', 1)
        ci_low = triple_result.get('ci_95_lower', 0)
        ci_high = triple_result.get('ci_95_upper', 0)
        
        logger.info("\nPRIMARY HYPOTHESIS TEST (Triple Interaction):")
        logger.info(f"  Coefficient: {coef:.4f}")
        logger.info(f"  p-value: {pval:.4f}")
        logger.info(f"  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
        
        if pval < 0.05:
            logger.info("  RESULT: Statistically significant (p < 0.05)")
        else:
            logger.info("  RESULT: Not statistically significant (p >= 0.05)")
    
    logger.info(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()
