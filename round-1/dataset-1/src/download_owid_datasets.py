#!/usr/bin/env python3
"""Download OWID datasets for triple shield hypothesis analysis."""
import requests
import json
from pathlib import Path
import time
from loguru import logger
import sys

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/owid_download.log", rotation="30 MB", level="DEBUG")

# OWID dataset endpoints (slug -> description)
DATASETS = {
    "electoral-democracy-index-v-dem": {
        "name": "V-Dem Electoral Democracy Index",
        "variable": "vdem_electoral",
        "description": "V-Dem v2x_polyarchy index (0-1) measuring electoral democracy"
    },
    "gini-index-worldbank": {
        "name": "Gini Index (World Bank)",
        "variable": "gini_wb",
        "description": "Gini coefficient before taxes (0-100 scale)"
    },
    "gini-index-after-taxes-and-transfers": {
        "name": "Gini After Taxes and Transfers",
        "variable": "gini_aftertax",
        "description": "Gini coefficient after taxes and transfers (0-100 scale)"
    },
    "mean-years-of-schooling": {
        "name": "Mean Years of Schooling",
        "variable": "education",
        "description": "Average years of schooling in population aged 25+"
    },
    "social-protection-spending-oecd": {
        "name": "Social Protection Spending (OECD)",
        "variable": "social_protection",
        "description": "Social protection expenditure as % of GDP"
    },
    "gdp-per-capita-worldbank": {
        "name": "GDP Per Capita (World Bank)",
        "variable": "gdp_per_capita",
        "description": "GDP per capita in constant 2015 US$"
    },
    "population": {
        "name": "Total Population",
        "variable": "population",
        "description": "Total population"
    },
    "natural-resource-rents": {
        "name": "Natural Resource Rents",
        "variable": "resource_rents",
        "description": "Total natural resource rents as % of GDP"
    },
}

def download_owid_dataset(slug: str, output_dir: Path) -> dict:
    """Download OWID dataset via grapher JSON endpoint."""
    url = f"https://ourworldindata.org/grapher/{slug}.json"
    
    try:
        logger.info(f"Downloading {slug} from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Save full dataset
        output_file = output_dir / f"full_{slug.replace('-', '_')}.json"
        output_file.write_text(json.dumps(data, indent=2))
        
        # Extract and save mini version (first 3 countries)
        if 'chart' in data and 'data' in data['chart']:
            chart_data = data['chart']['data']
            mini_data = {
                "name": slug,
                "variables": data.get('chart', {}).get('variableIds', []),
                "sample": chart_data[:3] if isinstance(chart_data, list) else []
            }
            mini_file = output_dir / f"mini_{slug.replace('-', '_')}.json"
            mini_file.write_text(json.dumps(mini_data, indent=2))
            logger.info(f"Saved {slug}: full={output_file}, mini={mini_file}")
        
        return {"slug": slug, "status": "success", "file": str(output_file)}
        
    except Exception as e:
        logger.error(f"Failed to download {slug}: {e}")
        return {"slug": slug, "status": "failed", "error": str(e)}

@logger.catch(reraise=True)
def main():
    output_dir = Path("temp/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting download of {len(DATASETS)} OWID datasets")
    
    results = []
    for slug, info in DATASETS.items():
        result = download_owid_dataset(slug, output_dir)
        results.append(result)
        time.sleep(1)  # Rate limiting
    
    # Save download summary
    summary_file = output_dir / "download_summary.json"
    summary_file.write_text(json.dumps(results, indent=2))
    
    successful = sum(1 for r in results if r['status'] == 'success')
    logger.info(f"Download complete: {successful}/{len(DATASETS)} successful")
    
    return results

if __name__ == "__main__":
    main()
