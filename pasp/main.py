import argparse
import sys
import os
import subprocess

def check_dependencies():
    deps = {"pandas": False, "numpy": False, "scipy": False, "rich": False}
    try:
        import pandas; deps["pandas"] = True
    except ImportError: pass
    try:
        import numpy; deps["numpy"] = True
    except ImportError: pass
    try:
        import scipy; deps["scipy"] = True
    except ImportError: pass
    try:
        import rich; deps["rich"] = True
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
    ui.display_info("[bold]General Installation:[/bold]\npip install git+https://github.com/ppmena/pasp")
    ui.display_info("\n[bold]Termux Specific Instructions:[/bold]")
    ui.display_info("1. Update packages: pkg update && pkg upgrade")
    ui.display_info("2. Install build tools: pkg install clang make cmake pkg-config ninja meson")
    ui.display_info("3. Install PASP: pip install git+https://github.com/ppmena/pasp")

def list_examples():
    from pasp import ui
    ui.display_header("PASP Example Datasets")
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'examples'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'examples'),
        os.path.join(os.getcwd(), 'examples'),
        os.path.join(os.getcwd(), 'pasp', 'examples')
    ]
    examples_dir = None
    for p in possible_paths:
        if os.path.exists(p) and os.path.isdir(p):
            examples_dir = p; break
    if examples_dir:
        files = sorted([f for f in os.listdir(examples_dir) if f.endswith('.csv')])
        for f in files: ui.display_info(f"- {f}")
    else:
        ui.display_info("Example directory not found.")

def update_pasp():
    print("Checking for updates and upgrading PASP...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-build-isolation", "--upgrade", "git+https://github.com/ppmena/PASP"])
        print("Successfully updated PASP to the latest version.")
    except Exception as e:
        print(f"Error updating PASP: {e}")
        print("Please try manually: pip install --no-build-isolation --upgrade git+https://github.com/ppmena/PASP")

