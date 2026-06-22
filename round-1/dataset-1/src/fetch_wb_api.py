#!/usr/bin/env python3
"""Fetch data from World Bank API for Gini, education, GDP, population."""
import requests
import json
from pathlib import Path
import time
from loguru import logger
import sys
import pandas as pd

# Setup logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/wb_api.log", rotation="30 MB", level="DEBUG")

# World Bank indicators
WB_INDICATORS = {
    "gini": "SI.POV.GINI",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "population": "SP.POP.TOTL",
    "education_years": "SE.SEC.DURS",
    "social_spending": "SE.XPD.TOTL.GD.ZS",
}

def fetch_wb_data(indicator: str, country_codes: list, start_year: int = 1990, end_year: int = 2022):
    """Fetch data from World Bank API."""
    countries_str = ";".join(country_codes)
    url = f"https://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator}"
    
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 1000
    }
    
    try:
        logger.info(f"Fetching {indicator} for {len(country_codes)} countries")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, list) and len(data) > 1:
            records = data[1]
            logger.info(f"  Retrieved {len(records)} records")
            return {"indicator": indicator, "records": records}
        else:
            logger.warning(f"  No data returned for {indicator}")
            return {"indicator": indicator, "records": []}
            
    except Exception as e:
        logger.error(f"Failed to fetch {indicator}: {e}")
        return {"indicator": indicator, "error": str(e), "records": []}

@logger.catch(reraise=True)
def main():
    output_dir = Path("temp/tables")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    countries = [
        "ALB", "ARM", "AZE", "BLR", "BEN", "BIH", "BWA", "BGR", "CPV", "HRV",
        "CZE", "EST", "GEO", "GHA", "GTM", "HTI", "HUN", "IDN", "KAZ", "KGZ",
        "LVA", "LTU", "MDG", "MWI", "MLI", "MDA", "MNG", "MNE", "MOZ", "NAM",
        "MKD", "PRY", "PER", "PHL", "POL", "ROU", "RUS", "STP", "SEN", "SRB",
        "SVK", "SVN", "ZAF", "TJK", "TZA", "THA", "TKM", "UKR", "UZB", "ZMB"
    ]
    
    logger.info(f"Fetching World Bank data for {len(countries)} countries (1990-2022)")
    
    results = {}
    for name, indicator in WB_INDICATORS.items():
        result = fetch_wb_data(indicator, countries)
        results[name] = result
        time.sleep(1)
    
    output_file = output_dir / "wb_api_data.json"
    output_file.write_text(json.dumps(results, indent=2))
    logger.info(f"Saved World Bank data to {output_file}")
    
    # Process into panel format
    logger.info("Processing World Bank data into panel format...")
    all_records = []
    
    for name, result in results.items():
        if 'records' in result and result['records']:
            for record in result['records']:
                country_code = record.get('countryiso3code', '')
                year = record.get('date', '')
                value = record.get('value', None)
                
                if country_code and year and value is not None:
                    all_records.append({
                        'country_code': country_code,
                        'year': int(year),
                        name: float(value)
                    })
    
    if all_records:
        df = pd.DataFrame(all_records)
        logger.info(f"Created dataframe with {len(df)} records")
        
        # Pivot to wide format
        df_pivot = df.pivot_table(index=['country_code', 'year'], aggfunc='first').reset_index()
        
        panel_file = output_dir / "wb_panel_data.json"
        df_pivot.to_json(panel_file, orient='records', indent=2)
        logger.info(f"Saved panel data: {panel_file}")
        logger.info(f"Shape: {df_pivot.shape}")
        logger.info(f"Columns: {list(df_pivot.columns)}")
    
    return results

if __name__ == "__main__":
    main()
