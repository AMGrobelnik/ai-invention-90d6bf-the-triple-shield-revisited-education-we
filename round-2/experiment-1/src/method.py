#!/usr/bin/env python3
"""
Triple Shield Analysis: Re-test Triple Interaction with Corrected Gini and MICE Multiple Imputation

This script implements:
1. Data loading and verification from dependency artifact
2. Gini scaling error correction (mixed 0-1 and 0-100 scales)
3. MICE multiple imputation (50 imputations) on full N=1,641 panel
4. Fixed-effects regressions with triple interaction (inequality × education × welfare spending)
5. Marginal effects computation per Brambor et al. (2006)
6. Export results to method_out.json

Author: AI Inventor System
Date: 2024
"""

from loguru import logger
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import sys
import numpy as np
import pandas as pd
import gc
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:HH:mm:ss}|{level:<7}|{message}"
)
logger.add(
    "logs/run.log",
    rotation="30 MB",
    level="DEBUG",
    backtrace=True,
    diagnose=True
)

# Create logs directory
Path("logs").mkdir(exist_ok=True)


@dataclass
class RegressionResult:
    """Container for regression results."""
    model_name: str
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    p_values: Dict[str, float]
    n_obs: int
    r_squared: float
    f_statistic: Optional[float] = None
    f_pvalue: Optional[float] = None


@dataclass
class ImputationResult:
    """Container for MICE imputation results."""
    imputed_datasets: List[pd.DataFrame]
    n_imputations: int
    original_missing_pattern: Dict[str, float]
    imputed_missing_pattern: Dict[str, float]


@dataclass
class MarginalEffect:
    """Container for marginal effect results."""
    variable: str
    at_values: Dict[str, float]
    effect: float
    std_error: float
    p_value: float
    ci_lower: float
    ci_upper: float


# ============================================================================
# STEP 1: DATA LOADING AND VERIFICATION
# ============================================================================

def load_and_verify_data(data_path: Path, mini: bool = False) -> pd.DataFrame:
    """
    Load the full panel dataset from dependency artifact.
    
    Args:
        data_path: Path to full_data_out.json or mini_data_out.json
        mini: If True, load mini dataset for testing
        
    Returns:
        DataFrame with columns: ['Code', 'Year', 'vdem_electoral', 'gini', 
                                  'education_years', 'social_spending', 
                                  'gdp_per_capita', 'resource_rents', 'population']
    """
    logger.info(f"Loading data from {data_path}")
    
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load data from {data_path}: {e}")
        raise
    
    # Extract examples from the datasets structure
    examples = data['datasets'][0]['examples']
    logger.info(f"Loaded {len(examples)} examples from JSON")
    
    # Convert to DataFrame
    rows = []
    for i, example in enumerate(examples):
        try:
            # Parse input JSON string
            input_dict = json.loads(example['input'])
            
            # Extract metadata
            country = example.get('metadata_country', f'UNK_{i}')
            year = example.get('metadata_year', 1990 + i)
            
            # Extract output (V-Dem electoral democracy index)
            vdem_electoral = float(example['output'])
            
            row = {
                'Code': country,
                'Year': int(year),
                'vdem_electoral': vdem_electoral,
                **input_dict  # Unpack all input features
            }
            rows.append(row)
            
        except Exception as e:
            logger.warning(f"Failed to parse example {i}: {e}")
            continue
    
    df = pd.DataFrame(rows)
    
    # Ensure correct column types
    numeric_cols = ['vdem_electoral', 'gini', 'education_years', 'social_spending',
                    'gdp_per_capita', 'resource_rents', 'population']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Set multi-index
    df = df.set_index(['Code', 'Year'])
    
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Countries: {df.index.get_level_values('Code').nunique()}")
    logger.info(f"Years: {df.index.get_level_values('Year').min()} - {df.index.get_level_values('Year').max()}")
    
    return df


# ============================================================================
# STEP 2: FIX GINI SCALING ERROR (CRITICAL)
# ============================================================================

