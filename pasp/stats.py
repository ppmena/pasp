import numpy as np
from scipy import stats
import pandas as pd

def descriptives(df, vars_list):
    """Calculate descriptive statistics for a list of variables."""
    results = []
    for var in vars_list:
        data = df[var].dropna()
        if data.empty:
            continue

        desc = {
            'Variable': var,
            'N': len(data),
            'Mean': np.mean(data),
            'Median': np.median(data),
            'Std. Deviation': np.std(data, ddof=1),
            'Minimum': np.min(data),
            'Maximum': np.max(data),
            'Skewness': data.skew(),
            'Kurtosis': data.kurtosis()
        }
        results.append(desc)
    return pd.DataFrame(results)

def ttest_one_sample(df, var, test_value=0):
    """Perform a one-sample t-test."""
    data = df[var].dropna()
    t_stat, p_val = stats.ttest_1samp(data, test_value)

    # Calculate Cohen's d
    d = (np.mean(data) - test_value) / np.std(data, ddof=1)

    return {
        'Variable': var,
        'Test Value': test_value,
        't': t_stat,
        'df': len(data) - 1,
        'p': p_val,
        'Mean Difference': np.mean(data) - test_value,
        "Cohen's d": d
    }

def ttest_independent(df, var, group_var):
    """Perform an independent samples t-test."""
    groups = df[group_var].unique()
    if len(groups) != 2:
        raise ValueError("Grouping variable must have exactly two levels.")

    g1_data = df[df[group_var] == groups[0]][var].dropna()
    g2_data = df[df[group_var] == groups[1]][var].dropna()

    t_stat, p_val = stats.ttest_ind(g1_data, g2_data)

    # Calculate Cohen's d (pooled std dev)
    n1, n2 = len(g1_data), len(g2_data)
    v1, v2 = np.var(g1_data, ddof=1), np.var(g2_data, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    d = (np.mean(g1_data) - np.mean(g2_data)) / pooled_std

    return {
        'Variable': var,
        'Group 1': groups[0],
        'Group 2': groups[1],
        't': t_stat,
        'df': n1 + n2 - 2,
        'p': p_val,
        'Mean Difference': np.mean(g1_data) - np.mean(g2_data),
        "Cohen's d": d
    }

def ttest_paired(df, var1, var2):
    """Perform a paired samples t-test."""
    temp_df = df[[var1, var2]].dropna()
    g1_data = temp_df[var1]
    g2_data = temp_df[var2]

    t_stat, p_val = stats.ttest_rel(g1_data, g2_data)

    # Cohen's d for paired samples
    diff = g1_data - g2_data
    d = np.mean(diff) / np.std(diff, ddof=1)

    return {
        'Variables': f"{var1} - {var2}",
        't': t_stat,
        'df': len(temp_df) - 1,
        'p': p_val,
        'Mean Difference': np.mean(diff),
        "Cohen's d": d
    }

def linear_regression(df, dep_var, indep_vars):
    """Perform a simple/multiple linear regression."""
    # For now, simple linear regression (one indep var)
    if isinstance(indep_vars, str):
        indep_vars = [indep_vars]

    temp_df = df[[dep_var] + indep_vars].dropna()
    y = temp_df[dep_var]
    X = temp_df[indep_vars]

    # Use scipy for simple linear regression or we could use statsmodels if we wanted more detail
    # Given the goal of being lightweight, we'll stick with scipy or numpy for now

    if len(indep_vars) == 1:
        x = X.iloc[:, 0]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        return {
            'Dependent': dep_var,
            'Independent': indep_vars[0],
            'R': r_value,
            'R-squared': r_value**2,
            'Intercept': intercept,
            'Slope': slope,
            'p-value': p_value,
            'Std.Error': std_err
        }
    else:
        # Multiple regression would need a different approach (e.g. np.linalg.lstsq)
        raise NotImplementedError("Multiple regression not yet implemented.")
