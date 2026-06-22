# gen_art_dataset_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_art`
> Run: `run_9gq-UFm593U6` — The Triple Shield Revisited: Education, Welfare State Institutions, and the Inequality-Democratic Resilience Link in Post-1990 Democratizers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_dataset_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-06-22 12:08:41 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx1
type: dataset
title: Correct Gini Scaling Error and Build Imputed Panel Dataset (1990-2022)
summary: >-
  Fix the Gini coefficient scaling error (mean=2.84 → 0.25-0.65 range), verify OWID variable availability, download corrected
  data from OWID and SWIID, apply Multiple Imputation by Chained Equations (MICE) with 50+ imputations, and export the corrected
  panel dataset with full/mini/preview variants and data dictionary. CRITICAL: The numeric variable IDs in the hypothesis
  (1014857, 1209753, 809139, 1210307) may not be standard OWID identifiers - they might be from V-Dem or another database.
  The executor must search by variable NAME, not ID.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: >-
  Balanced panel dataset (1990-2022) covering 50+ post-1990 democratizers with 4 key variables: (1) Gini coefficient (0-1
  scale, correctly scaled, values 0.25-0.65), (2) V-Dem Electoral Democracy Index (0-1 scale), (3) Mean years of schooling
  (continuous, 0-15 years), (4) Social protection spending (% GDP, 0-30%). All variables should have <30% missing data after
  MICE imputation. Dataset must be in long format (country-year observations), properly documented with variable definitions,
  sources, and the specific Gini scaling correction applied. Final file size must be under 300MB.
