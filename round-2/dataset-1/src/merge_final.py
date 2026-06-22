#!/usr/bin/env python3
"""Merge OWID datasets - corrected version."""

from loguru import logger
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import json

logger.remove()
logger.add(lambda msg: print(msg, end=""), level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

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
    transition = vdem_1990s[vdem_1990s['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    vdem_1989 = vdem[vdem['Year'] == 1989]
    pre_dem = vdem_1989[vdem_1989['v2x_polyarchy'] > 0.5]['Entity'].unique()
    
    post1990 = [c for c in transition if c not in pre_dem]
    logger.info("Found %d post-1990 democratizers", len(post1990))
    
    # Filter to 1990-2022
    logger.info("Filtering to 1990-2022...")
    gini = gini[gini['Entity'].isin(post1990) & gini['Year'].between(1990, 2022)].copy()
    vdem = vdem[vdem['Entity'].isin(post1990) & vdem['Year'].between(1990, 2022)].copy()
    edu = edu[edu['Entity'].isin(post1990) & edu['Year'].between(1990, 2022)].copy()
    social = social[social['Entity'].isin(post1990) & social['Year'].between(1990, 2022)].copy()
    
    # Merge
    logger.info("Merging datasets...")
    merged = gini[['Entity', 'Code', 'Year', 'gini']].merge(
        vdem[['Entity', 'Code', 'Year', 'v2x_polyarchy', 'region']],
        on=['Entity', 'Code', 'Year'], how='outer'
    ).merge(
        edu[['Entity', 'Code', 'Year', 'education']],
        on=['Entity', 'Code', 'Year'], how='outer'
    ).merge(
        social[['Entity', 'Code', 'Year', 'social_spending']],
        on=['Entity', 'Code', 'Year'], how='outer'
    )
    
    logger.info("Merged shape: %s", str(merged.shape))
    logger.info("Missing values:\n%s", str(merged.isnull().sum()))
    
    # Region dummies
    merged['region'] = merged['region'].fillna('Unknown')
    dummies = pd.get_dummies(merged['region'], prefix='region')
    merged = pd.concat([merged, dummies], axis=1)
    
    # MICE imputation
    logger.info("Running MICE imputation...")
    impute_vars = ['gini', 'v2x_polyarchy', 'education', 'social_spending']
    X = merged[impute_vars].copy()
    
    bounds = {'gini': (0, 1), 'v2x_polyarchy': (0, 1), 'education': (0, 20), 'social_spending': (0, 50)}
    
    imputer = IterativeImputer(max_iter=50, random_state=42, sample_posterior=True)
    X_imp = imputer.fit_transform(X)
    
    merged_imp = merged.copy()
    for i, var in enumerate(impute_vars):
        merged_imp[var] = np.clip(X_imp[:, i], bounds[var][0], bounds[var][1])
    
    # Save
    logger.info("Saving datasets...")
    merged_imp = merged_imp.rename(columns={'Entity': 'country', 'Code': 'country_code', 'Year': 'year'})
    merged_imp.to_json('data_out.json', orient='records', lines=True)
    
    mini_countries = post1990[:3] if len(post1990) >= 3 else post1990
    mini = merged_imp[merged_imp['country'].isin(mini_countries)]
    mini.to_json('mini_data_out.json', orient='records', lines=True)
    
    merged_imp.head(3).to_json('preview_data_out.json', orient='records', lines=True)
    
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
        f.write("- education (years), social_spending (pct GDP)\n\n")
        f.write("## Countries (N=%d)\n" % len(post1990))
        for c in sorted(post1990):
            f.write("- %s\n" % c)
    
    logger.info("Done! Final dataset: %d observations", merged_imp.shape[0])
    logger.info("Gini range: %.3f - %.3f", merged_imp['gini'].min(), merged_imp['gini'].max())

if __name__ == "__main__":
    main()
