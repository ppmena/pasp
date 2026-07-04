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

def get_variables(df, vars_list=None):
    """Return the specified variables or all numeric columns if none specified."""
    if vars_list:
        missing = [v for v in vars_list if v not in df.columns]
        if missing:
            print(f"Error: Variables {missing} not found in data.")
            sys.exit(1)
        return df[vars_list]
    return df.select_dtypes(include=['number'])