def main():
    SUBCOMMANDS = ["descriptives", "ttest-one", "ttest-ind", "ttest-paired", "anova", "correlation", "regression", "doctor", "install-help", "examples", "update"]
    parser = argparse.ArgumentParser(
        description="PASP: Portable Android Statistics Program. A lightweight CLI tool for statistical analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  Style A (Direct File):
    pasp data.csv --auto                      Automatic summary and descriptives
    pasp data.csv --anova score group --plot  One-way ANOVA with boxplots
    pasp data.csv --ttest-ind score gender --plot   Independent T-Test with visual plot

  Style B (Subcommands):
    pasp descriptives data.csv age height    Descriptive statistics for specific variables
    pasp doctor                              Check environment and dependencies
    pasp update                              Upgrade PASP from GitHub
        """,
        add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("--update", action="store_true", help="Upgrade PASP from GitHub")

    first_arg = sys.argv[1] if len(sys.argv) > 1 else None
    if first_arg == "--update" or first_arg == "update":
        update_pasp(); return

    if first_arg and first_arg not in SUBCOMMANDS and not first_arg.startswith("-"):
        parser.add_argument("file", help="Path to the data file")
        parser.add_argument("--auto", action="store_true", help="Run automatic analysis")
        parser.add_argument("--summary", action="store_true", help="Display data summary")
        parser.add_argument("--descriptives", action="store_true", help="Run descriptive statistics")
        parser.add_argument("--anova", nargs=2, metavar=('VAR', 'GROUP'), help="One-way ANOVA")
        parser.add_argument("--correlation", nargs="+", metavar='VARS', help="Correlation matrix")
        parser.add_argument("--ttest-ind", nargs=2, metavar=('VAR', 'GROUP'), help="Independent T-Test")
        parser.add_argument("--ttest-one", nargs=2, metavar=('VAR', 'VALUE'), help="One-sample T-Test")
        parser.add_argument("--ttest-paired", nargs=2, metavar=('VAR1', 'VAR2'), help="Paired T-Test")
        parser.add_argument("--regression", nargs=2, metavar=('DEP', 'INDEP'), help="Linear regression")
        parser.add_argument("--vars", nargs="+", help="Specific variables")
        parser.add_argument("--plot", action="store_true", help="Show visual plots (for anova and ttest-ind)")

        args = parser.parse_args()
        if args.help: parser.print_help(); return
        from pasp import data, stats, ui
        df = data.load_data(args.file)

        if args.summary or args.auto:
            ui.display_header(f"Data Summary: {args.file}")
            ui.display_info(f"[green]File loaded successfully.[/green]")
            ui.display_info(f"Encoding: {df.attrs.get('encoding', 'unknown')}, Separator: {df.attrs.get('delimiter', 'unknown')}")
            ui.display_info(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            ui.display_info(f"Variable list: {', '.join(df.columns.tolist())}")
        if args.descriptives or args.auto:
            vars_to_analyze = args.vars if args.vars else df.select_dtypes(include=['number', 'object', 'bool']).columns.tolist()
            ui.display_header("Descriptive Statistics")
            ui.display_info(f"Analyzing variables: {', '.join(vars_to_analyze)}")
            ui.display_table(stats.descriptives(df, vars_to_analyze), footer="* Ordinal variables interpretation should be cautious.")
        if args.anova:
            ui.display_anova(stats.anova_oneway(df, args.anova[0], args.anova[1]))
            if args.plot:
                from pasp import plots
                plots.render_boxplots(df, args.anova[0], args.anova[1])
        if args.correlation:
            ui.display_header("Correlation Matrix")
            ui.display_table(stats.correlation(df, args.correlation))
        if args.ttest_ind:
            try:
                ui.display_ttest(stats.ttest_independent(df, args.ttest_ind[0], args.ttest_ind[1]))
                if args.plot:
                    from pasp import plots
                    gn = df[args.ttest_ind[1]].unique()[:2]
                    plots.render_comparative_histogram(df[df[args.ttest_ind[1]]==gn[0]][args.ttest_ind[0]], df[df[args.ttest_ind[1]]==gn[1]][args.ttest_ind[0]], str(gn[0]), str(gn[1]))
            except Exception as e: ui.display_error(str(e))
        if args.ttest_one: ui.display_ttest(stats.ttest_one_sample(df, args.ttest_one[0], float(args.ttest_one[1])))
        if args.ttest_paired: ui.display_ttest(stats.ttest_paired(df, args.ttest_paired[0], args.ttest_paired[1]))
        if args.regression: ui.display_dict_as_table(stats.linear_regression(df, args.regression[0], args.regression[1]), title="Linear Regression")
        return

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    desc_p = subparsers.add_parser("descriptives", help="Calculate descriptive statistics")
    desc_p.add_argument("file", help="Data file")
    desc_p.add_argument("vars", nargs="*", help="Variables")
    tt1_p = subparsers.add_parser("ttest-one", help="One-sample T-test")
    tt1_p.add_argument("file", help="Data file"); tt1_p.add_argument("var", help="Variable"); tt1_p.add_argument("value", type=float, help="Null value")
    tti_p = subparsers.add_parser("ttest-ind", help="Independent T-test")
    tti_p.add_argument("file", help="Data file"); tti_p.add_argument("var", help="Variable"); tti_p.add_argument("group", help="Grouping variable"); tti_p.add_argument("--plot", action="store_true", help="Visual plot")
    ttp_p = subparsers.add_parser("ttest-paired", help="Paired T-test")
    ttp_p.add_argument("file", help="Data file"); ttp_p.add_argument("var1", help="Var 1"); ttp_p.add_argument("var2", help="Var 2")
    anova_p = subparsers.add_parser("anova", help="One-way ANOVA")
    anova_p.add_argument("file", help="Data file"); anova_p.add_argument("var", help="Variable"); anova_p.add_argument("group", help="Grouping variable"); anova_p.add_argument("--plot", action="store_true", help="Visual boxplot")
    corr_p = subparsers.add_parser("correlation", help="Pearson correlation")
    corr_p.add_argument("file", help="Data file"); corr_p.add_argument("vars", nargs="+", help="Variables")
    reg_p = subparsers.add_parser("regression", help="Linear regression")
    reg_p.add_argument("file", help="Data file"); reg_p.add_argument("dep", help="Dependent"); reg_p.add_argument("indep", help="Independent")
    subparsers.add_parser("doctor", help="Check system"); subparsers.add_parser("install-help", help="Installation guide"); subparsers.add_parser("examples", help="List examples"); subparsers.add_parser("update", help="Update from GitHub")

    args = parser.parse_args()
    if args.help or not args.command: parser.print_help(); sys.exit(0)
    if args.command == "doctor": doctor(); return
    if args.command == "install-help": install_help(); return
    if args.command == "examples": list_examples(); return
    if args.command == "update": update_pasp(); return
    from pasp import data, stats, ui
    df = data.load_data(args.file)
    if args.command == "descriptives":
        v = args.vars if args.vars else df.select_dtypes(include=['number', 'object', 'bool']).columns.tolist()
        ui.display_header("Descriptive Statistics")
        ui.display_info(f"Analyzing variables: {', '.join(v)}")
        ui.display_table(stats.descriptives(df, v), footer="* Ordinal interpretation cautious.")
    elif args.command == "ttest-one": ui.display_ttest(stats.ttest_one_sample(df, args.var, args.value))
    elif args.command == "ttest-ind":
        try:
            ui.display_ttest(stats.ttest_independent(df, args.var, args.group))
            if args.plot:
                from pasp import plots; gn = df[args.group].unique()[:2]
                plots.render_comparative_histogram(df[df[args.group]==gn[0]][args.var], df[df[args.group]==gn[1]][args.var], str(gn[0]), str(gn[1]))
        except Exception as e: ui.display_error(str(e))
    elif args.command == "ttest-paired": ui.display_ttest(stats.ttest_paired(df, args.var1, args.var2))
    elif args.command == "anova":
        ui.display_anova(stats.anova_oneway(df, args.var, args.group))
        if args.plot:
            from pasp import plots; plots.render_boxplots(df, args.var, args.group)
    elif args.command == "correlation":
        ui.display_header("Correlation Matrix"); ui.display_table(stats.correlation(df, args.vars))
    elif args.command == "regression": ui.display_dict_as_table(stats.linear_regression(df, args.dep, args.indep), title="Linear Regression")

if __name__ == "__main__":
    main()
