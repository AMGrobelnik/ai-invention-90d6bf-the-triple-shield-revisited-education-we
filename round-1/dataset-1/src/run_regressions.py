#!/usr/bin/env python3
"""Run panel regressions for the Triple Shield hypothesis."""
import json, sys, os
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

print("Loading analysis sample...")
df = pd.read_json('analysis_sample.json', orient='records')

# Set entity and time indexes
df = df.set_index(['Code', 'Year'])

# Standardize variables for interpretation
vars_to_std = ['gini', 'education_years', 'social_spending', 'gdp_per_capita', 'resource_rents']
for v in vars_to_std:
    if v in df.columns:
        df[f'{v}_std'] = (df[v] - df[v].mean()) / df[v].std()

# Create interaction terms with standardized variables
df['gini_x_edu_std'] = df['gini_std'] * df['education_years_std']
df['gini_x_soc_std'] = df['gini_std'] * df['social_spending_std']
df['edu_x_soc_std'] = df['education_years_std'] * df['social_spending_std']
df['triple_std'] = df['gini_std'] * df['education_years_std'] * df['social_spending_std']

# Model 1: Simple main effects (FE only)
print("\n" + "="*60)
print("MODEL 1: Main effects only (FE)")
print("="*60)
from linearmodels.panel import PanelOLS
exog1 = pd.DataFrame({
    'gini_std': df['gini_std'],
    'education_years_std': df['education_years_std'],
    'social_spending_std': df['social_spending_std'],
    'gdp_per_capita_std': df['gdp_per_capita_std'],
    'resource_rents_std': df['resource_rents_std'],
})
exog1 = sm.add_constant(exog1)
mod1 = PanelOLS(df['vdem_electoral'], exog1, entity_effects=True, time_effects=True)
res1 = mod1.fit(cov_type='clustered', cluster_entity=True)
print(res1.summary)

# Model 2: With two-way interactions
print("\n" + "="*60)
print("MODEL 2: Two-way interactions (FE)")
print("="*60)
exog2 = pd.DataFrame({
    'gini_std': df['gini_std'],
    'education_years_std': df['education_years_std'],
    'social_spending_std': df['social_spending_std'],
    'gdp_per_capita_std': df['gdp_per_capita_std'],
    'resource_rents_std': df['resource_rents_std'],
    'gini_x_edu_std': df['gini_x_edu_std'],
    'gini_x_soc_std': df['gini_x_soc_std'],
    'edu_x_soc_std': df['edu_x_soc_std'],
})
exog2 = sm.add_constant(exog2)
mod2 = PanelOLS(df['vdem_electoral'], exog2, entity_effects=True, time_effects=True)
res2 = mod2.fit(cov_type='clustered', cluster_entity=True)
print(res2.summary)

# Model 3: Triple interaction
print("\n" + "="*60)
print("MODEL 3: Triple interaction (FE)")
print("="*60)
exog3 = pd.DataFrame({
    'gini_std': df['gini_std'],
    'education_years_std': df['education_years_std'],
    'social_spending_std': df['social_spending_std'],
    'gdp_per_capita_std': df['gdp_per_capita_std'],
    'resource_rents_std': df['resource_rents_std'],
    'gini_x_edu_std': df['gini_x_edu_std'],
    'gini_x_soc_std': df['gini_x_soc_std'],
    'edu_x_soc_std': df['edu_x_soc_std'],
    'triple_std': df['triple_std'],
})
exog3 = sm.add_constant(exog3)
mod3 = PanelOLS(df['vdem_electoral'], exog3, entity_effects=True, time_effects=True)
res3 = mod3.fit(cov_type='clustered', cluster_entity=True)
print(res3.summary)

# Save results
results = {
    'model1_params': res1.params.to_dict(),
    'model1_pvalues': res1.pvalues.to_dict(),
    'model1_rsquared': res1.rsquared,
    'model2_params': res2.params.to_dict(),
    'model2_pvalues': res2.pvalues.to_dict(),
    'model2_rsquared': res2.rsquared,
    'model3_params': res3.params.to_dict(),
    'model3_pvalues': res3.pvalues.to_dict(),
    'model3_rsquared': res3.rsquared,
    'n_obs': int(res1.nobs),
    'n_entities': int(res1.entity_info['total']),
}
with open('regression_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved regression results to regression_results.json")
