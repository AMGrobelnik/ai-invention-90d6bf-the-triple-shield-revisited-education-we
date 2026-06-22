#!/usr/bin/env python3
"""Merge OWID datasets into panel format for triple shield hypothesis."""
import json
from pathlib import Path
import pandas as pd
from loguru import logger
import sys

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/data_merge.log", rotation="30 MB", level="DEBUG")

# Post-1990 democratizers list (from artifact plan)
POST_1990_DEMOCRATIZERS = [
    # Eastern Europe/CIS
    "POL", "CZE", "SVK", "HUN", "EST", "LVA", "LTU", "SVN", "HRV", "ROU", 
    "BGR", "ALB", "MKD", "SRB", "MNE", "BIH", "UKR", "BLR", "MDA", "RUS", 
    "ARM", "GEO", "AZE", "KAZ", "KGZ", "UZB", "TKM", "TJK",
    # Latin America
    "PER", "GTM", "PRY", "HTI",
    # Africa
    "BEN", "BWA", "CPV", "GHA", "MWI", "MLI", "NAM", "STP", "SEN", "ZAF", 
    "ZMB", "MDG", "MOZ", "TZA",
    # Asia
    "MNG", "PHL", "THA", "IDN"
]

def load_json_as_df(file_path: Path) -> pd.DataFrame:
    """Load JSON file and return as DataFrame."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

@logger.catch(reraise=True)
def main():
    tables_dir = Path("temp/tables")
    
    # Load all datasets
    logger.info("Loading datasets...")
    vdem = load_json_as_df(tables_dir / "full_vdem.json")
    gini = load_json_as_df(tables_dir / "full_gini.json")
    gini_aftertax = load_json_as_df(tables_dir / "full_gini_aftertax.json")
    education = load_json_as_df(tables_dir / "full_education.json")
    social = load_json_as_df(tables_dir / "full_social_spending.json")
    gdp = load_json_as_df(tables_dir / "full_gdp.json")
    resource = load_json_as_df(tables_dir / "full_resource_rents.json")
    population = load_json_as_df(tables_dir / "full_population.json")
    
    # Rename columns to standard names
    logger.info("Standardizing column names...")
    vdem = vdem.rename(columns={'Electoral democracy index': 'vdem_electoral'})
    gini = gini.rename(columns={'Gini coefficient': 'gini'})
    gini_aftertax = gini_aftertax.rename(columns={'Gini coefficient (after tax)': 'gini_aftertax'})
    education = education.rename(columns={'Average years of schooling': 'education_years'})
    social = social.rename(columns={'Public social expenditure as a share of GDP': 'social_spending_gdp'})
    gdp = gdp.rename(columns={'GDP per capita': 'gdp_per_capita'})
    resource = resource.rename(columns={'Total natural resources rents (% of GDP)': 'resource_rents_gdp'})
    population = population.rename(columns={'Population': 'population'})
    
    # Merge all datasets on Entity, Code, Year
    logger.info("Merging datasets...")
    dfs = [vdem, gini, gini_aftertax, education, social, gdp, resource, population]
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on=['Entity', 'Code', 'Year'], how='outer')
    
    logger.info(f"Merged shape: {merged.shape}")
    logger.info(f"Columns: {list(merged.columns)}")
    
    # Filter to post-1990 democratizers
    logger.info("Filtering to post-1990 democratizers (1990-2022)...")
    merged = merged[merged['Code'].isin(POST_1990_DEMOCRATIZERS)]
    merged = merged[merged['Year'].between(1990, 2022)]
    
    logger.info(f"After filtering: {merged.shape}")
    
    # Check missing data
    logger.info("Checking missing data...")
    missing = merged.isnull().sum()
    missing_pct = (missing / len(merged) * 100).round(2)
    missing_summary = pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})
    logger.info(f"Missing data:\n{missing_summary[missing_summary['missing_count'] > 0]}")
    
    # Save merged dataset
    output_dir = Path("temp/datasets")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Full dataset
    full_file = output_dir / "full_panel_data.json"
    merged.to_json(full_file, orient='records', indent=2)
    logger.info(f"Saved full dataset: {full_file}")
    
    # Mini dataset (first 3 rows)
    mini_file = output_dir / "mini_panel_data.json"
    merged.head(3).to_json(mini_file, orient='records', indent=2)
    logger.info(f"Saved mini dataset: {mini_file}")
    
    # Preview dataset (mini with truncated strings)
    preview_file = output_dir / "preview_panel_data.json"
    merged.head(3).to_json(preview_file, orient='records', indent=2)
    logger.info(f"Saved preview dataset: {preview_file}")
    
    # Save data dictionary
    data_dict = {
        "description": "OWID Panel Data for Triple Shield Hypothesis",
        "variables": list(merged.columns),
        "time_period": "1990-2022",
        "countries": merged['Code'].unique().tolist(),
        "n_countries": len(merged['Code'].unique()),
        "n_observations": len(merged),
        "missing_data": missing_summary[missing_summary['missing_count'] > 0].to_dict('records')
    }
    dict_file = output_dir / "data_dictionary.json"
    dict_file.write_text(json.dumps(data_dict, indent=2))
    logger.info(f"Saved data dictionary: {dict_file}")
    
    return merged

if __name__ == "__main__":
    result = main()
    logger.info(f"Final dataset: {result.shape}")