dataset_search_plan: "PHASE 1: IDENTIFY CORRECT DATA SOURCES (1 hour)\n\nSTEP 1.1: Verify OWID variable availability by searching\
  \ for VARIABLE NAMES (not IDs):\n- Use aii-owid-datasets skill to search for these variable names:\n  a. 'Gini coefficient'\
  \ or 'income inequality Gini'\n  b. 'V-Dem electoral democracy' or 'electoral democracy index'\n  c. 'mean years of schooling'\
  \ or 'schooling years'\n  d. 'social protection spending' or 'social expenditure'\n- IMPORTANT: The numeric IDs (1014857,\
  \ 1209753, 809139, 1210307) in the hypothesis are likely NOT OWID variable IDs. OWID uses path-based identifiers like 'grapher/inequality/2023-12-12/gini-coefficient'.\
  \ Search by name to find correct OWID paths.\n- Download mini/preview samples of each variable to verify data structure\
  \ and scaling.\n\nSTEP 1.2: Identify alternative data sources (in case OWID variables are unavailable):\n- SWIID (Standardized\
  \ World Income Inequality Database):\n  * URL: https://swiid.org/\n  * Direct download: https://swiid.org/data/swiid9_4.dta\
  \ (Stata format, readable with pandas.read_stata())\n  * Documentation: Check SWIID codebook for Gini variable names (typically\
  \ 'gini_disp' for disposable income, 'gini_mkt' for market income)\n- V-Dem (Varieties of Democracy):\n  * URL: https://v-dem.net/data/\n\
  \  * Direct CSV download: https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv\n  * Variable: 'v2x_egaldem'\
  \ (Electoral Democracy Index, 0-1 scale)\n- UNESCO Institute for Statistics:\n  * URL: http://data.uis.unesco.org/\n  *\
  \ API: http://data.uis.unesco.org/API/UNESCO/static/API-doc/\n  * Variable: Mean years of schooling (UIS statistic code:\
  \ 'ML.2.FSGOVT')\n- OECD Social Expenditure Database:\n  * URL: https://www.oecd.org/social/expenditure.htm\n  * API: https://stats.oecd.org/Index.aspx?DataSetCode=SOCX_AGG\n\
  \  * Variable: Social protection expenditure (% GDP)\n\nPHASE 2: DOWNLOAD AND MERGE DATA (1.5 hours)\n\nSTEP 2.1: Download\
  \ Gini coefficient data:\n- PRIMARY: Try OWID first (search 'Gini coefficient', download if available)\n- SECONDARY: Download\
  \ SWIID data:\n  ```python\n  import pandas as pd\n  swiid_url = 'https://swiid.org/data/swiid9_4.dta'\n  gini_df = pd.read_stata(swiid_url)\n\
  \  # Keep key columns: country, year, gini_disp (or gini_mkt)\n  ```\n- TERTIARY: Use World Bank PIP API:\n  ```python\n\
  \  import requests\n  # World Bank Gini API (indicator: SI.POV.GINI)\n  wb_url = 'https://api.worldbank.org/v2/country/all/indicator/SI.POV.GINI?format=json&per_page=1000'\n\
  \  response = requests.get(wb_url)\n  ```\n- Verify Gini scaling: Print descriptive statistics. Correct values should be\
  \ 0.25-0.65 (0-1 scale) or 25-65 (0-100 scale). If mean is 2.84, data is incorrectly scaled - apply fix: divide by 100 if\
  \ values are 20-70, or divide by 10 if values are 2-7.\n\nSTEP 2.2: Download V-Dem Electoral Democracy Index:\n- PRIMARY:\
  \ Download from V-Dem direct CSV link (https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv)\n- Filter\
  \ columns: 'country_name', 'year', 'v2x_egaldem'\n- Verify scale: Should be 0-1 (if not, check V-Dem codebook - may need\
  \ rescaling)\n\nSTEP 2.3: Download education data (Mean years of schooling):\n- PRIMARY: OWID search 'mean years of schooling'\n\
  - SECONDARY: UNESCO API or World Bank EdStats (indicator: SE.SEC.NENR)\n\nSTEP 2.4: Download social protection spending:\n\
  - PRIMARY: OWID search 'social protection spending'\n- SECONDARY: OECD Social Expenditure Database (for OECD members) or\
  \ ILO ILOSTAT\n\nSTEP 2.5: Merge all datasets:\n- Use country-year as merge key\n- Harmonize country names (create mapping\
  \ dictionary for different spellings)\n- Restrict to years 1990-2022\n\nPHASE 3: IDENTIFY POST-1990 DEMOCRATIZERS (30 min)\n\
  \nSTEP 3.1: Define inclusion criteria:\n- Countries with V-Dem Electoral Democracy Index > 0.5 in any year 1990-1999 (transition\
  \ to democracy)\n- Countries that remained sovereign through 2022 (exclude dissolved states like USSR, Yugoslavia)\n- Exclude\
  \ established democracies pre-1990 (V-Dem > 0.5 in 1989)\n\nSTEP 3.2: Create country list programmatically:\n```python\n\
  # Pseudo-code for identifying post-1990 democratizers\nvdem_df = pd.read_csv('vdem_data.csv')\ntransition_countries = vdem_df[\n\
  \    (vdem_df['year'].between(1990, 1999)) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n]['country_name'].unique()\n\n# Exclude\
  \ pre-1990 democracies\npre1990_democracies = vdem_df[\n    (vdem_df['year'] == 1989) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n\
  ]['country_name'].unique()\n\npost1990_democratizers = [c for c in transition_countries if c not in pre1990_democracies]\n\
  ```\n\nSTEP 3.3: Expected country list (~50-70 countries):\n- Post-communist: Poland, Czech Republic, Slovakia, Hungary,\
  \ Estonia, Latvia, Lithuania, Slovenia, Croatia, Romania, Bulgaria, Albania, N. Macedonia, Serbia, Montenegro, Bosnia, Ukraine,\
  \ Belarus, Moldova, Russia, Armenia, Georgia, Azerbaijan, Kazakhstan, Kyrgyzstan, Uzbekistan, Mongolia\n- Africa: South\
  \ Africa (1994), Ghana, Kenya, Malawi, Mali, Niger, Senegal, Zambia, Benin, Cape Verde, Mali, Madagascar, Tanzania\n- Asia:\
  \ Indonesia (1998), Philippines, Thailand, Taiwan, South Korea (check transition year)\n- Latin America: (few, most transitioned\
  \ pre-1990)\n\nPHASE 4: APPLY MULTIPLE IMPUTATION BY CHAINED EQUATIONS (2 hours)\n\nSTEP 4.1: Install required libraries:\n\
  ```bash\nuv pip install miceforest scikit-learn statsmodels openpyxl\n```\n\nSTEP 4.2: Prepare data for imputation:\n- Combine\
  \ all variables into single DataFrame (country, year, Gini, V-Dem, education, social_spending)\n- Add auxiliary variables\
  \ to improve imputation: GDP per capita, population, region dummies\n- Create dummy variables for regions (Europe, Africa,\
  \ Asia, Latin America)\n- Ensure all variables are numeric (no strings except country/year)\n\nSTEP 4.3: Run MICE using\
  \ miceforest (preferred for speed):\n```python\nimport miceforest as mf\nimport pandas as pd\nimport numpy as np\n\n# Load\
  \ data\ndf = pd.read_csv('merged_panel.csv')\n\n# Define variables to impute\nimpute_vars = ['gini', 'v2x_egaldem', 'education',\
  \ 'social_spending', \n               'gdp_per_capita', 'population']\n\n# Initialize MICE kernel\nkernel = mf.ImputationKernel(\n\
  \    data=df[impute_vars + ['country', 'year', 'region_europe', 'region_africa', 'region_asia']],\n    variable_schema={\n\
  \        'gini': impute_vars,\n        'v2x_egaldem': impute_vars,\n        'education': impute_vars,\n        'social_spending':\
  \ impute_vars\n    },\n    datasets=50,  # Number of imputed datasets\n    save_all_iterations=True\n)\n\n# Run MICE iterations\n\
  kernel.mice(5)  # 5 iterations per imputation\n\n# Get completed datasets\ncompleted_datasets = kernel.complete_data(dataset=0,\
  \ inplace=False)  # First imputed dataset\n```\n\nSTEP 4.4: Alternative MICE implementation (if miceforest fails):\n```python\n\
  from sklearn.experimental import enable_iterative_imputer\nfrom sklearn.impute import IterativeImputer\nimport pandas as\
  \ pd\n\n# Prepare data matrix\nX = df[impute_vars].values\n\n# Initialize iterative imputer (MICE-like)\nimputer = IterativeImputer(\n\
  \    max_iter=50,\n    random_state=42,\n    sample_posterior=True,\n    min_value=0,  # Gini, V-Dem, education, social\
  \ spending are non-negative\n    max_value=None\n)\n\n# Fit and transform\nX_imputed = imputer.fit_transform(X)\n```\n\n\
  STEP 4.5: Validate imputed values:\n- Check ranges: Gini 0.2-0.8, V-Dem 0-1, education 0-15, social spending 0-30\n- Compare\
  \ means before/after imputation (should be similar)\n- Plot distributions before/after imputation\n- Ensure no negative\
  \ values or impossible combinations\n\nPHASE 5: EXPORT AND DOCUMENT (1 hour)\n\nCRITICAL OUTPUT REQUIREMENTS:\n- Main output\
  \ file MUST be named 'data_out.json'\n- Output format: JSON with records orientation (one object per line)\n- Each record\
  \ = one country-year observation with all variables\n- File location: current working directory (where executor runs)\n\n\
  STEP 5.1: Export dataset in 3 variants:\n```python\n# Full dataset (first imputed dataset) - THIS IS THE MAIN OUTPUT\nfull_df\
  \ = completed_datasets  # or X_imputed as DataFrame\nfull_df.to_json('data_out.json', orient='records', lines=True)\n\n\
  # Mini dataset (3 complete country panels for testing)\nmini_countries = ['Poland', 'Hungary', 'South Africa']\nmini_df\
  \ = full_df[full_df['country'].isin(mini_countries)]\nmini_df.to_json('mini_data_out.json', orient='records', lines=True)\n\
  \n# Preview (first 3 rows for logging)\npreview_df = full_df.head(3)\npreview_df.to_json('preview_data_out.json', orient='records',\
  \ lines=True)\n```\n\nSTEP 5.2: Create data dictionary (data_dictionary.md):\n```markdown\n# Data Dictionary: Post-1990\
  \ Democratizers Panel (1990-2022)\n\n## Sources\n- Gini coefficient: [OWID/SWIID/World Bank] - specify which source used\n\
  - V-Dem Electoral Democracy Index: V-Dem v13 (2023)\n- Mean years of schooling: [OWID/UNESCO] - specify which source used\n\
  - Social protection spending: [OWID/OECD] - specify which source used\n\n## Variables\n- country: Country name (string)\n\
  - year: Year (integer, 1990-2022)\n- gini: Gini coefficient (float, 0-1 scale)\n  - SCALING CORRECTION: Original OWID data\
  \ had mean=2.84 (incorrect). \n    Fixed by [dividing by 100 / using SWIID data / etc.]\n- v2x_egaldem: V-Dem Electoral\
  \ Democracy Index (float, 0-1)\n- education: Mean years of schooling (float, years)\n- social_spending: Social protection\
  \ spending (% GDP, float)\n- region_europe: Dummy for Europe (0/1)\n- region_africa: Dummy for Africa (0/1)\n- region_asia:\
  \ Dummy for Asia (0/1)\n\n## Imputation\n- Method: MICE (Multiple Imputation by Chained Equations)\n- Software: miceforest\
  \ (50 imputations, 5 iterations each)\n- Variables imputed: gini, v2x_egaldem, education, social_spending\n- Auxiliary variables:\
  \ gdp_per_capita, population, region dummies\n- Missing data rate before imputation: X%\n- Missing data rate after imputation:\
  \ 0% (all values imputed)\n\n## Country List (N=XX)\n[List all post-1990 democratizers with transition year]\n```\n\nSTEP\
  \ 5.3: Validate output with aii-json skill:\n- Check that data_out.json conforms to expected schema\n- Verify file size\
  \ is under 300MB (use aii-file-size-limit skill if needed)\n- Run aii-json validation if schema is provided\n\nPHASE 6:\
  \ QUALITY ASSURANCE (30 min)\n\nSTEP 6.1: Verify variable scaling:\n```python\nprint('Gini descriptive stats:')\nprint(full_df['gini'].describe())\n\
  print('Expected: mean 0.35-0.45, range 0.20-0.70')\n\nprint('\\nV-Dem descriptive stats:')\nprint(full_df['v2x_egaldem'].describe())\n\
  print('Expected: mean 0.5-0.7, range 0-1')\n```\n\nSTEP 6.2: Check for data errors:\n- Negative values (not allowed for\
  \ any variable)\n- Gini > 1.0 (likely scaling error)\n- V-Dem outside 0-1 range\n- Education > 20 years (implausible)\n\
  - Social spending > 50% GDP (rare, flag for review)\n\nSTEP 6.3: Compare with published statistics:\n- Check V-Dem country\
  \ averages against V-Dem annual reports\n- Verify Gini values against SWIID published tables\n- Cross-check social spending\
  \ for OECD countries against OECD SOCX database\n\nFALLBACK OPTIONS:\n1. If OWID search fails: Use direct downloads from\
  \ original sources (V-Dem, SWIID, UNESCO, OECD)\n2. If miceforest fails: Use sklearn IterativeImputer (simpler but effective)\n\
  3. If 50 imputations take too long: Reduce to 10-20 imputations\n4. If MICE is too complex: Use simple mean/median imputation\
  \ for robustness check\n5. If file size > 300MB: Save only first imputed dataset + imputation model parameters\n6. If country\
  \ name harmonization fails: Use ISO 3-letter country codes as primary key\n\nTROUBLESHOOTING COMMON ISSUES:\n- Issue: OWID\
  \ search returns no results for variable names\n  Fix: Try alternative search terms (e.g., 'Gini' instead of 'Gini coefficient')\n\
  - Issue: SWIID download fails (403 Forbidden)\n  Fix: Try alternative URL or use World Bank PIP data\n- Issue: miceforest\
  \ installation fails\n  Fix: Use `uv pip install miceforest --no-deps` then install deps manually\n- Issue: MICE takes too\
  \ long (>2 hours)\n  Fix: Reduce number of imputations to 10, reduce iterations to 3\n- Issue: Country names don't match\
  \ across datasets\n  Fix: Create manual mapping dictionary for common variations"