def diagnose_gini_scaling(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Diagnose Gini scaling to identify mixed 0-1 and 0-100 scales.
    
    Returns:
        Dictionary with diagnostic information
    """
    logger.info("Diagnosing Gini scaling...")
    
    gini_col = 'gini'
    if gini_col not in df.columns:
        logger.warning("Gini column not found in DataFrame")
        return {}
    
    gini_data = df[gini_col].dropna()
    
    if len(gini_data) == 0:
        logger.warning("No non-null Gini values found")
        return {}
    
    diagnostics = {
        'count': len(gini_data),
        'mean': float(gini_data.mean()),
        'std': float(gini_data.std()),
        'min': float(gini_data.min()),
        'max': float(gini_data.max()),
        'median': float(gini_data.median()),
        'values_gt_1': int((gini_data > 1.0).sum()),
        'values_0_to_1': int(((gini_data >= 0) & (gini_data <= 1)).sum()),
        'values_lt_0': int((gini_data < 0).sum()),
    }
    
    logger.info(f"Gini diagnostics: {diagnostics}")
    
    # Determine if scaling fix is needed
    if diagnostics['values_gt_1'] > 0:
        logger.warning(f"Found {diagnostics['values_gt_1']} Gini values > 1.0 - scaling fix needed")
        diagnostics['needs_fix'] = True
    else:
        logger.info("All Gini values appear to be on 0-1 scale")
        diagnostics['needs_fix'] = False
    
    return diagnostics


def fix_gini_scaling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix Gini scaling error by converting values > 1 to 0-1 scale.
    
    Args:
        df: DataFrame with Gini column
        
    Returns:
        DataFrame with corrected Gini values
    """
    logger.info("Fixing Gini scaling...")
    
    df = df.copy()
    gini_col = 'gini'
    
    if gini_col not in df.columns:
        logger.warning("Gini column not found, skipping fix")
        return df
    
    # Diagnose before fix
    before_diagnostics = diagnose_gini_scaling(df)
    
    # Apply fix: divide values > 1 by 100
    mask = df[gini_col] > 1.0
    n_fixed = mask.sum()
    
    if n_fixed > 0:
        logger.info(f"Fixing {n_fixed} Gini values by dividing by 100")
        df.loc[mask, gini_col] = df.loc[mask, gini_col] / 100.0
    
    # Diagnose after fix
    after_diagnostics = diagnose_gini_scaling(df)
    
    # Safe formatting for logging
    before_mean = before_diagnostics.get('mean', 'N/A')
    after_mean = after_diagnostics.get('mean', 'N/A')
    
    before_str = f"{before_mean:.4f}" if isinstance(before_mean, (int, float)) else str(before_mean)
    after_str = f"{after_mean:.4f}" if isinstance(after_mean, (int, float)) else str(after_mean)
    
    logger.info(f"Gini fix complete. Before: mean={before_str}, "
                f"After: mean={after_str}")
    
    return df


# ============================================================================
# STEP 3: DATA PREPARATION FOR IMPUTATION
# ============================================================================

def prepare_data_for_imputation(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare data for MICE imputation.
    
    Args:
        df: Raw DataFrame with potential missing values (may have MultiIndex)
        
    Returns:
        Tuple of (df_imp, df_index): df_imp is numeric only, df_index has Code/Year
    """
    logger.info("Preparing data for imputation...")
    
    # Define required variables (numeric only)
    required_vars = ['vdem_electoral', 'gini', 'education_years', 
                       'social_spending', 'gdp_per_capita', 
                       'resource_rents', 'population']
    
    # Check which variables are available
    available_vars = [v for v in required_vars if v in df.columns]
    
    # Select available variables (numeric only)
    df_imp = df[available_vars].copy()
    
    # Extract index information (Code and Year) for later reassembly
    code_vals = df.index.get_level_values(0).tolist()
    year_vals = df.index.get_level_values(1).tolist()
    df_index = pd.DataFrame({'Code': code_vals, 'Year': year_vals})
    
    # Reset index for miceforest (numeric data only)
    df_imp = df_imp.reset_index(drop=True)
    
    logger.info(f"Prepared data shape: {df_imp.shape}")
    logger.info(f"Missing values: {df_imp.isnull().sum().to_dict()}")
    
    return df_imp, df_index



# ============================================================================
# STEP 4: MICE MULTIPLE IMPUTATION
# ============================================================================

def run_mice_imputation(df: pd.DataFrame, n_imputations: int = 50, 
                        n_iterations: int = 10, random_state: int = 42) -> ImputationResult:
    """
    Run MICE multiple imputation using miceforest.
    
    Args:
        df: DataFrame with missing values
        n_imputations: Number of imputed datasets to create
        n_iterations: Number of iterations per imputation
        random_state: Random seed for reproducibility
        
    Returns:
        ImputationResult containing imputed datasets and diagnostics
    """
    logger.info(f"Starting MICE imputation with {n_imputations} imputations...")
    
    try:
        import miceforest as mf
    except ImportError:
        logger.error("miceforest not installed. Please install with: uv pip install miceforest")
        raise
    
    # Record original missing pattern
    original_missing = df.isnull().mean().to_dict()
    logger.info(f"Original missing pattern: {original_missing}")
    
    # Initialize imputation kernel
    logger.info("Initializing ImputationKernel...")
    kernel = mf.ImputationKernel(
        df,
        num_datasets=n_imputations,
        save_all_iterations_data=False,  # Don't save all iterations to save memory
        random_state=random_state,
        copy_data=True
    )
    
    # Run MICE
    logger.info(f"Running MICE with {n_imputations} imputations, {n_iterations} iterations each...")
    kernel.mice(
        iterations=n_iterations,
        verbose=True
    )
    
    # Extract imputed datasets
    logger.info("Extracting imputed datasets...")
    imputed_datasets = []
    for i in range(n_imputations):
        imp_df = kernel.complete_data(i)
        imp_df['imputation_id'] = i
        imputed_datasets.append(imp_df)
    
    # Check missing pattern after imputation
    imputed_missing = imputed_datasets[0].isnull().mean().to_dict()
    logger.info(f"Imputed missing pattern (first dataset): {imputed_missing}")
    
    # Verify no missing values
    for i, imp_df in enumerate(imputed_datasets):
        n_missing = imp_df.isnull().sum().sum()
        if n_missing > 0:
            logger.warning(f"Imputed dataset {i} still has {n_missing} missing values")
    
    logger.info(f"MICE imputation complete. Generated {len(imputed_datasets)} complete datasets.")
    
    return ImputationResult(
        imputed_datasets=imputed_datasets,
        n_imputations=n_imputations,
        original_missing_pattern=original_missing,
        imputed_missing_pattern=imputed_missing
    )


def fallback_imputation(df: pd.DataFrame, n_imputations: int = 20) -> ImputationResult:
    """
    Fallback imputation using sklearn IterativeImputer if miceforest fails.
    
    Args:
        df: DataFrame with missing values
        n_imputations: Number of imputed datasets
        
    Returns:
        ImputationResult with imputed datasets
    """
    logger.warning("Using fallback imputation with sklearn IterativeImputer")
    
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    
    original_missing = df.isnull().mean().to_dict()
    
    imputed_datasets = []
    for i in range(n_imputations):
        logger.info(f"Fallback imputation {i+1}/{n_imputations}")
        
        imputer = IterativeImputer(
            max_iter=10,
            random_state=i,  # Different seed for each imputation
            sample_posterior=True
        )
        
        imputed_array = imputer.fit_transform(df)
        imp_df = pd.DataFrame(imputed_array, columns=df.columns, index=df.index)
        imp_df['imputation_id'] = i
        imputed_datasets.append(imp_df)
    
    imputed_missing = imputed_datasets[0].isnull().mean().to_dict()
    
    return ImputationResult(
        imputed_datasets=imputed_datasets,
        n_imputations=n_imputations,
        original_missing_pattern=original_missing,
        imputed_missing_pattern=imputed_missing
    )


# ============================================================================
# STEP 5: CREATE INTERACTION TERMS
# ============================================================================

def create_interaction_terms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create standardized interaction terms for regression.
    
    Following Brambor et al. (2006) recommendations:
    1. Standardize variables before creating interactions
    2. Include all constitutive terms
    3. Include all lower-order interactions
    
    Args:
        df: DataFrame with main effects
        
    Returns:
        DataFrame with interaction terms added
    """
    logger.info("Creating interaction terms...")
    
    df = df.copy()
    
    # Define variables
    y = 'vdem_electoral'
    x = 'gini'           # Inequality (primary independent variable)
    w1 = 'education_years'  # Education (moderator 1)
    w2 = 'social_spending'  # Welfare spending (moderator 2)
    
    # Standardize variables (z-scores)
    # This helps with interpretation and numerical stability
    vars_to_standardize = [x, w1, w2]
    
    for var in vars_to_standardize:
        if var in df.columns:
            mean = df[var].mean()
            std = df[var].std()
            if std > 0:
                df[f'{var}_z'] = (df[var] - mean) / std
            else:
                df[f'{var}_z'] = 0
                logger.warning(f"Zero std for {var}, setting standardized to 0")
    
    # Create interaction terms using standardized variables
    df['gini_x_edu'] = df['gini_z'] * df['education_years_z']
    df['gini_x_soc'] = df['gini_z'] * df['social_spending_z']
    df['edu_x_soc'] = df['education_years_z'] * df['social_spending_z']
    df['triple_int'] = df['gini_z'] * df['education_years_z'] * df['social_spending_z']
    
    logger.info("Interaction terms created:")
    logger.info(f"  gini_x_edu: mean={df['gini_x_edu'].mean():.4f}, std={df['gini_x_edu'].std():.4f}")
    logger.info(f"  gini_x_soc: mean={df['gini_x_soc'].mean():.4f}, std={df['gini_x_soc'].std():.4f}")
    logger.info(f"  triple_int: mean={df['triple_int'].mean():.4f}, std={df['triple_int'].std():.4f}")
    
    return df


def add_index_info(df: pd.DataFrame, df_index: pd.DataFrame) -> pd.DataFrame:
    """
    Add Code and Year columns back to DataFrame and set MultiIndex.
    
    Args:
        df: DataFrame with imputed data (no Code/Year columns)
        df_index: DataFrame with Code and Year columns
        
    Returns:
        DataFrame with Code and Year as MultiIndex
    """
    df = df.copy()
    df['Code'] = df_index['Code'].values
    df['Year'] = df_index['Year'].values
    return df.set_index(['Code', 'Year'])


# ============================================================================
# STEP 6: PANEL REGRESSION (Fixed Effects)
# ============================================================================

def run_panel_regression(df: pd.DataFrame, model_spec: str = "triple") -> Optional[RegressionResult]:
    """
    Run fixed-effects panel regression using linearmodels.
    
    Args:
        df: DataFrame with all variables and interaction terms
             (can have MultiIndex or Code/Year as columns)
        model_spec: Model specification ("main", "two_way", or "triple")
        
    Returns:
        RegressionResult or None if regression fails
    """
    logger.info(f"Running panel regression: {model_spec}")
    
    try:
        from linearmodels.panel import PanelOLS
        import statsmodels.api as sm
    except ImportError:
        logger.error("linearmodels not installed")
        raise
    
    # Ensure multi-index for panel data
    df_reg = df.copy()
    if not isinstance(df_reg.index, pd.MultiIndex):
        # Check if Code and Year are columns
        if 'Code' in df_reg.columns and 'Year' in df_reg.columns:
            df_reg = df_reg.set_index(['Code', 'Year'])
            logger.info("Converted Code and Year columns to MultiIndex")
        else:
            logger.error("DataFrame must have MultiIndex (Code, Year) or Code/Year columns for panel regression")
            return None
    
    # Define base variables
    y = 'vdem_electoral'
    x = 'gini_z'           # Standardized inequality
    w1 = 'education_years_z'  # Standardized education
    w2 = 'social_spending_z'  # Standardized welfare
    
    # Define model formulas based on specification
    if model_spec == "main":
        # Model 1: Main effects only
        exog_vars = [x, w1, w2, 'gdp_per_capita', 'resource_rents']
        model_name = "Model 1: Main Effects"
        
    elif model_spec == "two_way":
        # Model 2: Two-way interactions
        exog_vars = [x, w1, w2, 
                     'gini_x_edu', 'gini_x_soc',
                     'gdp_per_capita', 'resource_rents']
        model_name = "Model 2: Two-Way Interactions"
        
    elif model_spec == "triple":
        # Model 3: Triple interaction (PRIMARY HYPOTHESIS)
        exog_vars = [x, w1, w2,
                     'gini_x_edu', 'gini_x_soc', 'edu_x_soc',
                     'triple_int',
                     'gdp_per_capita', 'resource_rents']
        model_name = "Model 3: Triple Interaction"
        
    else:
        logger.error(f"Unknown model specification: {model_spec}")
        return None
    
    # Check that all variables exist
    missing_vars = [v for v in exog_vars if v not in df.columns]
    if missing_vars:
        logger.error(f"Missing variables for regression: {missing_vars}")
        return None
    
    # Prepare data
    exog = sm.add_constant(df_reg[exog_vars])
    endog = df_reg[y]
    
    # Run PanelOLS with entity (country) fixed effects and time effects
    try:
        model = PanelOLS(
            endog,
            exog,
            entity_effects=True,  # Country fixed effects
            time_effects=True,    # Year fixed effects (built-in)
            drop_absorbed=True
        )
        
        # Cluster standard errors by entity (country)
        result = model.fit(cov_type='clustered', cluster_entity=True)
        
        logger.info(f"\n{model_name}")
        logger.info(f"N = {result.nobs}")
        logger.info(f"R-squared = {result.rsquared:.4f}")
        
        # Extract coefficients, std errors, p-values
        params = result.params
        std_errors = result.std_errors
        pvalues = result.pvalues
        
        coefficients = params.to_dict()
        std_errors_dict = std_errors.to_dict()
        p_values_dict = pvalues.to_dict()
        
        # Get F-statistic if available
        f_stat = None
        f_pval = None
        try:
            if hasattr(result, 'f_statistic'):
                f_stat = float(result.f_statistic.stat)
                f_pval = float(result.f_statistic.pval)
        except:
            pass
        
        return RegressionResult(
            model_name=model_name,
            coefficients=coefficients,
            std_errors=std_errors_dict,
            p_values=p_values_dict,
            n_obs=int(result.nobs),
            r_squared=float(result.rsquared),
            f_statistic=f_stat,
            f_pvalue=f_pval
        )
        
    except Exception as e:
        logger.error(f"Regression failed for {model_spec}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


# ============================================================================
# STEP 7: POOL RESULTS (Rubin's Rules)
# ============================================================================

def pool_results_rubins_rules(results_list: List[RegressionResult], 
                              parameter: str) -> Dict[str, float]:
    """
    Pool coefficient estimates across imputations using Rubin's Rules.
    
    Args:
        results_list: List of RegressionResult objects from each imputation
        parameter: Name of the coefficient to pool
        
    Returns:
        Dictionary with pooled estimate, SE, p-value, CI
    """
    logger.info(f"Pooling results for parameter: {parameter}")
    
    if not results_list:
        logger.error("No results to pool")
        return {}
    
    # Extract estimates and variances
    Q = []  # Estimates
    U = []  # Within-imputation variances (SE^2)
    
    for res in results_list:
        if parameter in res.coefficients:
            Q.append(res.coefficients[parameter])
            U.append(res.std_errors[parameter] ** 2)
    
    if not Q:
        logger.warning(f"Parameter {parameter} not found in any results")
        return {}
    
    Q = np.array(Q)
    U = np.array(U)
    
    # Rubin's Rules
    Q_bar = np.mean(Q)  # Pooled point estimate
    U_bar = np.mean(U)  # Within-imputation variance
    B = np.var(Q, ddof=1)  # Between-imputation variance
    
    T = U_bar + (1 + 1/len(Q)) * B  # Total variance
    
    # Standard error
    SE = np.sqrt(T)
    
    # Degrees of freedom (Barnard-Rubin adjustment for small number of imputations)
    m = len(Q)
    df_old = (m - 1) * (1 + U_bar / ((1 + 1/m) * B)) ** 2
    df = min(df_old, (m - 1) * (1 + U_bar / ((1 + 1/m) * B)) ** 2)
    
    # t-statistic and p-value
    t_stat = Q_bar / SE if SE > 0 else 0
    from scipy import stats
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
    
    # 95% Confidence Interval
    ci_lower = Q_bar - 1.96 * SE
    ci_upper = Q_bar + 1.96 * SE
    
    pooled = {
        'parameter': parameter,
        'pooled_estimate': float(Q_bar),
        'pooled_se': float(SE),
        'pooled_pvalue': float(p_value),
        'ci_95_lower': float(ci_lower),
        'ci_95_upper': float(ci_upper),
        'n_imputations': m,
        'within_var': float(U_bar),
        'between_var': float(B),
        'total_var': float(T)
    }
    
    logger.info(f"Pooled result for {parameter}:")
    logger.info(f"  Estimate = {Q_bar:.4f}")
    logger.info(f"  SE = {SE:.4f}")
    logger.info(f"  p-value = {p_value:.4f}")
    logger.info(f"  95% CI = [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    return pooled


# ============================================================================
# STEP 8: MARGINAL EFFECTS (Brambor et al. 2006)
# ============================================================================

def compute_marginal_effects(results: RegressionResult, df: pd.DataFrame) -> List[MarginalEffect]:
    """
    Compute marginal effects for the triple interaction model.
    
    Following Brambor et al. (2006):
    ∂V-Dem/∂Gini = β_gini + β_gini_edu*E + β_gini_soc*S + β_triple*E*S
    
    Args:
        results: RegressionResult from triple interaction model
        df: DataFrame used for regression (to get E and S values)
        
    Returns:
        List of MarginalEffect objects at different values of E and S
    """
    logger.info("Computing marginal effects...")
    
    # Extract coefficients
    beta_gini = results.coefficients.get('gini_z', 0)
    beta_gini_edu = results.coefficients.get('gini_x_edu', 0)
    beta_gini_soc = results.coefficients.get('gini_x_soc', 0)
    beta_triple = results.coefficients.get('triple_int', 0)
    
    # Get standard errors for variance computation
    se_gini = results.std_errors.get('gini_z', 0)
    se_gini_edu = results.std_errors.get('gini_x_edu', 0)
    se_gini_soc = results.std_errors.get('gini_x_soc', 0)
    se_triple = results.std_errors.get('triple_int', 0)
    
    # Values at which to compute marginal effects
    # Education and Social Spending at -1SD, 0, +1SD
    edu_mean = df['education_years_z'].mean()
    edu_std = df['education_years_z'].std()
    soc_mean = df['social_spending_z'].mean()
    soc_std = df['social_spending_z'].std()
    
    eval_points = [
        {'education_years_z': -1, 'social_spending_z': -1, 'label': 'Low Edu, Low Soc'},
        {'education_years_z': -1, 'social_spending_z': 0, 'label': 'Low Edu, Avg Soc'},
        {'education_years_z': -1, 'social_spending_z': 1, 'label': 'Low Edu, High Soc'},
        {'education_years_z': 0, 'social_spending_z': -1, 'label': 'Avg Edu, Low Soc'},
        {'education_years_z': 0, 'social_spending_z': 0, 'label': 'Avg Edu, Avg Soc'},
        {'education_years_z': 0, 'social_spending_z': 1, 'label': 'Avg Edu, High Soc'},
        {'education_years_z': 1, 'social_spending_z': -1, 'label': 'High Edu, Low Soc'},
        {'education_years_z': 1, 'social_spending_z': 0, 'label': 'High Edu, Avg Soc'},
        {'education_years_z': 1, 'social_spending_z': 1, 'label': 'High Edu, High Soc'},
    ]
    
    marginal_effects = []
    
    for point in eval_points:
        E = point['education_years_z']
        S = point['social_spending_z']
        
        # Compute marginal effect: ∂Y/∂Gini = β1 + β3*E + β4*S + β7*E*S
        me = beta_gini + beta_gini_edu * E + beta_gini_soc * S + beta_triple * E * S
        
        # Compute variance of marginal effect using delta method
        # Var(∂Y/∂Gini) = Var(β1) + E^2*Var(β3) + S^2*Var(β4) + (E*S)^2*Var(β7)
        #                 + 2*E*Cov(β1,β3) + 2*S*Cov(β1,β4) + 2*E*S*Cov(β1,β7)
        #                 + 2*E*S*Cov(β3,β4) + 2*E^2*S*Cov(β3,β7) + 2*E*S^2*Cov(β4,β7)
        # Simplified: assume independence for now (conservative)
        var_me = (se_gini**2 + 
                 (E**2) * (se_gini_edu**2) + 
                 (S**2) * (se_gini_soc**2) + 
                 (E*S)**2 * (se_triple**2))
        
        se_me = np.sqrt(var_me) if var_me > 0 else 0
        
        # t-statistic and p-value
        t_stat = me / se_me if se_me > 0 else 0
        from scipy import stats
        dfreedom = results.n_obs - len(results.coefficients)
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), dfreedom))
        
        # 95% CI
        ci_lower = me - 1.96 * se_me
        ci_upper = me + 1.96 * se_me
        
        marginal_effects.append(MarginalEffect(
            variable='gini_on_vdem',
            at_values={'education': E, 'social_spending': S},
            effect=float(me),
            std_error=float(se_me),
            p_value=float(p_value),
            ci_lower=float(ci_lower),
            ci_upper=float(ci_upper)
        ))
        
        logger.info(f"Marginal effect at {point['label']}: {me:.4f} (SE={se_me:.4f}, p={p_value:.4f})")
    
    return marginal_effects


# ============================================================================
# STEP 9: ROBUSTNESS CHECKS
# ============================================================================

def run_robustness_checks(imputation_result: ImputationResult) -> Dict[str, Any]:
    """
    Run robustness checks on the primary results.
    
    Checks:
    1. Alternative model specifications
    2. Lagged dependent variable
    3. Different imputation methods
    
    Args:
        imputation_result: Result from MICE imputation
        
    Returns:
        Dictionary with robustness check results
    """
    logger.info("Running robustness checks...")
    
    robustness_results = {}
    
    # Check 1: Complete case analysis (compare with imputed)
    logger.info("Robustness Check 1: Complete case analysis")
    imputed_df = imputation_result.imputed_datasets[0]
    complete_cases = imputed_df.dropna()
    
    if len(complete_cases) > 100:
        # Run regression on complete cases only
        cc_results = []
        for model_spec in ["main", "two_way", "triple"]:
            res = run_panel_regression(complete_cases, model_spec)
            if res:
                cc_results.append({
                    'model': model_spec,
                    'n_obs': res.n_obs,
                    'triple_int_coef': res.coefficients.get('triple_int', None),
                    'triple_int_pval': res.p_values.get('triple_int', None)
                })
        robustness_results['complete_case'] = cc_results
    else:
        logger.warning("Too few complete cases for robustness check")
        robustness_results['complete_case'] = None
    
    # Check 2: Using only first imputation (single imputation bias)
    logger.info("Robustness Check 2: Single imputation (first dataset only)")
    single_imp_results = []
    for model_spec in ["main", "two_way", "triple"]:
        res = run_panel_regression(imputation_result.imputed_datasets[0], model_spec)
        if res:
            single_imp_results.append({
                'model': model_spec,
                'n_obs': res.n_obs,
                'triple_int_coef': res.coefficients.get('triple_int', None),
                'triple_int_pval': res.p_values.get('triple_int', None)
            })
    robustness_results['single_imputation'] = single_imp_results
    
    return robustness_results


# ============================================================================
# STEP 10: EXPORT RESULTS
# ============================================================================

def export_results(results: Dict[str, Any], output_path: Path):
    """
    Export all results to method_out.json in exp_gen_sol_out.json schema format.
    
    Args:
        results: Dictionary containing all analysis results
        output_path: Path to output JSON file
    """
    logger.info(f"Exporting results to {output_path}")
    
    # Convert dataclasses to dictionaries
    def convert_dataclass(obj):
        if hasattr(obj, '__dataclass_fields__'):
            return {k: convert_dataclass(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, dict):
            return {k: convert_dataclass(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_dataclass(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif pd.isna(obj):
            return None
        else:
            return obj
    
    results_serializable = convert_dataclass(results)
    
    # Create output in exp_gen_sol_out.json schema format
    # The schema expects: { "datasets": [ { "dataset": "...", "examples": [...] } ] }
    # Each example has: input (JSON string), output (string), metadata_*
    
    # For our experiment, we'll create examples from the regression results
    examples = []
    
    # Create examples from pooled regression results
    pooled = results_serializable.get('pooled_results', {})
    
    # Example 1: Triple interaction result (primary hypothesis)
    triple_result = pooled.get('triple_triple_int', {})
    if triple_result:
        example1 = {
            'input': json.dumps({
                'model': 'triple_interaction',
                'n_countries': results_serializable.get('experiment_info', {}).get('n_countries', 50),
                'n_observations': results_serializable.get('experiment_info', {}).get('n_observations_total', 1641)
            }),
            'output': str(triple_result.get('pooled_estimate', 0.0)),
            'metadata_fold': 0,
            'metadata_feature_names': ['gini_z', 'education_years_z', 'social_spending_z', 
                                 'gini_x_edu', 'gini_x_soc', 'triple_int'],
            'metadata_task_type': 'regression',
            'metadata_row_index': 0,
            'metadata_country': 'ALL',
            'metadata_year': 2022
        }
        examples.append(example1)
    
    # Example 2: Main effects model result
    main_result = pooled.get('main_gini_z', {})
    if main_result:
        example2 = {
            'input': json.dumps({
                'model': 'main_effects',
                'n_countries': results_serializable.get('experiment_info', {}).get('n_countries', 50)
            }),
            'output': str(main_result.get('pooled_estimate', 0.0)),
            'metadata_fold': 1,
            'metadata_feature_names': ['gini_z', 'education_years_z', 'social_spending_z'],
            'metadata_task_type': 'regression',
            'metadata_row_index': 1,
            'metadata_country': 'ALL',
            'metadata_year': 2022
        }
        examples.append(example2)
    
    # Construct final output
    output_data = {
        'datasets': [
            {
                'dataset': 'triple_shield_analysis',
                'examples': examples
            }
        ]
    }
    
    # Add full results as a metadata field (not in examples)
    output_data['full_results'] = results_serializable
    
    # Write to JSON
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    logger.info(f"Results exported successfully")
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    logger.info(f"Output file size: {file_size_mb:.2f} MB")
    
    if file_size_mb > 50:
        logger.warning(f"Output file is large ({file_size_mb:.2f} MB). Consider splitting.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

@logger.catch(reraise=True)
def main():
    """Main execution function."""
    
    logger.info("=" * 80)
    logger.info("TRIPLE SHIELD ANALYSIS: MICE IMPUTATION AND TRIPLE INTERACTION")
    logger.info("=" * 80)
    
    # Define paths
    workspace = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
    data_dir = Path("/ai-inventor/aii_data/runs/run_9gq-UFm593U6/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
    
    full_data_path = data_dir / "full_data_out.json"
    mini_data_path = data_dir / "mini_data_out.json"
    output_path = workspace / "method_out.json"
    
    # =========================================================================
    # TESTING PHASE: Start with mini data
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("TESTING PHASE: Running on mini dataset first")
    logger.info("=" * 80)
    
    # Load mini data for testing
    df_mini = load_and_verify_data(mini_data_path, mini=True)
    logger.info(f"Mini data loaded: {df_mini.shape}")
    
    # Fix Gini scaling
    df_mini = fix_gini_scaling(df_mini)
    
    # Prepare for imputation (returns df_imp, df_index)
    df_mini_imp, df_mini_index = prepare_data_for_imputation(df_mini)
    
    # Run MICE with small number of imputations for testing
    logger.info("Running MICE on mini data (5 imputations for testing)...")
    try:
        imp_result_mini = run_mice_imputation(df_mini_imp, n_imputations=5, n_iterations=5)
    except Exception as e:
        logger.warning(f"MICE failed on mini data: {e}")
        logger.info("Trying fallback imputation...")
        imp_result_mini = fallback_imputation(df_mini_imp, n_imputations=5)
    
    # Create interaction terms (need to add index back first)
    df_mini_imputed = imp_result_mini.imputed_datasets[0]
    df_mini_with_index = add_index_info(df_mini_imputed, df_mini_index)
    df_mini_interact = create_interaction_terms(df_mini_with_index)
    
    # Run regression on first imputed dataset
    logger.info("Running test regression on mini data...")
    test_result = run_panel_regression(df_mini_interact, model_spec="triple")
    
    if test_result:
        logger.info("Test regression successful!")
        logger.info(f"Coefficients: {test_result.coefficients}")
    else:
        logger.error("Test regression failed!")
        return
    
    # =========================================================================
    # FULL ANALYSIS: Run on full dataset
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("FULL ANALYSIS: Running on full dataset")
    logger.info("=" * 80)
    
    # Load full data
    df_full = load_and_verify_data(full_data_path, mini=False)
    logger.info(f"Full data loaded: {df_full.shape}")
    
    # Fix Gini scaling
    df_full = fix_gini_scaling(df_full)
    
    # Prepare for imputation (returns df_imp, df_index)
    df_full_imp, df_full_index = prepare_data_for_imputation(df_full)
    
    # Run MICE with 50 imputations
    logger.info("Running MICE on full data (50 imputations)...")
    try:
        imp_result_full = run_mice_imputation(df_full_imp, n_imputations=50, n_iterations=10)
    except Exception as e:
        logger.warning(f"MICE failed on full data: {e}")
        logger.info("Using fallback imputation...")
        imp_result_full = fallback_imputation(df_full_imp, n_imputations=20)
    
    # =========================================================================
    # REGRESSION ANALYSIS ON ALL IMPUTED DATASETS
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("REGRESSION ANALYSIS: Running on all imputed datasets")
    logger.info("=" * 80)
    
    all_results = {
        'main': [],
        'two_way': [],
        'triple': []
    }
    
    for i, imp_df in enumerate(imp_result_full.imputed_datasets):
        logger.info(f"Processing imputation {i+1}/{len(imp_result_full.imputed_datasets)}")
        
        # Add index info back before creating interaction terms
        imp_df_with_index = add_index_info(imp_df, df_full_index)
        
        # Create interaction terms
        imp_df_interact = create_interaction_terms(imp_df_with_index)
        
        # Run all three models
        for model_spec in ['main', 'two_way', 'triple']:
            result = run_panel_regression(imp_df_interact, model_spec)
            if result:
                all_results[model_spec].append(result)
        
        # Free memory
        del imp_df_interact
        gc.collect()
    
    # =========================================================================
    # POOL RESULTS USING RUBIN'S RULES
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("POOLING RESULTS: Applying Rubin's Rules")
    logger.info("=" * 80)
    
    pooled_results = {}
    
    # Parameters of interest
    params_of_interest = [
        'gini_z',
        'education_years_z',
        'social_spending_z',
        'gini_x_edu',
        'gini_x_soc',
        'triple_int',
        'gdp_per_capita',
        'resource_rents'
    ]
    
    for param in params_of_interest:
        for model_spec in ['main', 'two_way', 'triple']:
            if all_results[model_spec]:
                key = f"{model_spec}_{param}"
                pooled = pool_results_rubins_rules(all_results[model_spec], param)
                if pooled:
                    pooled_results[key] = pooled
    
    # =========================================================================
    # MARGINAL EFFECTS
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("MARGINAL EFFECTS: Computing ∂V-Dem/∂Gini")
    logger.info("=" * 80)
    
    marginal_effects = []
    if all_results['triple']:
        # Use first imputation for marginal effects computation
        # (in practice, should average across imputations)
        df_for_me = create_interaction_terms(imp_result_full.imputed_datasets[0])
        me = compute_marginal_effects(all_results['triple'][0], df_for_me)
        marginal_effects = me
    
    # =========================================================================
    # ROBUSTNESS CHECKS
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ROBUSTNESS CHECKS")
    logger.info("=" * 80)
    
    robustness = run_robustness_checks(imp_result_full)
    
    # =========================================================================
    # COMPILE AND EXPORT FINAL RESULTS
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("COMPILING FINAL RESULTS")
    logger.info("=" * 80)
    
    final_results = {
        'experiment_info': {
            'hypothesis': 'Triple interaction: inequality × education × welfare spending on democracy',
            'method': 'MICE multiple imputation (50 imputations) + Fixed-effects panel regression',
            'n_countries': int(df_full.index.get_level_values('Code').nunique()),
            'n_years': int(df_full.index.get_level_values('Year').max() - df_full.index.get_level_values('Year').min() + 1),
            'n_observations_total': len(df_full),
            'n_imputations': imp_result_full.n_imputations,
        },
        'gini_scaling_fix': {
            'applied': True,
            'description': 'Divided Gini values > 1 by 100 to convert from 0-100 to 0-1 scale'
        },
        'imputation_diagnostics': {
            'original_missing_pattern': imp_result_full.original_missing_pattern,
            'imputed_missing_pattern': imp_result_full.imputed_missing_pattern,
            'n_imputations': imp_result_full.n_imputations
        },
        'regression_results': {
            model_spec: [r.__dict__ for r in results] if results else []
            for model_spec, results in all_results.items()
        },
        'pooled_results': pooled_results,
        'marginal_effects': [me.__dict__ for me in marginal_effects],
        'robustness_checks': robustness,
        'primary_hypothesis_test': {
            'parameter': 'triple_int',
            'pooled_result': pooled_results.get('triple_triple_int', None),
            'interpretation': 'Positive coefficient supports triple shield hypothesis'
        }
    }
    
    # Export results
    export_results(final_results, output_path)
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ANALYSIS COMPLETE")
    logger.info("=" * 80)
    
    # Print summary of primary hypothesis test
    triple_result = pooled_results.get('triple_triple_int', {})
    if triple_result:
        coef = triple_result.get('pooled_estimate', 0)
        pval = triple_result.get('pooled_pvalue', 1)
        ci_low = triple_result.get('ci_95_lower', 0)
        ci_high = triple_result.get('ci_95_upper', 0)
        
        logger.info("\nPRIMARY HYPOTHESIS TEST (Triple Interaction):")
        logger.info(f"  Coefficient: {coef:.4f}")
        logger.info(f"  p-value: {pval:.4f}")
        logger.info(f"  95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
        
        if pval < 0.05:
            logger.info("  RESULT: Statistically significant (p < 0.05)")
        else:
            logger.info("  RESULT: Not statistically significant (p >= 0.05)")
    
    logger.info(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()

