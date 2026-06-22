#!/usr/bin/env python3
"""Run panel regressions for the Triple Shield hypothesis."""
import json, sys, os
import warnings
warnings.filterwarnings('ignore')

# Install required packages if needed
try:
    import pandas as pd
    import numpy as np
    from linearmodels.panel import PanelOLS
    from linearmodels.panel.results import PanelResults
    import statsmodels.api as sm
except ImportError:
    os.system('pip3 install pandas numpy linearmodels statsmodels -q')
    import pandas as pd
    import numpy as np
    from linearmodels.panel import PanelOLS
    from linearmodels.panel.results import PanelResults
    import statsmodels.api as sm

print("Loading data...")

# Load data
with open('temp/datasets/full_panel_final.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Set entity and time indexes
df['entity_id'] = df['Code']
df['time_id'] = df['Year']
df = df.set_index(['entity_id', 'time_id'])

print(f"\nSummary statistics (before dropping NAs):")
print(df[['vdem_electoral', 'gini', 'education_years', 'social_spending']].describe())

print(f"\nMissing values:")
print(df[['vdem_electoral', 'gini', 'education_years', 'social_spending']].isnull().sum())

# Create analysis sample - drop rows with missing on key variables
analysis_vars = ['vdem_electoral', 'gini', 'education_years', 'social_spending']
df_analysis = df.dropna(subset=analysis_vars)
print(f"\nAnalysis sample (complete cases on 4 key vars): {df_analysis.shape[0]} observations")

if df_analysis.shape[0] > 0:
    print(f"\nSummary stats (analysis sample):")
    print(df_analysis[analysis_vars].describe())
    
    # Correlation matrix
    print(f"\nCorrelation matrix:")
    print(df_analysis[analysis_vars].corr())
    
    # Save analysis sample for further use
    df_analysis.reset_index().to_json('analysis_sample.json', orient='records')
    print("\nSaved analysis sample to analysis_sample.json")
else:
    print("\nNot enough complete cases - need to use all available data with FEs")