target_num_datasets: 1
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read skill files for your data sources (see <available_data_sources>) and domain handbook if applicable (see <available_domain_handbooks>). Based on plan and context, decide which source(s) to use. Include everything specified in the artifact plan, but you may also collect additional relevant data beyond what's listed. Run 8 diverse searches across chosen source(s) — BROAD, GENERAL terms, not very specific. Parallelize where supported.
TODO 3. Identify the 4 most promising datasets. IMPORTANT: Only consider datasets under 300MB. Preview/inspect sample rows for each candidate. Parallelize previews.
TODO 4. Research each candidate BEFORE choosing which to download. For each, search the web (aii-web-tools skill): dataset name, papers citing it, original source/task, popularity. Red flags: no search results, no papers, anonymized features (F1, F2...), <100 downloads, no documentation. Green flags: papers using it, clear documentation, meaningful features, established benchmark. Also consider: will features/structure allow meaningful evaluation of the planned method?
TODO 5. Decide which to KEEP vs DISCARD. Look for: clear structure, relevant fields, quality examples matching requirements, confirmed provenance. Determine which 2 datasets have the most suitable data. Download and save to `temp/datasets/`. Parallelize downloads.
</todos>
````

### [2] HUMAN-USER prompt · 2026-06-22 12:08:41 UTC

```
Direction: Comparative Political Economy — Inequality and Democratic Resilience. Something genuinely novel and groundbreaking that traces how inequality, education, and democratic-quality co-evolve across post-1990 democratizers, identifies what sustains resilience versus backsliding, and tests whether welfare-state institutions mediate the link. MUST use Our World in Data (OWID) panels.

Ambition: level 1 of 5 — confirmatory/parametric science: a careful confirmatory test within established institutional-economics theory; precision, identification, and robustness over conceptual novelty.

Reviewer: I am Daron Acemoglu (MIT). Calibrate from my existing work. Cross-domain perspectives (historical sociology, political behavior, economic anthropology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for the American Political Science Review, the Journal of Democracy, or World Politics. Audience: comparative political economists and political scientists. Tone: empirically rigorous, grounded in institutional economics, reproducible on public OWID data.
```

### [3] SKILL-INPUT — aii-python · 2026-06-22 12:08:59 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-owid-datasets · 2026-06-22 12:08:59 UTC

The agent loaded the **aii-owid-datasets** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-owid-datasets
description: Search and load datasets from Our World in Data catalog using BM25 search. Returns actual table data (default limit 3) with metadata, preview, and mini dataset. Use for global statistics on energy, health, COVID-19, economics, environment, demographics.
---

## Contents

- Workflow (2-phase table discovery process)
- Scripts (Search, Download with full parameters)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: 2-Phase Table Discovery

### Phase 1: Search for Tables
Find tables with metadata (title, description, variables)
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_owid_search_datasets.py "renewable energy" --limit 5
```

### Phase 2: Download Table (if suitable)
Download the table after reviewing the search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_owid_download_datasets.py "grapher/energy/2023-12-12/energy_mix"
```

---

## Scripts

### Search OWID tables (aii_owid_search_datasets.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_owid_search_datasets.py "climate change" --limit 3
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_owid_search_datasets.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 3' ::: 'renewable energy' 'climate change' 'covid mortality'
```

**Example output:**
```
Found 3 OWID tables for 'climate change':

[1] Climate Change Impacts
    Path: grapher/climate/2023-10-15/climate_impacts
    Description: Global temperature anomalies and sea level rise...
    Variables (42 total):
      - Global temperature anomaly (°C): Annual global mean temperature anomaly
      - Sea level rise (mm): Global mean sea level change
      - Atmospheric CO2 concentration (ppm): Monthly CO2 concentration at Mauna Loa
      - Arctic sea ice extent (million km²): Monthly Arctic sea ice extent
      ...
```

**Parameters:**

`query` (required, positional)
- Search query string
- Examples: `"covid"`, `"energy mix"`, `"climate change"`

`--limit` (optional)
- Number of search results to return (default: 3)
- Higher values = more results to choose from

**Tips:**
- Search is fast (uses pre-built BM25 index, no network required)
- Returns metadata only - no data is downloaded
- Use the `path` field from results to download specific tables
- BM25 search ranks by relevance across table titles, descriptions, and variable metadata
- Search returns tables from all channels (garden=highest quality, meadow=raw, backport=legacy, open_numbers=Gapminder)

---

### Download OWID table (aii_owid_download_datasets.py)

Download a table by path (from search results) and save to files.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_owid_download_datasets.py "grapher/energy/2023-12-12/energy_mix"
```

**Parallel execution (multiple tables):**

IMPORTANT: When downloading multiple tables, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-owid-datasets" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_owid_download_datasets.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'grapher/energy/2023-12-12/energy_mix' 'grapher/demography/2023-10-10/population' 'grapher/health/2023-08-01/life_expectancy'
```

**Example output:**
```
Downloaded OWID table: grapher/energy/2023-12-12/energy_mix

Dimensions: 15,420 rows x 12 columns
Columns: country, year, coal, oil, gas, nuclear, hydro, solar, wind, biofuels...

Files saved:
  Mini (READ THIS for development/testing): /path/to/mini_grapher_energy_2023-12-12_energy_mix.json
  Preview (DO NOT READ - for logging only): /path/to/preview_grapher_energy_2023-12-12_energy_mix.json
  Full (DO NOT READ - for scripts only):    /path/to/full_grapher_energy_2023-12-12_energy_mix.json

Sample data (first 3 rows):
  Row 1:
    country: Afghanistan
    year: 2000
    coal: 0.5
    ...
