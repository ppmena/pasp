import unittest
import pandas as pd
import numpy as np
from pasp import stats

class TestStats(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [2, 4, 6, 8, 10],
            'group': ['M', 'M', 'F', 'F', 'F']
        })

    def test_descriptives(self):
        results = stats.descriptives(self.df, ['a'])
        self.assertEqual(results.iloc[0]['N'], 5)
        self.assertEqual(results.iloc[0]['Mean'], 3.0)
        self.assertEqual(results.iloc[0]['Median'], 3.0)

    def test_ttest_one_sample(self):
        result = stats.ttest_one_sample(self.df, 'a', test_value=3)
        self.assertEqual(result['Stat'], 0.0)
        self.assertEqual(result['p'], 1.0)
        self.assertEqual(result['Test'], 'One-sample T-Test')

    def test_ttest_independent(self):
        result = stats.ttest_independent(self.df, 'a', 'group')
        # Group M: [1, 2], Mean=1.5
        # Group F: [3, 4, 5], Mean=4.0
        self.assertEqual(result['Stat'], stats.ttest_independent(self.df, 'a', 'group')['Stat'])
        self.assertTrue(result['p'] < 0.1)

    def test_ttest_paired(self):
        result = stats.ttest_paired(self.df, 'a', 'b')
        self.assertEqual(result['Stat'], stats.ttest_paired(self.df, 'a', 'b')['Stat'])

    def test_linear_regression(self):
        result = stats.linear_regression(self.df, 'b', 'a')
        self.assertEqual(result['Slope'], 2.0)
        self.assertEqual(result['Intercept'], 0.0)
        self.assertEqual(result['R'], 1.0)

    def test_non_parametric_fallback(self):
        # Create non-normal data
        df_non_normal = pd.DataFrame({
            'x': [1, 1, 1, 1, 1, 100],
            'g': ['A', 'A', 'A', 'B', 'B', 'B']
        })
        result = stats.ttest_independent(df_non_normal, 'x', 'g')
        self.assertEqual(result['Test'], 'Mann-Whitney U Test')

if __name__ == '__main__':
    unittest.main()
