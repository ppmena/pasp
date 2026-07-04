import unittest
import pandas as pd
import os
from pasp import data

class TestDataLoading(unittest.TestCase):
    def setUp(self):
        self.test_files = {
            "comma.csv": "ID,Edad,Ansiedad\n1,23,15\n2,25,20",
            "semicolon.csv": "ID;Edad;Ansiedad\n1;23;15\n2;25;20",
            "tab.tsv": "ID\tEdad\tAnsiedad\n1\t23\t15\n2\t25\t20",
            "pipe.csv": "ID|Edad|Ansiedad\n1|23|15\n2|25|20"
        }
        for name, content in self.test_files.items():
            with open(name, "w") as f:
                f.write(content)

    def tearDown(self):
        for name in self.test_files:
            if os.path.exists(name):
                os.remove(name)

    def test_load_comma(self):
        df = data.load_data("comma.csv")
        self.assertEqual(df.shape[1], 3)
        self.assertEqual(list(df.columns), ["ID", "Edad", "Ansiedad"])
        self.assertEqual(df.attrs["delimiter"], ",")

    def test_load_semicolon(self):
        df = data.load_data("semicolon.csv")
        self.assertEqual(df.shape[1], 3)
        self.assertEqual(list(df.columns), ["ID", "Edad", "Ansiedad"])
        self.assertEqual(df.attrs["delimiter"], ";")

    def test_load_tab(self):
        df = data.load_data("tab.tsv")
        self.assertEqual(df.shape[1], 3)
        self.assertEqual(list(df.columns), ["ID", "Edad", "Ansiedad"])
        self.assertEqual(df.attrs["delimiter"], "\t")

    def test_load_pipe(self):
        df = data.load_data("pipe.csv")
        self.assertEqual(df.shape[1], 3)
        self.assertEqual(list(df.columns), ["ID", "Edad", "Ansiedad"])
        self.assertEqual(df.attrs["delimiter"], "|")

if __name__ == "__main__":
    unittest.main()