```

**Parameters:**

`path` (required, positional)
- Table path from search results
- Examples: `"grapher/energy/2023-12-12/energy_mix"`, `"garden/demography/2023-10-10/population"`

**Output files (auto-saved to `temp/tables/`):**
1. **Mini**: `mini_{path}.json` - 3 full rows - **READ THIS** for development/testing
2. **Preview**: `preview_{path}.json` - 3 truncated rows - **DO NOT READ directly** - for code you write to read
3. **Full**: `full_{path}.json` - All rows - **DO NOT READ directly** - for code you write to read

**Tips:**
- **Critical**: Only read the mini file directly with Read tool. Preview and full are input paths for code you write
- Use the `path` from search results to download specific tables
- Downloads directly from OWID catalog (network required)
- Files always saved to `temp/tables/` (path included in response)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SKILL-INPUT — aii-json · 2026-06-22 12:08:59 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-use-hardware · 2026-06-22 12:09:01 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [7] SKILL-INPUT — aii-long-running-tasks · 2026-06-22 12:09:17 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [8] SKILL-INPUT — aii-parallel-computing · 2026-06-22 12:09:17 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SKILL-INPUT — aii-file-size-limit · 2026-06-22 12:09:17 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [10] SKILL-INPUT — aii-web-tools · 2026-06-22 12:10:41 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [11] SYSTEM-USER prompt · 2026-06-22 12:20:04 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx1
type: dataset
title: Correct Gini Scaling Error and Build Imputed Panel Dataset (1990-2022)
summary: >-
  Fix the Gini coefficient scaling error (mean=2.84 → 0.25-0.65 range), verify OWID variable availability, download corrected
  data from OWID and SWIID, apply Multiple Imputation by Chained Equations (MICE) with 50+ imputations, and export the corrected
  panel dataset with full/mini/preview variants and data dictionary. CRITICAL: The numeric variable IDs in the hypothesis
  (1014857, 1209753, 809139, 1210307) may not be standard OWID identifiers - they might be from V-Dem or another database.
  The executor must search by variable NAME, not ID.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: >-
  Balanced panel dataset (1990-2022) covering 50+ post-1990 democratizers with 4 key variables: (1) Gini coefficient (0-1
  scale, correctly scaled, values 0.25-0.65), (2) V-Dem Electoral Democracy Index (0-1 scale), (3) Mean years of schooling
  (continuous, 0-15 years), (4) Social protection spending (% GDP, 0-30%). All variables should have <30% missing data after
  MICE imputation. Dataset must be in long format (country-year observations), properly documented with variable definitions,
  sources, and the specific Gini scaling correction applied. Final file size must be under 300MB.
dataset_search_plan: "PHASE 1: IDENTIFY CORRECT DATA SOURCES (1 hour)\n\nSTEP 1.1: Verify OWID variable availability by searching\
  \ for VARIABLE NAMES (not IDs):\n- Use aii-owid-datasets skill to search for these variable names:\n  a. 'Gini coefficient'\
  \ or 'income inequality Gini'\n  b. 'V-Dem electoral democracy' or 'electoral democracy index'\n  c. 'mean years of schooling'\
  \ or 'schooling years'\n  d. 'social protection spending' or 'social expenditure'\n- IMPORTANT: The numeric IDs (1014857,\
  \ 1209753, 809139, 1210307) in the hypothesis are likely NOT OWID variable IDs. OWID uses path-based identifiers like 'grapher/inequality/2023-12-12/gini-coefficient'.\
  \ Search by name to find correct OWID paths.\n- Download mini/preview samples of each variable to verify data structure\
  \ and scaling.\n\nSTEP 1.2: Identify alternative data sources (in case OWID variables are unavailable):\n- SWIID (Standardized\
  \ World Income Inequality Database):\n  * URL: https://swiid.org/\n  * Direct download: https://swiid.org/data/swiid9_4.dta\
  \ (Stata format, readable with pandas.read_stata())\n  * Documentation: Check SWIID codebook for Gini variable names (typically\
  \ 'gini_disp' for disposable income, 'gini_mkt' for market income)\n- V-Dem (Varieties of Democracy):\n  * URL: https://v-dem.net/data/\n\
  \  * Direct CSV download: https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv\n  * Variable: 'v2x_egaldem'\
  \ (Electoral Democracy Index, 0-1 scale)\n- UNESCO Institute for Statistics:\n  * URL: http://data.uis.unesco.org/\n  *\
  \ API: http://data.uis.unesco.org/API/UNESCO/static/API-doc/\n  * Variable: Mean years of schooling (UIS statistic code:\
  \ 'ML.2.FSGOVT')\n- OECD Social Expenditure Database:\n  * URL: https://www.oecd.org/social/expenditure.htm\n  * API: https://stats.oecd.org/Index.aspx?DataSetCode=SOCX_AGG\n\
  \  * Variable: Social protection expenditure (% GDP)\n\nPHASE 2: DOWNLOAD AND MERGE DATA (1.5 hours)\n\nSTEP 2.1: Download\
  \ Gini coefficient data:\n- PRIMARY: Try OWID first (search 'Gini coefficient', download if available)\n- SECONDARY: Download\
  \ SWIID data:\n  ```python\n  import pandas as pd\n  swiid_url = 'https://swiid.org/data/swiid9_4.dta'\n  gini_df = pd.read_stata(swiid_url)\n\
  \  # Keep key columns: country, year, gini_disp (or gini_mkt)\n  ```\n- TERTIARY: Use World Bank PIP API:\n  ```python\n\
  \  import requests\n  # World Bank Gini API (indicator: SI.POV.GINI)\n  wb_url = 'https://api.worldbank.org/v2/country/all/indicator/SI.POV.GINI?format=json&per_page=1000'\n\
  \  response = requests.get(wb_url)\n  ```\n- Verify Gini scaling: Print descriptive statistics. Correct values should be\
  \ 0.25-0.65 (0-1 scale) or 25-65 (0-100 scale). If mean is 2.84, data is incorrectly scaled - apply fix: divide by 100 if\
  \ values are 20-70, or divide by 10 if values are 2-7.\n\nSTEP 2.2: Download V-Dem Electoral Democracy Index:\n- PRIMARY:\
  \ Download from V-Dem direct CSV link (https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv)\n- Filter\
  \ columns: 'country_name', 'year', 'v2x_egaldem'\n- Verify scale: Should be 0-1 (if not, check V-Dem codebook - may need\
  \ rescaling)\n\nSTEP 2.3: Download education data (Mean years of schooling):\n- PRIMARY: OWID search 'mean years of schooling'\n\
  - SECONDARY: UNESCO API or World Bank EdStats (indicator: SE.SEC.NENR)\n\nSTEP 2.4: Download social protection spending:\n\
  - PRIMARY: OWID search 'social protection spending'\n- SECONDARY: OECD Social Expenditure Database (for OECD members) or\
  \ ILO ILOSTAT\n\nSTEP 2.5: Merge all datasets:\n- Use country-year as merge key\n- Harmonize country names (create mapping\
  \ dictionary for different spellings)\n- Restrict to years 1990-2022\n\nPHASE 3: IDENTIFY POST-1990 DEMOCRATIZERS (30 min)\n\
  \nSTEP 3.1: Define inclusion criteria:\n- Countries with V-Dem Electoral Democracy Index > 0.5 in any year 1990-1999 (transition\
  \ to democracy)\n- Countries that remained sovereign through 2022 (exclude dissolved states like USSR, Yugoslavia)\n- Exclude\
  \ established democracies pre-1990 (V-Dem > 0.5 in 1989)\n\nSTEP 3.2: Create country list programmatically:\n```python\n\
  # Pseudo-code for identifying post-1990 democratizers\nvdem_df = pd.read_csv('vdem_data.csv')\ntransition_countries = vdem_df[\n\
  \    (vdem_df['year'].between(1990, 1999)) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n]['country_name'].unique()\n\n# Exclude\
  \ pre-1990 democracies\npre1990_democracies = vdem_df[\n    (vdem_df['year'] == 1989) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n\
  ]['country_name'].unique()\n\npost1990_democratizers = [c for c in transition_countries if c not in pre1990_democracies]\n\
  ```\n\nSTEP 3.3: Expected country list (~50-70 countries):\n- Post-communist: Poland, Czech Republic, Slovakia, Hungary,\
  \ Estonia, Latvia, Lithuania, Slovenia, Croatia, Romania, Bulgaria, Albania, N. Macedonia, Serbia, Montenegro, Bosnia, Ukraine,\
  \ Belarus, Moldova, Russia, Armenia, Georgia, Azerbaijan, Kazakhstan, Kyrgyzstan, Uzbekistan, Mongolia\n- Africa: South\
  \ Africa (1994), Ghana, Kenya, Malawi, Mali, Niger, Senegal, Zambia, Benin, Cape Verde, Mali, Madagascar, Tanzania\n- Asia:\
  \ Indonesia (1998), Philippines, Thailand, Taiwan, South Korea (check transition year)\n- Latin America: (few, most transitioned\
  \ pre-1990)\n\nPHASE 4: APPLY MULTIPLE IMPUTATION BY CHAINED EQUATIONS (2 hours)\n\nSTEP 4.1: Install required libraries:\n\
  ```bash\nuv pip install miceforest scikit-learn statsmodels openpyxl\n```\n\nSTEP 4.2: Prepare data for imputation:\n- Combine\
  \ all variables into single DataFrame (country, year, Gini, V-Dem, education, social_spending)\n- Add auxiliary variables\
  \ to improve imputation: GDP per capita, population, region dummies\n- Create dummy variables for regions (Europe, Africa,\
  \ Asia, Latin America)\n- Ensure all variables are numeric (no strings except country/year)\n\nSTEP 4.3: Run MICE using\
  \ miceforest (preferred for speed):\n```python\nimport miceforest as mf\nimport pandas as pd\nimport numpy as np\n\n# Load\
  \ data\ndf = pd.read_csv('merged_panel.csv')\n\n# Define variables to impute\nimpute_vars = ['gini', 'v2x_egaldem', 'education',\
  \ 'social_spending', \n               'gdp_per_capita', 'population']\n\n# Initialize MICE kernel\nkernel = mf.ImputationKernel(\n\
  \    data=df[impute_vars + ['country', 'year', 'region_europe', 'region_africa', 'region_asia']],\n    variable_schema={\n\
  \        'gini': impute_vars,\n        'v2x_egaldem': impute_vars,\n        'education': impute_vars,\n        'social_spending':\
  \ impute_vars\n    },\n    datasets=50,  # Number of imputed datasets\n    save_all_iterations=True\n)\n\n# Run MICE iterations\n\
  kernel.mice(5)  # 5 iterations per imputation\n\n# Get completed datasets\ncompleted_datasets = kernel.complete_data(dataset=0,\
  \ inplace=False)  # First imputed dataset\n```\n\nSTEP 4.4: Alternative MICE implementation (if miceforest fails):\n```python\n\
  from sklearn.experimental import enable_iterative_imputer\nfrom sklearn.impute import IterativeImputer\nimport pandas as\
  \ pd\n\n# Prepare data matrix\nX = df[impute_vars].values\n\n# Initialize iterative imputer (MICE-like)\nimputer = IterativeImputer(\n\
  \    max_iter=50,\n    random_state=42,\n    sample_posterior=True,\n    min_value=0,  # Gini, V-Dem, education, social\
  \ spending are non-negative\n    max_value=None\n)\n\n# Fit and transform\nX_imputed = imputer.fit_transform(X)\n```\n\n\
  STEP 4.5: Validate imputed values:\n- Check ranges: Gini 0.2-0.8, V-Dem 0-1, education 0-15, social spending 0-30\n- Compare\
  \ means before/after imputation (should be similar)\n- Plot distributions before/after imputation\n- Ensure no negative\
  \ values or impossible combinations\n\nPHASE 5: EXPORT AND DOCUMENT (1 hour)\n\nCRITICAL OUTPUT REQUIREMENTS:\n- Main output\
  \ file MUST be named 'data_out.json'\n- Output format: JSON with records orientation (one object per line)\n- Each record\
  \ = one country-year observation with all variables\n- File location: current working directory (where executor runs)\n\n\
  STEP 5.1: Export dataset in 3 variants:\n```python\n# Full dataset (first imputed dataset) - THIS IS THE MAIN OUTPUT\nfull_df\
  \ = completed_datasets  # or X_imputed as DataFrame\nfull_df.to_json('data_out.json', orient='records', lines=True)\n\n\
  # Mini dataset (3 complete country panels for testing)\nmini_countries = ['Poland', 'Hungary', 'South Africa']\nmini_df\
  \ = full_df[full_df['country'].isin(mini_countries)]\nmini_df.to_json('mini_data_out.json', orient='records', lines=True)\n\
  \n# Preview (first 3 rows for logging)\npreview_df = full_df.head(3)\npreview_df.to_json('preview_data_out.json', orient='records',\
  \ lines=True)\n```\n\nSTEP 5.2: Create data dictionary (data_dictionary.md):\n```markdown\n# Data Dictionary: Post-1990\
  \ Democratizers Panel (1990-2022)\n\n## Sources\n- Gini coefficient: [OWID/SWIID/World Bank] - specify which source used\n\
  - V-Dem Electoral Democracy Index: V-Dem v13 (2023)\n- Mean years of schooling: [OWID/UNESCO] - specify which source used\n\
  - Social protection spending: [OWID/OECD] - specify which source used\n\n## Variables\n- country: Country name (string)\n\
  - year: Year (integer, 1990-2022)\n- gini: Gini coefficient (float, 0-1 scale)\n  - SCALING CORRECTION: Original OWID data\
  \ had mean=2.84 (incorrect). \n    Fixed by [dividing by 100 / using SWIID data / etc.]\n- v2x_egaldem: V-Dem Electoral\
  \ Democracy Index (float, 0-1)\n- education: Mean years of schooling (float, years)\n- social_spending: Social protection\
  \ spending (% GDP, float)\n- region_europe: Dummy for Europe (0/1)\n- region_africa: Dummy for Africa (0/1)\n- region_asia:\
  \ Dummy for Asia (0/1)\n\n## Imputation\n- Method: MICE (Multiple Imputation by Chained Equations)\n- Software: miceforest\
  \ (50 imputations, 5 iterations each)\n- Variables imputed: gini, v2x_egaldem, education, social_spending\n- Auxiliary variables:\
  \ gdp_per_capita, population, region dummies\n- Missing data rate before imputation: X%\n- Missing data rate after imputation:\
  \ 0% (all values imputed)\n\n## Country List (N=XX)\n[List all post-1990 democratizers with transition year]\n```\n\nSTEP\
  \ 5.3: Validate output with aii-json skill:\n- Check that data_out.json conforms to expected schema\n- Verify file size\
  \ is under 300MB (use aii-file-size-limit skill if needed)\n- Run aii-json validation if schema is provided\n\nPHASE 6:\
  \ QUALITY ASSURANCE (30 min)\n\nSTEP 6.1: Verify variable scaling:\n```python\nprint('Gini descriptive stats:')\nprint(full_df['gini'].describe())\n\
  print('Expected: mean 0.35-0.45, range 0.20-0.70')\n\nprint('\\nV-Dem descriptive stats:')\nprint(full_df['v2x_egaldem'].describe())\n\
  print('Expected: mean 0.5-0.7, range 0-1')\n```\n\nSTEP 6.2: Check for data errors:\n- Negative values (not allowed for\
  \ any variable)\n- Gini > 1.0 (likely scaling error)\n- V-Dem outside 0-1 range\n- Education > 20 years (implausible)\n\
  - Social spending > 50% GDP (rare, flag for review)\n\nSTEP 6.3: Compare with published statistics:\n- Check V-Dem country\
  \ averages against V-Dem annual reports\n- Verify Gini values against SWIID published tables\n- Cross-check social spending\
  \ for OECD countries against OECD SOCX database\n\nFALLBACK OPTIONS:\n1. If OWID search fails: Use direct downloads from\
  \ original sources (V-Dem, SWIID, UNESCO, OECD)\n2. If miceforest fails: Use sklearn IterativeImputer (simpler but effective)\n\
  3. If 50 imputations take too long: Reduce to 10-20 imputations\n4. If MICE is too complex: Use simple mean/median imputation\
  \ for robustness check\n5. If file size > 300MB: Save only first imputed dataset + imputation model parameters\n6. If country\
  \ name harmonization fails: Use ISO 3-letter country codes as primary key\n\nTROUBLESHOOTING COMMON ISSUES:\n- Issue: OWID\
  \ search returns no results for variable names\n  Fix: Try alternative search terms (e.g., 'Gini' instead of 'Gini coefficient')\n\
  - Issue: SWIID download fails (403 Forbidden)\n  Fix: Try alternative URL or use World Bank PIP data\n- Issue: miceforest\
  \ installation fails\n  Fix: Use `uv pip install miceforest --no-deps` then install deps manually\n- Issue: MICE takes too\
  \ long (>2 hours)\n  Fix: Reduce number of imputations to 10, reduce iterations to 3\n- Issue: Country names don't match\
  \ across datasets\n  Fix: Create manual mapping dictionary for common variations"
