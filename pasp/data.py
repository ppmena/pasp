import pandas as pd
import sys

def load_data(filepath):
    """Load data from a CSV or TSV file."""
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.tsv') or filepath.endswith('.txt'):
            df = pd.read_csv(filepath, sep='\t')
        else:
            # Try CSV by default
            df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def get_variables(df, vars_list=None):
    """Return the specified variables or all numeric columns if none specified."""
    if vars_list:
        missing = [v for v in vars_list if v not in df.columns]
        if missing:
            print(f"Error: Variables {missing} not found in data.")
            sys.exit(1)
        return df[vars_list]
    return df.select_dtypes(include=['number'])
