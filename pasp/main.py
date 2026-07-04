import argparse
import sys
import os

def check_dependencies():
    deps = {
        "pandas": False,
        "numpy": False,
        "scipy": False,
        "rich": False
    }
    try:
        import pandas
        deps["pandas"] = True
    except ImportError: pass
    try:
        import numpy
        deps["numpy"] = True
    except ImportError: pass
    try:
        import scipy
        deps["scipy"] = True
    except ImportError: pass
    try:
        import rich
        deps["rich"] = True
    except ImportError: pass
    return deps

def doctor():
    from pasp import ui
    import platform

    ui.display_header("PASP Doctor - Diagnostic Report")

    ui.display_info(f"[bold]System:[/bold] {platform.system()} {platform.release()}")
    ui.display_info(f"[bold]Python Version:[/bold] {sys.version.split()[0]}")

    is_termux = "com.termux" in sys.executable or os.path.exists("/data/data/com.termux")
    ui.display_info(f"[bold]Termux detected:[/bold] {'Yes' if is_termux else 'No'}")

    ui.display_info("\n[bold]Dependencies:[/bold]")
    deps = check_dependencies()
    for dep, installed in deps.items():
        status = "[green]Installed[/green]" if installed else "[red]Missing[/red]"
        ui.display_info(f"- {dep}: {status}")

    if not all(deps.values()):
        ui.display_info("\n[yellow]Recommendations:[/yellow]")
        if is_termux:
            ui.display_info("It seems you are in Termux. If you have issues installing pandas/numpy/scipy:")
            ui.display_info("1. pkg install clang make cmake pkg-config ninja meson")
            ui.display_info("2. pip install numpy scipy pandas rich")
        else:
            ui.display_info("Install missing dependencies using: pip install pandas numpy scipy rich")

def install_help():
    from pasp import ui
    ui.display_header("PASP Installation Help")
    ui.display_info("[bold]General Installation:[/bold]")
    ui.display_info("pip install git+https://github.com/ppmena/PASP.git")

    ui.display_info("\n[bold]Termux Specific Instructions:[/bold]")
    ui.display_info("1. Update packages: pkg update && pkg upgrade")
    ui.display_info("2. Install build tools: pkg install clang make cmake pkg-config ninja meson")
    ui.display_info("3. Install PASP: pip install git+https://github.com/ppmena/PASP.git")

def list_examples():
    from pasp import ui
    ui.display_header("PASP Example Datasets")

    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')

    if os.path.exists(examples_dir) and os.path.isdir(examples_dir):
        files = sorted([f for f in os.listdir(examples_dir) if f.endswith('.csv')])
        for f in files:
            ui.display_info(f"- {f}")
    else:
        ui.display_info(f"Example directory not found at {examples_dir}")