target_num_datasets: 1
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. For the top 2 datasets, create data.py (uv inline script) that: loads from temp/datasets/, standardizes to exp_sel_data_out.json schema (aii-json skill), extracts all examples per dataset, handles domain requirements, saves to full_data_out.json.

Each data ROW must be a separate example — do NOT create one example per dataset or per fold. Each data point (row, sample, instance) = one example. 500 rows → 500 examples. The output is GROUPED BY DATASET:
```json
{
  "datasets": [
    {
      "dataset": "iris",
      "examples": [
        {"input": "...", "output": "...", "metadata_fold": 2, "metadata_feature_names": [...]},
        ...
      ]
    },
    {
      "dataset": "adult_census",
      "examples": [...]
    }
  ]
}
```
Per-example required fields:
- `input`: input features/text (tabular: JSON string of feature values)
- `output`: target/label (as string)
Per-example optional metadata via `metadata_<name>` fields (flat, not nested object):
- `metadata_fold`: fold assignment (int), `metadata_feature_names`: feature name list, `metadata_task_type`: "classification"/"regression", `metadata_n_classes`: number of classes, `metadata_row_index`: original row index, etc.
Do NOT use `split`, `dataset`, or `context` as per-example fields. Dataset name goes at the group level, metadata goes in `metadata_*` fields.
TODO 2. Run 'uv run data.py' and fix errors. Validate full_data_out.json against exp_sel_data_out.json schema (aii-json skill) — fix errors. Generate preview, mini, full versions with aii-json skill's format script.
TODO 3. Read preview to inspect examples. Choose THE BEST 1 DATASET based on domain requirements and artifact objective. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
````

