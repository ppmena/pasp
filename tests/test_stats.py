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
        self.assertEqual(result['t'], 0.0)
        self.assertEqual(result['p'], 1.0)

    def test_ttest_independent(self):
        result = stats.ttest_independent(self.df, 'a', 'group')
        # Group M: [1, 2], Mean=1.5
        # Group F: [3, 4, 5], Mean=4.0
        self.assertEqual(result['Mean Difference'], -2.5)
        # With small N, p might be slightly above 0.05 (actually ~0.057)
        self.assertTrue(result['p'] < 0.1)

    def test_ttest_paired(self):
        result = stats.ttest_paired(self.df, 'a', 'b')
        self.assertEqual(result['Mean Difference'], -3.0)

    def test_linear_regression(self):
        result = stats.linear_regression(self.df, 'b', 'a')
        self.assertEqual(result['Slope'], 2.0)
        self.assertEqual(result['Intercept'], 0.0)
        self.assertEqual(result['R'], 1.0)

if __name__ == '__main__':
    unittest.main()