def main():
    parser = argparse.ArgumentParser(description="PASP: Portable Android Statistics Program", add_help=False)
    parser.add_argument("-h", "--help", action="store_true")

    if len(sys.argv) > 1 and sys.argv[1] not in ["-h", "--help", "descriptives", "ttest-one", "ttest-ind", "ttest-paired", "anova", "correlation", "regression", "doctor", "install-help", "examples"]:
        parser.add_argument("file", help="Path to the data file")
        parser.add_argument("--auto", action="store_true", help="Run automatic analysis")
        parser.add_argument("--summary", action="store_true", help="Show data summary")
        parser.add_argument("--descriptives", action="store_true", help="Run descriptive statistics")
        parser.add_argument("--anova", nargs=2, metavar=('VAR', 'GROUP'), help="One-way ANOVA")
        parser.add_argument("--correlation", nargs="+", metavar='VARS', help="Correlation analysis")
        parser.add_argument("--ttest-ind", nargs=2, metavar=('VAR', 'GROUP'), help="Independent samples t-test")
        parser.add_argument("--ttest-one", nargs=2, metavar=('VAR', 'VALUE'), help="One-sample t-test")
        parser.add_argument("--ttest-paired", nargs=2, metavar=('VAR1', 'VAR2'), help="Paired samples t-test")
        parser.add_argument("--regression", nargs=2, metavar=('DEP', 'INDEP'), help="Simple linear regression")
        parser.add_argument("--vars", nargs="+", help="Variables for descriptives")
        parser.add_argument("--plot", action="store_true", help="Show visual plots (for ttest-ind)")

        args = parser.parse_args()

        if args.help:
            parser.print_help()
            sys.exit(0)

        from pasp import data, stats, ui
        df = data.load_data(args.file)

        if args.summary or args.auto:
            ui.display_header(f"Data Summary: {args.file}")
            ui.display_info(f"[green]File loaded successfully.[/green]")
            ui.display_info(f"Encoding detected: {df.attrs.get('encoding', 'unknown')}")
            delim = df.attrs.get('delimiter', 'unknown')
            if delim == '\t': delim = 'tabulator'
            ui.display_info(f"Separator detected: {delim}")
            ui.display_info(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            ui.display_info(f"Columns: {', '.join(df.columns)}")

        if args.descriptives or args.auto:
            vars_to_analyze = args.vars if args.vars else df.select_dtypes(include=['number', 'object', 'bool']).columns.tolist()
            results = stats.descriptives(df, vars_to_analyze)
            ui.display_header("Descriptive Statistics")
            footer = "* Note: Variables marked with asterisk are identified as ordinal (discrete with max 4 values). Interpretation should be cautious."
            ui.display_table(results, footer=footer)

        if args.anova:
            results = stats.anova_oneway(df, args.anova[0], args.anova[1])
            ui.display_anova(results)

        if args.correlation:
            results = stats.correlation(df, args.correlation)
            ui.display_header("Correlation Matrix")
            ui.display_table(results)

        if args.ttest_ind:
            try:
                results = stats.ttest_independent(df, args.ttest_ind[0], args.ttest_ind[1])
                ui.display_ttest(results)

                if args.plot:
                    from pasp import plots
                    g_var = args.ttest_ind[1]
                    v_var = args.ttest_ind[0]
                    groups = df[g_var].unique()
                    g1_data = df[df[g_var] == groups[0]][v_var]
                    g2_data = df[df[g_var] == groups[1]][v_var]
                    plots.render_comparative_histogram(g1_data, g2_data, str(groups[0]), str(groups[1]))
            except ValueError as e: ui.display_error(str(e))

        if args.ttest_one:
            results = stats.ttest_one_sample(df, args.ttest_one[0], float(args.ttest_one[1]))
            ui.display_ttest(results)

        if args.ttest_paired:
            results = stats.ttest_paired(df, args.ttest_paired[0], args.ttest_paired[1])
            ui.display_ttest(results)

        if args.regression:
            try:
                results = stats.linear_regression(df, args.regression[0], args.regression[1])
                ui.display_header("Linear Regression")
                ui.display_dict_as_table(results)
            except NotImplementedError as e: ui.display_error(str(e))
        return

    subparsers = parser.add_subparsers(dest="command", help="Statistical command to run")

    desc_p = subparsers.add_parser("descriptives", help="Calculate descriptive statistics")
    desc_p.add_argument("file", help="Path to the data file")
    desc_p.add_argument("vars", nargs="*", help="Variables to analyze")

    tt1_p = subparsers.add_parser("ttest-one", help="One-sample t-test")
    tt1_p.add_argument("file", help="Path to the data file")
    tt1_p.add_argument("var", help="Variable to test")
    tt1_p.add_argument("value", type=float, help="Test value")

    tti_p = subparsers.add_parser("ttest-ind", help="Independent samples t-test")
    tti_p.add_argument("file", help="Path to the data file")
    tti_p.add_argument("var", help="Dependent variable")
    tti_p.add_argument("group", help="Grouping variable")
    tti_p.add_argument("--plot", action="store_true", help="Show visual plot")

    ttp_p = subparsers.add_parser("ttest-paired", help="Paired samples t-test")
    ttp_p.add_argument("file", help="Path to the data file")
    ttp_p.add_argument("var1", help="First variable")
    ttp_p.add_argument("var2", help="Second variable")

    anova_p = subparsers.add_parser("anova", help="One-way ANOVA")
    anova_p.add_argument("file", help="Path to the data file")
    anova_p.add_argument("var", help="Dependent variable")
    anova_p.add_argument("group", help="Grouping variable")

    corr_p = subparsers.add_parser("correlation", help="Correlation analysis")
    corr_p.add_argument("file", help="Path to the data file")
    corr_p.add_argument("vars", nargs="+", help="Variables to correlate")

    reg_p = subparsers.add_parser("regression", help="Simple linear regression")
    reg_p.add_argument("file", help="Path to the data file")
    reg_p.add_argument("dep", help="Dependent variable")
    reg_p.add_argument("indep", help="Independent variable")

    subparsers.add_parser("doctor", help="Check system and dependencies")
    subparsers.add_parser("install-help", help="Show installation instructions")
    subparsers.add_parser("examples", help="List example datasets")

    args = parser.parse_args()

    if args.help or (not args.command):
        parser.print_help()
        sys.exit(0)

    if args.command == "doctor":
        doctor()
        return
    if args.command == "install-help":
        install_help()
        return
    if args.command == "examples":
        list_examples()
        return

    from pasp import data, stats, ui
    df = data.load_data(args.file)

    if args.command == "descriptives":
        vars_to_analyze = args.vars if args.vars else df.select_dtypes(include=['number', 'object', 'bool']).columns.tolist()
        results = stats.descriptives(df, vars_to_analyze)
        ui.display_header("Descriptive Statistics")
        footer = "* Note: Variables marked with asterisk are identified as ordinal (discrete with max 4 values). Interpretation should be cautious."
        ui.display_table(results, footer=footer)
    elif args.command == "ttest-one":
        results = stats.ttest_one_sample(df, args.var, args.value)
        ui.display_ttest(results)
    elif args.command == "ttest-ind":
        try:
            results = stats.ttest_independent(df, args.var, args.group)
            ui.display_ttest(results)
            if args.plot:
                from pasp import plots
                groups = df[args.group].unique()
                g1_data = df[df[args.group] == groups[0]][args.var]
                g2_data = df[df[args.group] == groups[1]][args.var]
                plots.render_comparative_histogram(g1_data, g2_data, str(groups[0]), str(groups[1]))
        except ValueError as e: ui.display_error(str(e))
    elif args.command == "ttest-paired":
        results = stats.ttest_paired(df, args.var1, args.var2)
        ui.display_ttest(results)
    elif args.command == "anova":
        results = stats.anova_oneway(df, args.var, args.group)
        ui.display_anova(results)
    elif args.command == "correlation":
        results = stats.correlation(df, args.vars)
        ui.display_header("Correlation Matrix")
        ui.display_table(results)
    elif args.command == "regression":
        try:
            results = stats.linear_regression(df, args.dep, args.indep)
            ui.display_header("Linear Regression")
            ui.display_dict_as_table(results)
        except NotImplementedError as e: ui.display_error(str(e))

if __name__ == "__main__":
    main()