### [12] SYSTEM-USER prompt · 2026-06-22 12:21:44 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/`:
GOOD: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/file.py`, `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_dataset_1_idx1
type: dataset
title: Correct Gini Scaling Error and Build Imputed Panel Dataset (1990-2022)
summary: >-
  Fix the Gini coefficient scaling error (mean=2.84 → 0.25-0.65 range), verify OWID variable availability, download corrected
  data from OWID and SWIID, apply Multiple Imputation by Chained Equations (MICE) with 50+ imputations, and export the corrected
  panel dataset with full/mini/preview variants and data dictionary. CRITICAL: The numeric variable IDs in the hypothesis
  (1014857, 1209753, 809139, 1210307) may not be standard OWID identifiers - they might be from V-Dem or another database.
  The executor must search by variable NAME, not ID.
runpod_compute_profile: cpu_heavy
ideal_dataset_criteria: >-
  Balanced panel dataset (1990-2022) covering 50+ post-1990 democratizers with 4 key variables: (1) Gini coefficient (0-1
  scale, correctly scaled, values 0.25-0.65), (2) V-Dem Electoral Democracy Index (0-1 scale), (3) Mean years of schooling
  (continuous, 0-15 years), (4) Social protection spending (% GDP, 0-30%). All variables should have <30% missing data after
  MICE imputation. Dataset must be in long format (country-year observations), properly documented with variable definitions,
  sources, and the specific Gini scaling correction applied. Final file size must be under 300MB.
