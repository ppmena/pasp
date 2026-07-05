def display_header(title):
    try:
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.print(Panel(f"[bold blue]{title}[/bold blue]", expand=False))
    except ImportError:
        print(f"\n=== {title} ===")

def display_table(df, title=None, footer=None, highlight_col=None, highlight_threshold=None):
    try:
        from rich.console import Console
        from rich.table import Table
        console = Console()
        if title:
            console.print(f"\n[bold]{title}[/bold]")

        table = Table(show_header=True, header_style="bold magenta")

        for column in df.columns:
            table.add_column(str(column))

        for _, row in df.iterrows():
            style = None

            if highlight_col and highlight_col in row:
                try:
                    val = float(row[highlight_col])
                    if val < highlight_threshold:
                        style = "green bold"
                except (ValueError, TypeError):
                    pass

            if not style and 'Type' in df.columns:
                if row['Type'] == 'Nominal':
                    style = "cyan"
                elif row['Type'] == 'Ordinal':
                    style = "yellow"

            formatted_row = []
            for col in df.columns:
                val = row[col]
                if isinstance(val, float):
                    col_lower = str(col).lower()
                    # Only format as p-value if column name starts with 'p ' or 'p-' or is exactly 'p'
                    is_p_col = col_lower == 'p' or col_lower.startswith('p ') or col_lower.startswith('p-') or 'p-value' in col_lower

                    if is_p_col and val < 0.001:
                        formatted_row.append("< .001")
                    else:
                        formatted_row.append(f"{val:.3f}")
                else:
                    formatted_row.append(str(val))

            table.add_row(*formatted_row, style=style)

        console.print(table)
        if footer:
            console.print(f"[italic]{footer}[/italic]")

    except ImportError:
        if title:
            print(f"\n{title}")
        print(df.to_string(index=False))
        if footer:
            f = footer.replace("[italic]", "").replace("[/italic]", "")
            print(f"\n{f}")

def display_dict_as_table(data_dict, title=None):
    try:
        import pandas as pd
        df = pd.DataFrame([data_dict])
        display_table(df, title)
    except ImportError:
        if title:
            print(f"\n{title}")
        for k, v in data_dict.items():
            print(f"{k}: {v}")

def display_anova(results):
    """Specialized display for ANOVA and Post-Hoc results with strict assumptions."""
    import pandas as pd

    global_df = pd.DataFrame([results['global']])
    test_name = results['global']['Test']
    display_header(f"{test_name} Result")

    display_table(global_df)

    assump = results['assumptions']

    strict_data = [
        {
            'Assumption': 'Normality',
            'Test or criteria': 'Shapiro-Wilk on residuals',
            'p-value / result': f"{assump['p_norm']:.3f}",
            'Decision': 'Assumption met' if assump['Normality'] else 'Assumption not met'
        },
        {
            'Assumption': 'Homogeneity of variances',
            'Test or criteria': 'Levene',
            'p-value / result': f"{assump['p_homog']:.3f}",
            'Decision': 'Assumption met' if assump['Homogeneity'] else 'Assumption not met'
        },
        {
            'Assumption': 'Outliers',
            'Test or criteria': '|std. residual| > 3',
            'p-value / result': f"{assump['num_outliers']} cases",
            'Decision': 'No relevant outliers detected' if not assump['Outliers'] else 'Relevant outliers detected'
        }
    ]

    display_header("Strict Assumption Evaluation")
    display_table(pd.DataFrame(strict_data))

    if assump['Normality'] and assump['Homogeneity'] and not assump['Outliers']:
        display_info("\n[bold green]One-way ANOVA is adequate.[/bold green]")
    else:
        display_info("\n[bold red]One-way ANOVA is not adequate.[/bold red]")

    if results['post_hoc']:
        post_hoc_df = pd.DataFrame(results['post_hoc'])
        if test_name == "Kruskal-Wallis H Test":
            ph_title = "Dunn's Post-Hoc Comparisons (Bonferroni)"
        else:
            ph_title = "Post-Hoc Comparisons (Bonferroni)"

        display_header(ph_title)
        footer = "* Note: Bonferroni adjustment multiplies the p-value by the number of comparisons. Effect size (d) uses the model's residual variance."
        display_table(post_hoc_df, footer=footer, highlight_col='p (bonf)', highlight_threshold=0.05)

def display_ttest(results):
    """Specialized display for T-Tests with assumption info."""
    test_name = results['Test']
    display_header(f"{test_name} Result")
    display_dict_as_table(results)

    display_info(f"\n[bold]Assumption Checks:[/bold]")
    if 'Normality p' in results:
        norm_status = "[green]Pass[/green]" if results['Normality p'] > 0.05 else "[red]Fail[/red]"
        display_info(f"- Normality (Shapiro-Wilk): {norm_status} (p = {results['Normality p']:.3f})")
    if 'Normality p (diff)' in results:
        norm_status = "[green]Pass[/green]" if results['Normality p (diff)'] > 0.05 else "[red]Fail[/red]"
        display_info(f"- Normality of differences (Shapiro-Wilk): {norm_status} (p = {results['Normality p (diff)']:.3f})")
    if 'Normality p (G1)' in results:
        norm1 = "[green]Pass[/green]" if results['Normality p (G1)'] > 0.05 else "[red]Fail[/red]"
        norm2 = "[green]Pass[/green]" if results['Normality p (G2)'] > 0.05 else "[red]Fail[/red]"
        display_info(f"- Normality G1: {norm1} (p = {results['Normality p (G1)']:.3f})")
        display_info(f"- Normality G2: {norm2} (p = {results['Normality p (G2)']:.3f})")
    if 'Homogeneity p' in results:
        homog_status = "[green]Pass[/green]" if results['Homogeneity p'] > 0.05 else "[red]Fail[/red]"
        display_info(f"- Homogeneity (Levene): {homog_status} (p = {results['Homogeneity p']:.3f})")

    if "Wilcoxon" in test_name:
        display_info(f"- Wilcoxon signed-rank p-value: {results['p']:.3f}")

def display_error(message):
    try:
        from rich.console import Console
        console = Console()
        console.print(f"[bold red]Error:[/bold red] {message}")
    except ImportError:
        print(f"Error: {message}")

def display_info(message):
    try:
        from rich.console import Console
        console = Console()
        console.print(message)
    except ImportError:
        m = str(message).replace("[bold]", "").replace("[/bold]", "")
        m = m.replace("[green]", "").replace("[/green]", "")
        m = m.replace("[red]", "").replace("[/red]", "")
        m = m.replace("[blue]", "").replace("[/blue]", "")
        m = m.replace("[yellow]", "").replace("[/yellow]", "")
        print(m)
