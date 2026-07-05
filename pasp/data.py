import sys
import csv
from pathlib import Path

COMMON_SEPARATORS = [",", ";", "\t", "|"]

def detect_delimiter(filepath, encoding="utf-8"):
    """Attempt to detect the delimiter of a CSV file."""
    path = Path(filepath)
    try:
        with path.open("r", encoding=encoding, newline="") as f:
            sample = f.read(4096)
    except Exception:
        return ","

    if not sample.strip():
        return ","

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=COMMON_SEPARATORS)
        return dialect.delimiter
    except csv.Error:
        pass

    # Fallback: simple counting
    lines = [line for line in sample.splitlines() if line.strip()]
    first_line = lines[0] if lines else ""

    best_separator = ","
    best_count = 1

    for sep in COMMON_SEPARATORS:
        count = len(first_line.split(sep))
        if count > best_count:
            best_separator = sep
            best_count = count

    return best_separator

def load_data(filepath):
    """Load data from a CSV or TSV file with auto-detection of delimiter and encoding."""
    import pandas as pd
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    last_error = None
    for encoding in ["utf-8", "latin-1"]:
        try:
            delimiter = detect_delimiter(path, encoding=encoding)
            df = pd.read_csv(path, sep=delimiter, encoding=encoding)

            # If it only has one column, it might have failed to detect the real delimiter
            if df.shape[1] == 1:
                best_df = df
                best_delimiter = delimiter

                for sep in COMMON_SEPARATORS:
                    if sep == delimiter: continue
                    try:
                        candidate = pd.read_csv(path, sep=sep, encoding=encoding)
                        if candidate.shape[1] > best_df.shape[1]:
                            best_df = candidate
                            best_delimiter = sep
                    except Exception:
                        continue
                df = best_df
                delimiter = best_delimiter

            df.attrs["delimiter"] = delimiter
            df.attrs["encoding"] = encoding
            return df

        except Exception as e:
            last_error = e
            continue

    print(f"Error loading data: {last_error}")
    sys.exit(1)

def resolve_variables(df, vars_list):
    """
    Translates a list of names or indices (as strings) into actual column names.
    Supports input like: ['0', '3', 'age'] -> ['id', 'score', 'age']
    """
    if not vars_list:
        return []

    resolved = []
    columns = df.columns.tolist()
    num_cols = len(columns)

    for v in vars_list:
        if v in columns:
            resolved.append(v)
        else:
            try:
                idx = int(v)
                if 0 <= idx < num_cols:
                    resolved.append(columns[idx])
                else:
                    print(f"Error: Variable index {idx} out of range (0-{num_cols-1}).")
                    sys.exit(1)
            except ValueError:
                print(f"Error: Variable '{v}' not found in dataset.")
                sys.exit(1)

    return resolved

def get_variables(df, vars_list=None):
    """Return the specified variables or all numeric columns if none specified."""
    if vars_list:
        resolved = resolve_variables(df, vars_list)
        return df[resolved]
    return df.select_dtypes(include=['number'])
