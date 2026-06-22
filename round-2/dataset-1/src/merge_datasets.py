#!/usr/bin/env python3
"""Merge OWID datasets and create panel for post-1990 democratizers with MICE imputation."""

from loguru import logger
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import json

logger.remove()
logger.add(lambda msg: print(msg, end=""), level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

@logger.catch(reraise=True)
def main():
    # Load datasets
    logger.info("Loading OWID datasets...")
    gini = pd.read_csv('owid_gini.csv')
    vdem = pd.read_csv('owid_vdem.csv')
    edu = pd.read_csv('owid_education.csv')
    social = pd.read_csv('owid_social_spending.csv')
    
    # Rename columns for consistency
    gini = gini.rename(columns={'Gini coefficient': 'gini', 'World region according to OWID': 'region'})
    vdem = vdem.rename(columns={'Electoral democracy index': 'v2x_polyarchy', 'World region according to OWID': 'region'})
    edu = edu.rename(columns={'Average years of schooling': 'education'})
    social = social.rename(columns={'Public social expenditure as a share of GDP': 'social_spending'})
    
    # Identify post-1990 democratizers (using full V-Dem data)
    logger.info("Identifying post-1990 democratizers...")
    
    # Countries with V-Dem > 0.5 in 1990-1999 (transition to democracy)
    vdem_1990s = vdem[(vdem['Year'] >= 1990) & (vdem['Year'] <= 1999)]
    transition_countries = vdem_1990s[vdem_1990s['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    # Exclude pre-1990 democracies (V-Dem > 0.5 in 1989)
    vdem_1989 = vdem[vdem['Year'] == 1989]
    pre1990_democracies = vdem_1989[vdem_1989['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    # Post-1990 democratizers
    post1990_democratizers = [c for c in transition_countries if c not in pre1990_democracies]
    
    logger.info(f"Found {len(post1990_democratizers)} post-1990 democratizers")
    logger.info(f"Sample: {post1990_democratizers[:10]}")
    
    # Now filter all datasets to 1990-2022 AND post-1990 democratizers
    logger.info("Filtering datasets to 1990-2022 and post-1990 democratizers...")
    gini = gini[gini['Entity'].isin(post1990_democratizers) & gini['Year'].between(1990, 2022)].copy()
    vdem = vdem[vdem['Entity'].isin(post1990_democratizers) & vdem['Year'].between(1990, 2022)].copy()
    edu = edu[edu['Entity'].isin(post1990_democratizers) & edu['Year'].between(1990, 2022)].copy()
    social = social[social['Entity'].isin(post1990_democratizers) & social['Year'].between(1990, 2022)].copy()
    
    # Merge datasets (use vdem region as primary)
    logger.info("Merging datasets...")
    merged = gini[['Entity', 'Code', 'Year', 'gini']].merge(
        vdem[['Entity', 'Code', 'Year', 'v2x_polyarchy', 'region']],
        on=['Entity', 'Code', 'Year'],
        how='outer'
    ).merge(
        edu[['Entity', 'Code', 'Year', 'education']],
        on=['Entity', 'Code', 'Year'],
        how='outer'
    ).merge(
        social[['Entity', 'Code', 'Year', 'social_spending']],
        on=['Entity', 'Code', 'Year'],
        how='outer'
    )
    
    logger.info(f"Merged dataset shape: {merged.shape}")
    logger.info(f"Missing values:\n{merged.isnull().sum()}")
    
    # Create region dummies
    merged['region'] = merged['region'].fillna('Unknown')
    region_dummies = pd.get_dummies(merged['region'], prefix='region')
    merged = pd.concat([merged, region_dummies], axis=1)
    
    # Prepare data for MICE
    logger.info("Preparing data for MICE imputation...")
    impute_vars = ['gini', 'v2x_polyarchy', 'education', 'social_spending']
    X = merged[impute_vars].copy()
    
    # Check ranges before imputation
    logger.info("Variable ranges before imputation:")
    for var in impute_vars:
        logger.info(f"{var}: {X[var].min():.3f} - {X[var].max():.3f} (missing: {X[var].isnull().sum()})")
    
    # Apply MICE with bounds
    logger.info("Running MICE imputation with bounds...")
    
    # Define bounds for each variable
    bounds = {
        'gini': (0, 1),
        'v2x_polyarchy': (0, 1),
        'education': (0, 20),
        'social_spending': (0, 50)
    }
    
    imputer = IterativeImputer(max_iter=50, random_state=42, sample_posterior=True)
    X_imputed = imputer.fit_transform(X)
    
    # Create imputed dataset
    merged_imputed = merged.copy()
    for i, var in enumerate(impute_vars):
        values = X_imputed[:, i]
        # Clip to bounds
        values = np.clip(values, bounds[var][0], bounds[var][1])
        merged_imputed[var] = values
    
    # Verify imputation
    logger.info("Variable ranges after imputation (with bounds):")
    for var in impute_vars:
        logger.info(f"{var}: {merged_imputed[var].min():.3f} - {merged_imputed[var].max():.3f}")
    
    # Save main output (data_out.json)
    logger.info("Saving datasets...")
    merged_imputed = merged_imputed.rename(columns={'Entity': 'country', 'Code': 'country_code', 'Year': 'year'})
    merged_imputed.to_json('data_out.json', orient='records', lines=True)
    
    # Save mini dataset (3 countries)
    mini_countries = post1990_democratizers[:3] if len(post1990_democratizers) >= 3 else post1990_democratizers
    mini_df = merged_imputed[merged_imputed['country'].isin(mini_countries)]
    mini_df.to_json('mini_data_out.json', orient='records', lines=True)
    
    # Save preview (first 3 rows)
    preview_df = merged_imputed.head(3)
    preview_df.to_json('preview_data_out.json', orient='records', lines=True)
    
    # Create data dictionary
    with open('data_dictionary.md', 'w') as f:
        f.write("# Data Dictionary: Post-1990 Democratizers Panel (1990-2022)\n\n")
        f.write("## Sources\n")
        f.write("- Gini coefficient: World Bank PIP (via OWID)\n")
        f.write("- V-Dem Electoral Democracy Index: V-Dem v13 (via OWID)\n")
        f.write("- Mean years of schooling: Barro and Lee (via OWID)\n")
        f.write("- Social protection spending: OECD (via OWID)\n\n")
        f.write("## Variables\n")
        f.write("- country: Country name (string)\n")
        f.write("- country_code: ISO 3-letter country code (string)\n")
        f.write("- year: Year (integer, 1990-2022)\n")
        f.write("- gini: Gini coefficient (float, 0-1 scale)\n")
        f.write("- v2x_polyarchy: V-Dem Electoral Democracy Index (float, 0-1)\n")
        f.write("- education: Mean years of schooling (float, years)\n")
        f.write("- social_spending: Social protection spending (% GDP, float)\n\n")
        f.write("## Imputation\n")
        f.write("- Method: MICE (IterativeImputer from sklearn)\n")
        f.write(f"- Variables imputed: {', '.join(impute_vars)}\n")
        f.write(f"- Missing data before: {merged[impute_vars].isnull().sum().sum()} total values\n")
        f.write("- Missing data after: 0 (all values imputed)\n\n")
        f.write("## Country List (N={})\n".format(len(post1990_democratizers)))
        for c in sorted(post1990_democratizers):
            f.write(f"- {c}\n")
    
    logger.info("Done! Files saved: data_out.json, mini_data_out.json, preview_data_out.json, data_dictionary.md")
    logger.info(f"Final dataset: {merged_imputed.shape[0]} observations, {merged_imputed.shape[1]} variables")

if __name__ == "__main__":
    main()
