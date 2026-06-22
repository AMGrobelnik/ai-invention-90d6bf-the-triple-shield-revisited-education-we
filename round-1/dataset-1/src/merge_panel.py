#!/usr/bin/env python3
"""Final panel merge - working version."""
import json
from pathlib import Path
import pandas as pd
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

# Post-1990 democratizers
COUNTRIES = [
    "ALB", "ARM", "AZE", "BLR", "BEN", "BIH", "BWA", "BGR", "CPV", "HRV",
    "CZE", "EST", "GEO", "GHA", "GTM", "HTI", "HUN", "IDN", "KAZ", "KGZ",
    "LVA", "LTU", "MDG", "MWI", "MLI", "MDA", "MNG", "MNE", "MOZ", "NAM",
    "MKD", "PRY", "PER", "PHL", "POL", "ROU", "RUS", "STP", "SEN", "SRB",
    "SVK", "SVN", "ZAF", "TJK", "TZA", "THA", "TKM", "UKR", "UZB", "ZMB"
]

@logger.catch(reraise=True)
def main():
    tables_dir = Path("temp/tables")
    output_dir = Path("temp/datasets")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load and rename OWID datasets
    logger.info("Loading OWID datasets...")
    
    vdem = pd.read_json(tables_dir / "full_vdem.json", orient='records')
    vdem = vdem.rename(columns={'Electoral democracy index': 'vdem_electoral'})
    
    gini = pd.read_json(tables_dir / "full_gini.json", orient='records')
    gini = gini.rename(columns={'Gini coefficient': 'gini'})
    
    edu = pd.read_json(tables_dir / "full_education.json", orient='records')
    edu = edu.rename(columns={'Average years of schooling': 'education_years'})
    
    social = pd.read_json(tables_dir / "full_social_spending.json", orient='records')
    social = social.rename(columns={'Public social expenditure as a share of GDP': 'social_spending'})
    
    gdp = pd.read_json(tables_dir / "full_gdp.json", orient='records')
    gdp = gdp.rename(columns={'GDP per capita': 'gdp_per_capita'})
    
    pop = pd.read_json(tables_dir / "full_population.json", orient='records')
    pop = pop.rename(columns={'Population': 'population'})
    
    resource = pd.read_json(tables_dir / "full_resource_rents.json", orient='records')
    resource = resource.rename(columns={'Total natural resources rents (% of GDP)': 'resource_rents'})
    
    # Merge OWID datasets
    logger.info("Merging OWID datasets...")
    owid = vdem
    for df in [gini, edu, social, gdp, pop, resource]:
        owid = pd.merge(owid, df, on=['Entity', 'Code', 'Year'], how='outer')
    
    logger.info(f"OWID shape: {owid.shape}")
    
    # Load WB data
    logger.info("Loading World Bank data...")
    wb = pd.read_json(tables_dir / "wb_panel_data.json", orient='records')
    wb = wb.rename(columns={'country_code': 'Code', 'year': 'Year'})
    
    # Merge OWID with WB
    logger.info("Merging OWID + WB...")
    merged = pd.merge(owid, wb, on=['Code', 'Year'], how='left')
    
    # Filter to post-1990 democratizers
    merged = merged[merged['Code'].isin(COUNTRIES)]
    merged = merged[merged['Year'].between(1990, 2022)]
    logger.info(f"After filtering: {merged.shape}")
    
    # Clean variables
    logger.info("Cleaning variables...")
    merged['vdem_electoral'] = pd.to_numeric(merged['vdem_electoral'], errors='coerce')
    
    # Use OWID vars, fill with WB if missing
    if 'gini_wb' in merged.columns:
        merged['gini'] = merged['gini'].fillna(merged['gini_wb'])
    merged['gini'] = pd.to_numeric(merged['gini'], errors='coerce')
    
    if 'education_years_wb' in merged.columns:
        merged['education_years'] = merged['education_years'].fillna(merged['education_years_wb'])
    merged['education_years'] = pd.to_numeric(merged['education_years'], errors='coerce')
    
    if 'social_spending_wb' in merged.columns:
        merged['social_spending'] = merged['social_spending'].fillna(merged['social_spending_wb'])
    merged['social_spending'] = pd.to_numeric(merged['social_spending'], errors='coerce')
    
    if 'gdp_per_capita_wb' in merged.columns:
        merged['gdp_per_capita'] = merged['gdp_per_capita'].fillna(merged['gdp_per_capita_wb'])
    merged['gdp_per_capita'] = pd.to_numeric(merged['gdp_per_capita'], errors='coerce')
    
    if 'population_wb' in merged.columns:
        merged['population'] = merged['population'].fillna(merged['population_wb'])
    merged['population'] = pd.to_numeric(merged['population'], errors='coerce')
    
    merged['resource_rents'] = pd.to_numeric(merged['resource_rents'], errors='coerce')
    
    # Drop rows missing outcome
    merged = merged.dropna(subset=['vdem_electoral'])
    logger.info(f"After dropping missing V-Dem: {merged.shape}")
    
    # Create interaction terms
    merged['gini_x_education'] = merged['gini'] * merged['education_years']
    merged['gini_x_social'] = merged['gini'] * merged['social_spending']
    merged['triple_interaction'] = merged['gini'] * merged['education_years'] * merged['social_spending']
    
    # Select analysis variables
    analysis_vars = [
        'Entity', 'Code', 'Year', 'vdem_electoral', 'gini', 'education_years',
        'social_spending', 'gdp_per_capita', 'resource_rents', 'population',
        'gini_x_education', 'gini_x_social', 'triple_interaction'
    ]
    available_vars = [v for v in analysis_vars if v in merged.columns]
    final_df = merged[available_vars].copy()
    
    # Save dataset
    logger.info("Saving final dataset...")
    final_df.to_json(output_dir / "full_panel_final.json", orient='records', indent=2)
    final_df.head(3).to_json(output_dir / "mini_panel_final.json", orient='records', indent=2)
    final_df.head(3).to_json(output_dir / "preview_panel_final.json", orient='records', indent=2)
    
    # Data dictionary
    data_dict = {
        "n_countries": len(final_df['Code'].unique()),
        "n_observations": len(final_df),
        "years": str(final_df['Year'].min()) + "-" + str(final_df['Year'].max()),
        "variables": list(final_df.columns)
    }
    (output_dir / "data_dictionary_final.json").write_text(json.dumps(data_dict, indent=2))
    
    logger.info(f"Final dataset: {final_df.shape}")
    logger.info(f"Countries: {data_dict['n_countries']}")
    logger.info(f"Years: {data_dict['years']}")
    
    return final_df

if __name__ == "__main__":
    result = main()
    logger.info("Done!")
