def classify_variable(series):
    """
    Classify a variable as Nominal, Ordinal, or Scale.
    - Nominal: Strings, booleans, or objects.
    - Ordinal: Discrete numeric (integers) with max 4 unique values.
    - Scale: Numeric with more than 4 unique values.
    """
    import pandas as pd
    import numpy as np

    non_null = series.dropna()
    if non_null.empty:
        return "Nominal"

    unique_count = non_null.nunique()
    is_numeric = pd.api.types.is_numeric_dtype(series)
    is_integer = pd.api.types.is_integer_dtype(series) or (is_numeric and np.all(non_null % 1 == 0))

    if not is_numeric:
        return "Nominal"

    if is_integer and unique_count <= 4:
        return "Ordinal"

    return "Scale"

def descriptives(df, vars_list):
    """Calculate descriptive statistics with variable classification."""
    import numpy as np
    import pandas as pd
    results = []
    for var in vars_list:
        series = df[var]
        data = series.dropna()
        if data.empty:
            continue

        var_type = classify_variable(series)

        # Calculate mode separately as it applies to all types
        mode_val = data.mode()
        mode_str = str(mode_val.iloc[0]) if not mode_val.empty else "N/A"

        desc = {
            'Variable': f"{var}*" if var_type == "Ordinal" else var,
            'Type': var_type,
            'N': len(data),
            'Mean': np.mean(data) if var_type != "Nominal" else "N/A",
            'Median': np.median(data) if var_type != "Nominal" else "N/A",
            'Std. Deviation': np.std(data, ddof=1) if var_type != "Nominal" else "N/A",
            'Minimum': np.min(data) if var_type != "Nominal" else "N/A",
            'Maximum': np.max(data) if var_type != "Nominal" else "N/A",
            'Mode': mode_str
        }
        results.append(desc)
    return pd.DataFrame(results)

def ttest_one_sample(df, var, test_value=0):
    """Perform a one-sample t-test."""
    import numpy as np
    from scipy import stats
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
    import numpy as np
    from scipy import stats
    groups = df[group_var].unique()
    if len(groups) != 2:
        raise ValueError(f"Grouping variable '{group_var}' must have exactly two levels. Found: {groups}")

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
    import numpy as np
    from scipy import stats
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

def anova_oneway(df, var, group_var):
    """Perform a one-way ANOVA with Post-Hoc comparisons."""
    import numpy as np
    from scipy import stats
    import pandas as pd
    from itertools import combinations

    # Clean data
    clean_df = df[[var, group_var]].dropna()
    groups = sorted(clean_df[group_var].unique())
    num_groups = len(groups)

    if num_groups < 2:
        raise ValueError(f"ANOVA requires at least 2 groups. Found: {num_groups}")

    # Prepare data groups
    data_groups = [clean_df[clean_df[group_var] == g][var] for g in groups]
    n_groups = [len(g) for g in data_groups]

    if any(n < 1 for n in n_groups):
         raise ValueError("One or more groups are empty.")
    if any(n < 2 for n in n_groups):
         # Technically ANOVA can run with n=1 in some groups as long as df_error > 0,
         # but post-hoc comparisons might be problematic.
         # For robustness, we'll proceed if total df_error > 0.
         pass

    # Global ANOVA
    f_stat, p_val = stats.f_oneway(*data_groups)

    # Manual calculations for MS_error and SS
    all_data = clean_df[var]
    grand_mean = all_data.mean()
    total_n = len(all_data)

    ss_between = sum(n * (g.mean() - grand_mean)**2 for n, g in zip(n_groups, data_groups))
    ss_total = sum((all_data - grand_mean)**2)
    ss_error = ss_total - ss_between

    df_between = num_groups - 1
    df_error = total_n - num_groups

    if df_error <= 0:
        raise ValueError("Not enough degrees of freedom to calculate error variance.")

    ms_between = ss_between / df_between
    ms_error = ss_error / df_error

    global_results = {
        'Variable': var,
        'Grouping': group_var,
        'SS Between': ss_between,
        'df Between': df_between,
        'MS Between': ms_between,
        'SS Error': ss_error,
        'df Error': df_error,
        'MS Error': ms_error,
        'F': f_stat,
        'p': p_val
    }

    post_hoc_results = []
    if num_groups > 2:
        pairs = list(combinations(groups, 2))
        num_comparisons = len(pairs)

        for g1, g2 in pairs:
            d1 = clean_df[clean_df[group_var] == g1][var]
            d2 = clean_df[clean_df[group_var] == g2][var]

            mean_diff = d1.mean() - d2.mean()
            n1, n2 = len(d1), len(d2)

            # Standard error using pooled MS_error from the global model
            se = np.sqrt(ms_error * (1/n1 + 1/n2))
            t_val = mean_diff / se if se > 0 else 0

            # P-value (two-tailed) from t-distribution with df_error
            p_raw = 2 * (1 - stats.t.cdf(abs(t_val), df_error))
            p_bonf = min(1.0, p_raw * num_comparisons)

            # Cohen's d using root(MS_error) as specified
            d_cohen = mean_diff / np.sqrt(ms_error) if ms_error > 0 else 0

            post_hoc_results.append({
                'Grupo 1': g1,
                'Grupo 2': g2,
                'Diferencia de Medias': mean_diff,
                'Error Típico': se,
                't': t_val,
                'p (bonf)': p_bonf,
                'd de Cohen': d_cohen
            })

    return {
        'global': global_results,
        'post_hoc': post_hoc_results
    }

def correlation(df, vars_list):
    """Calculate Pearson correlation matrix."""
    import pandas as pd
    temp_df = df[vars_list].dropna()
    corr_matrix = temp_df.corr()
    return corr_matrix

def linear_regression(df, dep_var, indep_vars):
    """Perform a simple/multiple linear regression."""
    from scipy import stats
    if isinstance(indep_vars, str):
        indep_vars = [indep_vars]

    temp_df = df[[dep_var] + indep_vars].dropna()
    y = temp_df[dep_var]
    X = temp_df[indep_vars]

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
        raise NotImplementedError("Multiple regression not yet implemented.")