dataset_search_plan: "PHASE 1: IDENTIFY CORRECT DATA SOURCES (1 hour)\n\nSTEP 1.1: Verify OWID variable availability by searching\
  \ for VARIABLE NAMES (not IDs):\n- Use aii-owid-datasets skill to search for these variable names:\n  a. 'Gini coefficient'\
  \ or 'income inequality Gini'\n  b. 'V-Dem electoral democracy' or 'electoral democracy index'\n  c. 'mean years of schooling'\
  \ or 'schooling years'\n  d. 'social protection spending' or 'social expenditure'\n- IMPORTANT: The numeric IDs (1014857,\
  \ 1209753, 809139, 1210307) in the hypothesis are likely NOT OWID variable IDs. OWID uses path-based identifiers like 'grapher/inequality/2023-12-12/gini-coefficient'.\
  \ Search by name to find correct OWID paths.\n- Download mini/preview samples of each variable to verify data structure\
  \ and scaling.\n\nSTEP 1.2: Identify alternative data sources (in case OWID variables are unavailable):\n- SWIID (Standardized\
  \ World Income Inequality Database):\n  * URL: https://swiid.org/\n  * Direct download: https://swiid.org/data/swiid9_4.dta\
  \ (Stata format, readable with pandas.read_stata())\n  * Documentation: Check SWIID codebook for Gini variable names (typically\
  \ 'gini_disp' for disposable income, 'gini_mkt' for market income)\n- V-Dem (Varieties of Democracy):\n  * URL: https://v-dem.net/data/\n\
  \  * Direct CSV download: https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv\n  * Variable: 'v2x_egaldem'\
  \ (Electoral Democracy Index, 0-1 scale)\n- UNESCO Institute for Statistics:\n  * URL: http://data.uis.unesco.org/\n  *\
  \ API: http://data.uis.unesco.org/API/UNESCO/static/API-doc/\n  * Variable: Mean years of schooling (UIS statistic code:\
  \ 'ML.2.FSGOVT')\n- OECD Social Expenditure Database:\n  * URL: https://www.oecd.org/social/expenditure.htm\n  * API: https://stats.oecd.org/Index.aspx?DataSetCode=SOCX_AGG\n\
  \  * Variable: Social protection expenditure (% GDP)\n\nPHASE 2: DOWNLOAD AND MERGE DATA (1.5 hours)\n\nSTEP 2.1: Download\
  \ Gini coefficient data:\n- PRIMARY: Try OWID first (search 'Gini coefficient', download if available)\n- SECONDARY: Download\
  \ SWIID data:\n  ```python\n  import pandas as pd\n  swiid_url = 'https://swiid.org/data/swiid9_4.dta'\n  gini_df = pd.read_stata(swiid_url)\n\
  \  # Keep key columns: country, year, gini_disp (or gini_mkt)\n  ```\n- TERTIARY: Use World Bank PIP API:\n  ```python\n\
  \  import requests\n  # World Bank Gini API (indicator: SI.POV.GINI)\n  wb_url = 'https://api.worldbank.org/v2/country/all/indicator/SI.POV.GINI?format=json&per_page=1000'\n\
  \  response = requests.get(wb_url)\n  ```\n- Verify Gini scaling: Print descriptive statistics. Correct values should be\
  \ 0.25-0.65 (0-1 scale) or 25-65 (0-100 scale). If mean is 2.84, data is incorrectly scaled - apply fix: divide by 100 if\
  \ values are 20-70, or divide by 10 if values are 2-7.\n\nSTEP 2.2: Download V-Dem Electoral Democracy Index:\n- PRIMARY:\
  \ Download from V-Dem direct CSV link (https://v-dem.net/static/website/share/2023/V-Dem-CY+Others+Others-v13.csv)\n- Filter\
  \ columns: 'country_name', 'year', 'v2x_egaldem'\n- Verify scale: Should be 0-1 (if not, check V-Dem codebook - may need\
  \ rescaling)\n\nSTEP 2.3: Download education data (Mean years of schooling):\n- PRIMARY: OWID search 'mean years of schooling'\n\
  - SECONDARY: UNESCO API or World Bank EdStats (indicator: SE.SEC.NENR)\n\nSTEP 2.4: Download social protection spending:\n\
  - PRIMARY: OWID search 'social protection spending'\n- SECONDARY: OECD Social Expenditure Database (for OECD members) or\
  \ ILO ILOSTAT\n\nSTEP 2.5: Merge all datasets:\n- Use country-year as merge key\n- Harmonize country names (create mapping\
  \ dictionary for different spellings)\n- Restrict to years 1990-2022\n\nPHASE 3: IDENTIFY POST-1990 DEMOCRATIZERS (30 min)\n\
  \nSTEP 3.1: Define inclusion criteria:\n- Countries with V-Dem Electoral Democracy Index > 0.5 in any year 1990-1999 (transition\
  \ to democracy)\n- Countries that remained sovereign through 2022 (exclude dissolved states like USSR, Yugoslavia)\n- Exclude\
  \ established democracies pre-1990 (V-Dem > 0.5 in 1989)\n\nSTEP 3.2: Create country list programmatically:\n```python\n\
  # Pseudo-code for identifying post-1990 democratizers\nvdem_df = pd.read_csv('vdem_data.csv')\ntransition_countries = vdem_df[\n\
  \    (vdem_df['year'].between(1990, 1999)) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n]['country_name'].unique()\n\n# Exclude\
  \ pre-1990 democracies\npre1990_democracies = vdem_df[\n    (vdem_df['year'] == 1989) &\n    (vdem_df['v2x_egaldem'] > 0.5)\n\
  ]['country_name'].unique()\n\npost1990_democratizers = [c for c in transition_countries if c not in pre1990_democracies]\n\
  ```\n\nSTEP 3.3: Expected country list (~50-70 countries):\n- Post-communist: Poland, Czech Republic, Slovakia, Hungary,\
  \ Estonia, Latvia, Lithuania, Slovenia, Croatia, Romania, Bulgaria, Albania, N. Macedonia, Serbia, Montenegro, Bosnia, Ukraine,\
  \ Belarus, Moldova, Russia, Armenia, Georgia, Azerbaijan, Kazakhstan, Kyrgyzstan, Uzbekistan, Mongolia\n- Africa: South\
  \ Africa (1994), Ghana, Kenya, Malawi, Mali, Niger, Senegal, Zambia, Benin, Cape Verde, Mali, Madagascar, Tanzania\n- Asia:\
  \ Indonesia (1998), Philippines, Thailand, Taiwan, South Korea (check transition year)\n- Latin America: (few, most transitioned\
  \ pre-1990)\n\nPHASE 4: APPLY MULTIPLE IMPUTATION BY CHAINED EQUATIONS (2 hours)\n\nSTEP 4.1: Install required libraries:\n\
  ```bash\nuv pip install miceforest scikit-learn statsmodels openpyxl\n```\n\nSTEP 4.2: Prepare data for imputation:\n- Combine\
  \ all variables into single DataFrame (country, year, Gini, V-Dem, education, social_spending)\n- Add auxiliary variables\
  \ to improve imputation: GDP per capita, population, region dummies\n- Create dummy variables for regions (Europe, Africa,\
  \ Asia, Latin America)\n- Ensure all variables are numeric (no strings except country/year)\n\nSTEP 4.3: Run MICE using\
  \ miceforest (preferred for speed):\n```python\nimport miceforest as mf\nimport pandas as pd\nimport numpy as np\n\n# Load\
  \ data\ndf = pd.read_csv('merged_panel.csv')\n\n# Define variables to impute\nimpute_vars = ['gini', 'v2x_egaldem', 'education',\
  \ 'social_spending', \n               'gdp_per_capita', 'population']\n\n# Initialize MICE kernel\nkernel = mf.ImputationKernel(\n\
  \    data=df[impute_vars + ['country', 'year', 'region_europe', 'region_africa', 'region_asia']],\n    variable_schema={\n\
  \        'gini': impute_vars,\n        'v2x_egaldem': impute_vars,\n        'education': impute_vars,\n        'social_spending':\
  \ impute_vars\n    },\n    datasets=50,  # Number of imputed datasets\n    save_all_iterations=True\n)\n\n# Run MICE iterations\n\
  kernel.mice(5)  # 5 iterations per imputation\n\n# Get completed datasets\ncompleted_datasets = kernel.complete_data(dataset=0,\
  \ inplace=False)  # First imputed dataset\n```\n\nSTEP 4.4: Alternative MICE implementation (if miceforest fails):\n```python\n\
  from sklearn.experimental import enable_iterative_imputer\nfrom sklearn.impute import IterativeImputer\nimport pandas as\
  \ pd\n\n# Prepare data matrix\nX = df[impute_vars].values\n\n# Initialize iterative imputer (MICE-like)\nimputer = IterativeImputer(\n\
  \    max_iter=50,\n    random_state=42,\n    sample_posterior=True,\n    min_value=0,  # Gini, V-Dem, education, social\
  \ spending are non-negative\n    max_value=None\n)\n\n# Fit and transform\nX_imputed = imputer.fit_transform(X)\n```\n\n\
  STEP 4.5: Validate imputed values:\n- Check ranges: Gini 0.2-0.8, V-Dem 0-1, education 0-15, social spending 0-30\n- Compare\
  \ means before/after imputation (should be similar)\n- Plot distributions before/after imputation\n- Ensure no negative\
  \ values or impossible combinations\n\nPHASE 5: EXPORT AND DOCUMENT (1 hour)\n\nCRITICAL OUTPUT REQUIREMENTS:\n- Main output\
  \ file MUST be named 'data_out.json'\n- Output format: JSON with records orientation (one object per line)\n- Each record\
  \ = one country-year observation with all variables\n- File location: current working directory (where executor runs)\n\n\
  STEP 5.1: Export dataset in 3 variants:\n```python\n# Full dataset (first imputed dataset) - THIS IS THE MAIN OUTPUT\nfull_df\
  \ = completed_datasets  # or X_imputed as DataFrame\nfull_df.to_json('data_out.json', orient='records', lines=True)\n\n\
  # Mini dataset (3 complete country panels for testing)\nmini_countries = ['Poland', 'Hungary', 'South Africa']\nmini_df\
  \ = full_df[full_df['country'].isin(mini_countries)]\nmini_df.to_json('mini_data_out.json', orient='records', lines=True)\n\
  \n# Preview (first 3 rows for logging)\npreview_df = full_df.head(3)\npreview_df.to_json('preview_data_out.json', orient='records',\
  \ lines=True)\n```\n\nSTEP 5.2: Create data dictionary (data_dictionary.md):\n```markdown\n# Data Dictionary: Post-1990\
  \ Democratizers Panel (1990-2022)\n\n## Sources\n- Gini coefficient: [OWID/SWIID/World Bank] - specify which source used\n\
  - V-Dem Electoral Democracy Index: V-Dem v13 (2023)\n- Mean years of schooling: [OWID/UNESCO] - specify which source used\n\
  - Social protection spending: [OWID/OECD] - specify which source used\n\n## Variables\n- country: Country name (string)\n\
  - year: Year (integer, 1990-2022)\n- gini: Gini coefficient (float, 0-1 scale)\n  - SCALING CORRECTION: Original OWID data\
  \ had mean=2.84 (incorrect). \n    Fixed by [dividing by 100 / using SWIID data / etc.]\n- v2x_egaldem: V-Dem Electoral\
  \ Democracy Index (float, 0-1)\n- education: Mean years of schooling (float, years)\n- social_spending: Social protection\
  \ spending (% GDP, float)\n- region_europe: Dummy for Europe (0/1)\n- region_africa: Dummy for Africa (0/1)\n- region_asia:\
  \ Dummy for Asia (0/1)\n\n## Imputation\n- Method: MICE (Multiple Imputation by Chained Equations)\n- Software: miceforest\
  \ (50 imputations, 5 iterations each)\n- Variables imputed: gini, v2x_egaldem, education, social_spending\n- Auxiliary variables:\
  \ gdp_per_capita, population, region dummies\n- Missing data rate before imputation: X%\n- Missing data rate after imputation:\
  \ 0% (all values imputed)\n\n## Country List (N=XX)\n[List all post-1990 democratizers with transition year]\n```\n\nSTEP\
  \ 5.3: Validate output with aii-json skill:\n- Check that data_out.json conforms to expected schema\n- Verify file size\
  \ is under 300MB (use aii-file-size-limit skill if needed)\n- Run aii-json validation if schema is provided\n\nPHASE 6:\
  \ QUALITY ASSURANCE (30 min)\n\nSTEP 6.1: Verify variable scaling:\n```python\nprint('Gini descriptive stats:')\nprint(full_df['gini'].describe())\n\
  print('Expected: mean 0.35-0.45, range 0.20-0.70')\n\nprint('\\nV-Dem descriptive stats:')\nprint(full_df['v2x_egaldem'].describe())\n\
  print('Expected: mean 0.5-0.7, range 0-1')\n```\n\nSTEP 6.2: Check for data errors:\n- Negative values (not allowed for\
  \ any variable)\n- Gini > 1.0 (likely scaling error)\n- V-Dem outside 0-1 range\n- Education > 20 years (implausible)\n\
  - Social spending > 50% GDP (rare, flag for review)\n\nSTEP 6.3: Compare with published statistics:\n- Check V-Dem country\
  \ averages against V-Dem annual reports\n- Verify Gini values against SWIID published tables\n- Cross-check social spending\
  \ for OECD countries against OECD SOCX database\n\nFALLBACK OPTIONS:\n1. If OWID search fails: Use direct downloads from\
  \ original sources (V-Dem, SWIID, UNESCO, OECD)\n2. If miceforest fails: Use sklearn IterativeImputer (simpler but effective)\n\
  3. If 50 imputations take too long: Reduce to 10-20 imputations\n4. If MICE is too complex: Use simple mean/median imputation\
  \ for robustness check\n5. If file size > 300MB: Save only first imputed dataset + imputation model parameters\n6. If country\
  \ name harmonization fails: Use ISO 3-letter country codes as primary key\n\nTROUBLESHOOTING COMMON ISSUES:\n- Issue: OWID\
  \ search returns no results for variable names\n  Fix: Try alternative search terms (e.g., 'Gini' instead of 'Gini coefficient')\n\
  - Issue: SWIID download fails (403 Forbidden)\n  Fix: Try alternative URL or use World Bank PIP data\n- Issue: miceforest\
  \ installation fails\n  Fix: Use `uv pip install miceforest --no-deps` then install deps manually\n- Issue: MICE takes too\
  \ long (>2 hours)\n  Fix: Reduce number of imputations to 10, reduce iterations to 3\n- Issue: Country names don't match\
  \ across datasets\n  Fix: Create manual mapping dictionary for common variations"
