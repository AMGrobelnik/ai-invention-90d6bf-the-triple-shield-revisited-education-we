#!/usr/bin/env python3
"""Download OWID datasets using correct grapher endpoints."""
import requests
import json
from pathlib import Path
import time
from loguru import logger
import sys

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/owid_download_v2.log", rotation="30 MB", level="DEBUG")

# Correct OWID grapher slugs found via web search
DATASETS = {
    "electoral-democracy-index": "V-Dem Electoral Democracy Index",
    "economic-inequality-gini-index": "Gini Coefficient (before tax)",
    "gini-coefficient-after-tax-lis": "Gini Coefficient (after tax)",
    "mean-years-of-schooling-long-run": "Mean Years of Schooling (Barro-Lee)",
    "social-spending-oecd-longrun": "Social Protection Spending (% GDP)",
    "gdp-per-capita-worldbank": "GDP Per Capita (World Bank)",
    "natural-resource-rents": "Natural Resource Rents (% GDP)",
    "population": "Total Population",
    "years-of-schooling": "Years of Schooling (all levels)",
}

def download_owid_json(slug: str, output_dir: Path) -> dict:
    """Download OWID dataset via grapher JSON API."""
    # Try multiple URL patterns
    urls = [
        f"https://ourworldindata.org/grapher/{slug}.json",
        f"https://ourworldindata.org/{slug}.json",
    ]
    
    for url in urls:
        try:
            logger.info(f"Trying {url}")
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                # Save full dataset
                safe_slug = slug.replace('-', '_').replace('/', '_')
                output_file = output_dir / f"full_{safe_slug}.json"
                output_file.write_text(json.dumps(data, indent=2))
                
                # Create mini version
                mini_data = {
                    "slug": slug,
                    "url": url,
                    "keys": list(data.keys())[:10] if isinstance(data, dict) else "list"
                }
                if isinstance(data, dict):
                    if 'chart' in data and 'data' in data.get('chart', {}):
                        chart_data = data['chart']['data']
                        mini_data['sample_rows'] = chart_data[:3] if isinstance(chart_data, list) else []
                        mini_data['total_rows'] = len(chart_data) if isinstance(chart_data, list) else 'unknown'
                
                mini_file = output_dir / f"mini_{safe_slug}.json"
                mini_file.write_text(json.dumps(mini_data, indent=2))
                
                logger.info(f"✓ Downloaded {slug}: {len(str(data))} bytes")
                return {"slug": slug, "status": "success", "file": str(output_file), "url": url}
        
        except Exception as e:
            logger.warning(f"Failed {url}: {e}")
            continue
    
    return {"slug": slug, "status": "failed", "error": "All URL patterns failed"}

@logger.catch(reraise=True)
def main():
    output_dir = Path("temp/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting download of {len(DATASETS)} OWID datasets")
    
    results = []
    for slug, description in DATASETS.items():
        logger.info(f"Dataset: {description}")
        result = download_owid_json(slug, output_dir)
        results.append(result)
        time.sleep(0.5)  # Rate limiting
    
    # Save summary
    summary_file = output_dir / "download_summary_v2.json"
    summary_file.write_text(json.dumps(results, indent=2))
    
    successful = sum(1 for r in results if r['status'] == 'success')
    logger.info(f"Download complete: {successful}/{len(DATASETS)} successful")
    
    return results

if __name__ == "__main__":
    main()
