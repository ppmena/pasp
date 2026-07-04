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

def check_normality(data):
    """Check for normality using Shapiro-Wilk test."""
    from scipy import stats
    if len(data) < 3:
        return True, 1.0
    stat, p = stats.shapiro(data)
    return p > 0.05, p

def check_homogeneity(groups):
    """Check for homogeneity of variance using Levene's test."""
    from scipy import stats
    stat, p = stats.levene(*groups)
    return p > 0.05, p

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
    """Perform a one-sample t-test or Wilcoxon signed-rank test."""
    import numpy as np
    from scipy import stats
    data = df[var].dropna()

    is_normal, p_norm = check_normality(data)

    if is_normal:
        test_name = "One-sample T-Test"
        t_stat, p_val = stats.ttest_1samp(data, test_value)
        es = (np.mean(data) - test_value) / np.std(data, ddof=1)
    else:
        test_name = "Wilcoxon Signed-Rank Test"
        diff = data - test_value
        t_stat, p_val = stats.wilcoxon(diff)
        es = t_stat / (len(data) * (len(data) + 1) / 2)

    return {
        'Test': test_name,
        'Variable': var,
        'Test Value': test_value,
        'Stat': t_stat,
        'df': len(data) - 1 if is_normal else "N/A",
        'p': p_val,
        'Effect Size': es,
        'Normality p': p_norm
    }

def ttest_independent(df, var, group_var):
    """Perform an independent samples t-test, Welch's t-test, or Mann-Whitney U test."""
    import numpy as np
    from scipy import stats
    groups = df[group_var].unique()
    if len(groups) != 2:
        raise ValueError(f"Grouping variable '{group_var}' must have exactly two levels. Found: {groups}")

    g1_data = df[df[group_var] == groups[0]][var].dropna()
    g2_data = df[df[group_var] == groups[1]][var].dropna()

    norm1, p_norm1 = check_normality(g1_data)
    norm2, p_norm2 = check_normality(g2_data)
    homog, p_homog = check_homogeneity([g1_data, g2_data])

    if norm1 and norm2:
        if homog:
            test_name = "Independent Samples T-Test"
            t_stat, p_val = stats.ttest_ind(g1_data, g2_data)
            df_val = len(g1_data) + len(g2_data) - 2
        else:
            test_name = "Welch's T-Test"
            t_stat, p_val = stats.ttest_ind(g1_data, g2_data, equal_var=False)
            v1, v2 = np.var(g1_data, ddof=1), np.var(g2_data, ddof=1)
            n1, n2 = len(g1_data), len(g2_data)
            df_val = (v1/n1 + v2/n2)**2 / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))

        n1, n2 = len(g1_data), len(g2_data)
        v1, v2 = np.var(g1_data, ddof=1), np.var(g2_data, ddof=1)
        pooled_std = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
        es = (np.mean(g1_data) - np.mean(g2_data)) / pooled_std
    else:
        test_name = "Mann-Whitney U Test"
        t_stat, p_val = stats.mannwhitneyu(g1_data, g2_data)
        df_val = "N/A"
        es = t_stat / (len(g1_data) * len(g2_data))

    return {
        'Test': test_name,
        'Variable': var,
        'Group 1': groups[0],
        'Group 2': groups[1],
        'Stat': t_stat,
        'df': df_val,
        'p': p_val,
        'Effect Size': es,
        'Normality p (G1)': p_norm1,
        'Normality p (G2)': p_norm2,
        'Homogeneity p': p_homog
    }

def ttest_paired(df, var1, var2):
    """Perform a paired samples t-test or Wilcoxon signed-rank test."""
    import numpy as np
    from scipy import stats
    temp_df = df[[var1, var2]].dropna()
    g1_data = temp_df[var1]
    g2_data = temp_df[var2]
    diff = g1_data - g2_data

    is_normal, p_norm = check_normality(diff)

    if is_normal:
        test_name = "Paired Samples T-Test"
        t_stat, p_val = stats.ttest_rel(g1_data, g2_data)
        d = np.mean(diff) / np.std(diff, ddof=1)
    else:
        test_name = "Wilcoxon Signed-Rank Test (Paired)"
        t_stat, p_val = stats.wilcoxon(g1_data, g2_data)
        d = t_stat / (len(diff) * (len(diff) + 1) / 2)

    return {
        'Test': test_name,
        'Variables': f"{var1} - {var2}",
        'Stat': t_stat,
        'df': len(temp_df) - 1 if is_normal else "N/A",
        'p': p_val,
        'Effect Size': d,
        'Normality p (diff)': p_norm
    }

