#!/usr/bin/env python3
"""Download OWID datasets using CSV endpoints found in search results."""
import requests
import json
from pathlib import Path
import time
import pandas as pd
from loguru import logger
import sys

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/owid_csv_download.log", rotation="30 MB", level="DEBUG")

# OWID CSV data URLs (from search results - "Download full data" links)
DATASETS = {
    "vdem": {
        "name": "V-Dem Electoral Democracy",
        "url": "https://ourworldindata.org/grapher/electoral-democracy-index.csv",
        "description": "V-Dem v2x_polyarchy index"
    },
    "gini": {
        "name": "Gini Coefficient",
        "url": "https://ourworldindata.org/grapher/economic-inequality-gini-index.csv",
        "description": "Gini index before taxes"
    },
    "gini_aftertax": {
        "name": "Gini After Tax",
        "url": "https://ourworldindata.org/grapher/gini-coefficient-after-tax-lis.csv",
        "description": "Gini index after taxes"
    },
    "education": {
        "name": "Mean Years Schooling",
        "url": "https://ourworldindata.org/grapher/mean-years-of-schooling-long-run.csv",
        "description": "Barro-Lee education data"
    },
    "social_spending": {
        "name": "Social Spending OECD",
        "url": "https://ourworldindata.org/grapher/social-spending-oecd-longrun.csv",
        "description": "OECD social expenditure"
    },
    "gdp": {
        "name": "GDP Per Capita",
        "url": "https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv",
        "description": "World Bank GDP per capita"
    },
    "resource_rents": {
        "name": "Natural Resource Rents",
        "url": "https://ourworldindata.org/grapher/natural-resource-rents.csv",
        "description": "Total natural resource rents % GDP"
    },
    "population": {
        "name": "Population",
        "url": "https://ourworldindata.org/grapher/population.csv",
        "description": "Total population"
    },
}

def download_csv_dataset(name: str, info: dict, output_dir: Path) -> dict:
    """Download dataset from OWID CSV endpoint."""
    url = info['url']
    
    try:
        logger.info(f"Downloading {name} from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse CSV
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        
        # Save as JSON (full, mini, preview)
        safe_name = name.replace(' ', '_').lower()
        
        # Full: all data
        full_file = output_dir / f"full_{safe_name}.json"
        df.to_json(full_file, orient='records', indent=2)
        
        # Mini: first 3 rows
        mini_file = output_dir / f"mini_{safe_name}.json"
        df.head(3).to_json(mini_file, orient='records', indent=2)
        
        # Preview: mini with truncated strings
        preview_data = df.head(3).to_dict('records')
        preview_file = output_dir / f"preview_{safe_name}.json"
        preview_file.write_text(json.dumps(preview_data, indent=2))
        
        logger.info(f"✓ {name}: {len(df)} rows, {len(df.columns)} cols")
        logger.info(f"  Columns: {list(df.columns)}")
        logger.info(f"  Saved: {full_file}, {mini_file}, {preview_file}")
        
        return {
            "name": name,
            "status": "success",
            "rows": len(df),
            "columns": list(df.columns),
            "full_file": str(full_file),
            "mini_file": str(mini_file)
        }
        
    except Exception as e:
        logger.error(f"Failed {name}: {e}")
        return {"name": name, "status": "failed", "error": str(e)}

@logger.catch(reraise=True)
def main():
    output_dir = Path("temp/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting CSV download of {len(DATASETS)} OWID datasets")
    
    results = []
    for name, info in DATASETS.items():
        result = download_csv_dataset(name, info, output_dir)
        results.append(result)
        time.sleep(0.5)
    
    # Save summary
    summary_file = output_dir / "csv_download_summary.json"
    summary_file.write_text(json.dumps(results, indent=2))
    
    successful = sum(1 for r in results if r['status'] == 'success')
    logger.info(f"Download complete: {successful}/{len(DATASETS)} successful")
    
    return results

if __name__ == "__main__":
    main()
