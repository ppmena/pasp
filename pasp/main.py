import argparse
import sys
from pasp import data, stats, ui

def main():
    parser = argparse.ArgumentParser(description="PASP: Portable Android Statistics Program")
    subparsers = parser.add_subparsers(dest="command", help="Statistical command to run")

    # Descriptives
    desc_parser = subparsers.add_parser("descriptives", help="Calculate descriptive statistics")
    desc_parser.add_argument("file", help="Path to the data file (CSV/TSV)")
    desc_parser.add_argument("--vars", nargs="+", help="Variables to analyze")

    # T-Test One Sample
    tt1_parser = subparsers.add_parser("ttest-one", help="One-sample t-test")
    tt1_parser.add_argument("file", help="Path to the data file")
    tt1_parser.add_argument("--vars", required=True, dest="var", help="Variable to test")
    tt1_parser.add_argument("--value", type=float, default=0, help="Test value (default: 0)")

    # T-Test Independent
    tti_parser = subparsers.add_parser("ttest-ind", help="Independent samples t-test")
    tti_parser.add_argument("file", help="Path to the data file")
    tti_parser.add_argument("--vars", required=True, dest="var", help="Dependent variable")
    tti_parser.add_argument("--group", required=True, help="Grouping variable")

    # T-Test Paired
    ttp_parser = subparsers.add_parser("ttest-paired", help="Paired samples t-test")
    ttp_parser.add_argument("file", help="Path to the data file")
    ttp_parser.add_argument("--vars", nargs=2, required=True, help="Two variables for paired test")

    # Regression
    reg_parser = subparsers.add_parser("regression", help="Simple linear regression")
    reg_parser.add_argument("file", help="Path to the data file")
    reg_parser.add_argument("--dep", required=True, help="Dependent variable")
    reg_parser.add_argument("--indep", required=True, help="Independent variable")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load data
    df = data.load_data(args.file)

    if args.command == "descriptives":
        vars_to_analyze = args.vars if args.vars else df.select_dtypes(include=['number']).columns.tolist()
        results = stats.descriptives(df, vars_to_analyze)
        ui.display_header("Descriptive Statistics")
        ui.display_table(results)

    elif args.command == "ttest-one":
        results = stats.ttest_one_sample(df, args.var, args.value)
        ui.display_header("One Sample T-Test")
        ui.display_dict_as_table(results)

    elif args.command == "ttest-ind":
        try:
            results = stats.ttest_independent(df, args.var, args.group)
            ui.display_header("Independent Samples T-Test")
            ui.display_dict_as_table(results)
        except ValueError as e:
            ui.display_error(str(e))

    elif args.command == "ttest-paired":
        results = stats.ttest_paired(df, args.vars[0], args.vars[1])
        ui.display_header("Paired Samples T-Test")
        ui.display_dict_as_table(results)

    elif args.command == "regression":
        try:
            results = stats.linear_regression(df, args.dep, args.indep)
            ui.display_header("Linear Regression")
            ui.display_dict_as_table(results)
        except NotImplementedError as e:
            ui.display_error(str(e))

if __name__ == "__main__":
    main()