def anova_oneway(df, var, group_var):
    """Perform a one-way ANOVA, Welch's ANOVA, or Kruskal-Wallis test."""
    import numpy as np
    from scipy import stats
    import pandas as pd
    from itertools import combinations

    clean_df = df[[var, group_var]].dropna()
    groups = sorted(clean_df[group_var].unique())
    num_groups = len(groups)

    if num_groups < 2:
        raise ValueError(f"ANOVA requires at least 2 groups. Found: {num_groups}")

    data_groups = [clean_df[clean_df[group_var] == g][var] for g in groups]

    normality_results = [check_normality(g) for g in data_groups]
    all_normal = all(r[0] for r in normality_results)
    homog, p_homog = check_homogeneity(data_groups)

    if all_normal:
        if homog:
            test_name = "One-way ANOVA"
            f_stat, p_val = stats.f_oneway(*data_groups)

            all_data = clean_df[var]
            grand_mean = all_data.mean()
            total_n = len(all_data)
            n_groups = [len(g) for g in data_groups]
            ss_between = sum(n * (g.mean() - grand_mean)**2 for n, g in zip(n_groups, data_groups))
            ss_total = sum((all_data - grand_mean)**2)
            ss_error = ss_total - ss_between
            df_between = num_groups - 1
            df_error = total_n - num_groups
            ms_error = ss_error / df_error if df_error > 0 else 0
        else:
            test_name = "Welch's ANOVA"
            n = np.array([len(g) for g in data_groups])
            means = np.array([g.mean() for g in data_groups])
            vars = np.array([g.var(ddof=1) for g in data_groups])
            weights = n / vars
            sum_w = np.sum(weights)
            weighted_mean = np.sum(weights * means) / sum_w

            num = np.sum(weights * (means - weighted_mean)**2) / (num_groups - 1)
            lambdas = (1 - weights / sum_w)**2 / (n - 1)
            den = 1 + 2 * (num_groups - 2) / (num_groups**2 - 1) * np.sum(lambdas)
            f_stat = num / den

            df_between = num_groups - 1
            df_error = 1 / (3 / (num_groups**2 - 1) * np.sum(lambdas))
            p_val = 1 - stats.f.cdf(f_stat, df_between, df_error)

            ms_error = np.mean(vars)

        global_results = {
            'Test': test_name,
            'Variable': var,
            'Grouping': group_var,
            'F': f_stat,
            'df Between': df_between,
            'df Error': df_error,
            'p': p_val
        }
    else:
        test_name = "Kruskal-Wallis H Test"
        h_stat, p_val = stats.kruskal(*data_groups)
        global_results = {
            'Test': test_name,
            'Variable': var,
            'Grouping': group_var,
            'H': h_stat,
            'df': num_groups - 1,
            'p': p_val
        }
        ms_error = clean_df[var].var()

    post_hoc_results = []
    if num_groups > 2:
        pairs = list(combinations(groups, 2))
        num_comparisons = len(pairs)

        for g1, g2 in pairs:
            d1 = clean_df[clean_df[group_var] == g1][var]
            d2 = clean_df[clean_df[group_var] == g2][var]

            mean1 = d1.mean()
            mean2 = d2.mean()
            mean_diff = mean1 - mean2
            n1, n2 = len(d1), len(d2)

            if test_name == "Kruskal-Wallis H Test":
                u_stat, p_raw = stats.mannwhitneyu(d1, d2)
                t_val = u_stat
                es = u_stat / (n1 * n2)
            else:
                se = np.sqrt(ms_error * (1/n1 + 1/n2))
                t_val = mean_diff / se if se > 0 else 0
                df_post = len(clean_df) - num_groups
                p_raw = 2 * (1 - stats.t.cdf(abs(t_val), df_post))
                es = mean_diff / np.sqrt(ms_error) if ms_error > 0 else 0

            p_bonf = min(1.0, p_raw * num_comparisons)

            post_hoc_results.append({
                'Group 1': g1,
                'Group 2': g2,
                'Mean 1': mean1,
                'Mean 2': mean2,
                'Mean Diff': mean_diff,
                't/U': t_val,
                'p (bonf)': p_bonf,
                'Effect': es
            })

    return {
        'global': global_results,
        'post_hoc': post_hoc_results,
        'assumptions': {
            'Normality': all_normal,
            'Homogeneity': homog,
            'p_homog': p_homog
        }
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
