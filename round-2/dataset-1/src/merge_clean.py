#!/usr/bin/env python3
"""Merge OWID datasets and create panel for post-1990 democratizers with MICE imputation."""

from loguru import logger
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
    
    # Rename columns
    gini = gini.rename(columns={'Gini coefficient': 'gini', 'World region according to OWID': 'region'})
    vdem = vdem.rename(columns={'Electoral democracy index': 'v2x_polyarchy', 'World region according to OWID': 'region'})
    edu = edu.rename(columns={'Average years of schooling': 'education'})
    social = social.rename(columns={'Public social expenditure as a share of GDP': 'social_spending'})
    
    # Identify post-1990 democratizers
    logger.info("Identifying post-1990 democratizers...")
    vdem_1990s = vdem[(vdem['Year'] >= 1990) & (vdem['Year'] <= 1999)]
    transition_countries = vdem_1990s[vdem_1990s['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    vdem_1989 = vdem[vdem['Year'] == 1989]
    pre1990_democracies = vdem_1989[vdem_1989['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    post1990_democratizers = [c for c in transition_countries if c not in pre1990_democracies]
    logger.info(f"Found {len(post1990_democratizers)} post-1990 democratizers")
    
    # Filter to 1990-2022 and post-1990 democratizers
    logger.info("Filtering datasets to 1990-2022...")
    gini = gini[gini['Entity'].isin(post1990_democratizers) & gini['Year'].between(1990, 2022)].copy()
    vdem = vdem[vdem['Entity'].isin(post1990_democratizers) & vdem['Year'].between(1990, 2022)].copy()
    edu = edu[edu['Entity'].isin(post1990_democratizers) & edu['Year'].between(1990, 2022)].copy()
    social = social[social['Entity'].isin(post1990_democratizers) & social['Year'].between(1990, 2022)].copy()
    
    # Merge datasets
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
    
    logger.info(f"Merged shape: {merged.shape}")
    logger.info(f"Missing values:\n{merged.isnull().sum()}")
    
    # Create region dummies
    merged['region'] = merged['region'].fillna('Unknown')
    region_dummies = pd.get_dummies(merged['region'], prefix='region')
    merged = pd.concat([merged, region_dummies], axis=1)
    
    # MICE imputation with bounds
    logger.info("Running MICE imputation...")
    impute_vars = ['gini', 'v2x_polyarchy', 'education', 'social_spending']
    X = merged[impute_vars].copy()
    
    bounds = {'gini': (0, 1), 'v2x_polyarchy': (0, 1), 'education': (0, 20), 'social_spending': (0, 50)}
    
    imputer = IterativeImputer(max_iter=50, random_state=42, sample_posterior=True)
    X_imputed = imputer.fit_transform(X)
    
    merged_imputed = merged.copy()
    for i, var in enumerate(impute_vars):
        merged_imputed[var] = np.clip(X_imputed[:, i], bounds[var][0], bounds[var][1])
    
    # Save outputs
    logger.info("Saving datasets...")
    merged_imputed = merged_imputed.rename(columns={'Entity': 'country', 'Code': 'country_code', 'Year': 'year'})
    merged_imputed.to_json('data_out.json', orient='records', lines=True)
    
    mini_countries = post1990_democratizers[:3] if len(post1990_democratizers) >= 3 else post1990_democratizers
    merged_imputed[merged_imputed['country'].isin(mini_countries)].to_json('mini_data_out.json', orient='records', lines=True)
    merged_imputed.head(3).to_json('preview_data_out.json', orient='records', lines=True)
    
    # Data dictionary
    with open('data_dictionary.md', 'w') as f:
        f.write("# Data Dictionary: Post-1990 Democratizers Panel (1990-2022)\n\n")
        f.write("## Sources\n")
        f.write("- Gini: World Bank PIP (OWID)\n")
        f.write("- V-Dem: V-Dem v13 (OWID)\n")
        f.write("- Education: Barro and Lee (OWID)\n")
        f.write("- Social spending: OECD (OWID)\n\n")
        f.write("## Variables\n")
        f.write("- country, country_code, year\n")
        f.write("- gini (0-1), v2x_polyarchy (0-1)\n")
        f.write("- education (years), social_spending (% GDP)\n\n")
        f.write(f"## Countries (N={len(post1990_democratizers)})\n")
        for c in sorted(post1990_democratizers):
            f.write(f"- {c}\n")
    
    logger.info(f"Done! Final dataset: {merged_imputed.shape[0]} observations")
    logger.info(f"Gini range: {merged_imputed['gini'].min():.3f} - {merged_imputed['gini'].max():.3f}")

if __name__ == "__main__":
    main()
