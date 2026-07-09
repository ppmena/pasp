import pytest
import pandas as pd
import numpy as np
from pasp import stats

def test_force_parametric():
    # Data that is definitely not normal
    data = {'val': [1, 1, 1, 1, 10, 10, 10, 10], 'group': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B']}
    df = pd.DataFrame(data)

    # Normally this would fall back to Mann-Whitney
    res_default = stats.ttest_independent(df, 'val', 'group')
    assert "Mann-Whitney" in res_default['Test']

    # Force parametric
    res_forced = stats.ttest_independent(df, 'val', 'group', force_parametric=True)
    assert "T-Test" in res_forced['Test']

def test_chi_square():
    data = {
        'var1': ['A', 'A', 'B', 'B', 'A', 'A', 'B', 'B'],
        'var2': ['X', 'X', 'Y', 'Y', 'X', 'Y', 'X', 'Y']
    }
    df = pd.DataFrame(data)
    res = stats.chi_square_independence(df, 'var1', 'var2')
    assert res['Test'] == 'Chi-square Test of Independence'
    assert 'Chi2' in res
    assert 'Post-hoc Residuals' in res
    assert len(res['Post-hoc Residuals']) == 4