target_num_datasets: 1
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
- aii-handbook-multi-llm-agents: Multi-LLM agent orchestration patterns
</skills>
</available_resources>

<available_data_sources>
Use the sources appropriate to your task. Read the relevant skill file BEFORE using each source.

- **HuggingFace Hub** (HF) — ML datasets (NLP, vision, tabular, benchmarks)
- **Our World in Data** (OWID) — Global statistics (energy, health, economics, environment, demographics)
- **Alternate methods** — Python/shell (sklearn.datasets, openml, direct URL, APIs, etc.)

If the plan specifies a source or one fits better, use it.
You may combine sources. Use web search (aii-web-tools skill) to research candidates (background, papers, provenance) — NOT to find/download datasets.
</available_data_sources>

<available_domain_handbooks>
If your domain has a handbook, read the relevant skill file BEFORE working on that domain.

- **Multi-LLM Agents** — dataset selection, evaluation metrics, agent orchestration patterns
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Update data.py to only include the chosen 1 dataset and generate full_data_out.json. Re-run to generate full_data_out.json. Validate output format with aii-json skill and fix any errors. Generate full, mini, and preview versions with aii-json skill's format script using `--input full_data_out.json` (creates full_full_data_out.json, mini_full_data_out.json, preview_full_data_out.json — rename to full_data_out.json, mini_data_out.json, preview_data_out.json).
TODO 2. Verify full_data_out.json, preview_data_out.json, and mini_data_out.json exist in your workspace (see <workspace>) and contain correct data.
TODO 3. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to full_data_out.json.
TODO 4. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DatasetExpectedFiles": {
      "description": "All expected output files from dataset artifact.",
      "properties": {
        "script": {
          "description": "Path to data.py script. Example: 'data.py'",
          "title": "Script",
          "type": "string"
        },
        "datasets": {
          "description": "Dataset file groups \u2014 one per dataset, each with full/mini/preview variants",
          "items": {
            "$ref": "#/$defs/DatasetFileSet"
          },
          "title": "Datasets",
          "type": "array"
        }
      },
      "required": [
        "script",
        "datasets"
      ],
      "title": "DatasetExpectedFiles",
      "type": "object"
    },
    "DatasetFileSet": {
      "description": "One dataset's three required output variants.",
      "properties": {
        "full": {
          "description": "Full dataset JSON file(s). Single file or split files. Example: ['full_data_out.json'] or ['full_data_out/full_data_out_1.json', 'full_data_out/full_data_out_2.json']",
          "items": {
            "type": "string"
          },
          "title": "Full",
          "type": "array"
        },
        "mini": {
          "description": "Mini dataset JSON file path (3 examples). Example: 'mini_data_out.json'",
          "title": "Mini",
          "type": "string"
        },
        "preview": {
          "description": "Preview dataset JSON file path (10 examples). Example: 'preview_data_out.json'",
          "title": "Preview",
          "type": "string"
        }
      },
      "required": [
        "full",
        "mini",
        "preview"
      ],
      "title": "DatasetFileSet",
      "type": "object"
    }
  },
  "description": "Dataset artifact \u2014 structured output + file metadata.\n\nFinds, evaluates, and prepares datasets for research experiments.\nProduces data.py and full_data_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Descriptive title (roughly 30-90 characters). Must describe content, NOT a status message.",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/DatasetExpectedFiles",
      "description": "All output files you created. Must include data.py script plus dataset file groups (full/mini/preview variants)."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "DatasetArtifact",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_dataset_1/.sdk_openhands_agent_struct_out.json`.
````
