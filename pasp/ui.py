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

            # Highlight significant p-values if requested
            if highlight_col and highlight_col in row:
                try:
                    val = float(row[highlight_col])
                    if val < highlight_threshold:
                        style = "green bold"
                except (ValueError, TypeError):
                    pass

            # Classification styles for Descriptives
            if not style and 'Type' in df.columns:
                if row['Type'] == 'Nominal':
                    style = "cyan"
                elif row['Type'] == 'Ordinal':
                    style = "yellow"

            formatted_row = []
            for col in df.columns:
                val = row[col]
                if isinstance(val, float):
                    if "p" in str(col).lower() and val < 0.001:
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
    """Specialized display for ANOVA and Post-Hoc results with assumptions."""
    import pandas as pd

    global_df = pd.DataFrame([results['global']])
    test_name = results['global']['Test']
    display_header(f"{test_name} Result")

    # Display global table
    display_table(global_df)

    # Display assumptions
    assump = results['assumptions']
    norm_status = "[green]Pass[/green]" if assump['Normality'] else "[red]Fail[/red]"
    homog_status = "[green]Pass[/green]" if assump['Homogeneity'] else "[red]Fail[/red]"
    display_info(f"\n[bold]Assumption Checks:[/bold]")
    display_info(f"- Normality (Shapiro-Wilk): {norm_status}")
    display_info(f"- Homogeneity (Levene): {homog_status} (p = {assump['p_homog']:.3f})")

    if results['post_hoc']:
        post_hoc_df = pd.DataFrame(results['post_hoc'])
        display_header("Post-Hoc Comparisons (Bonferroni)")
        footer = "* Nota: El ajuste de Bonferroni multiplica el p-valor por el número de comparaciones."
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
        m = message.replace("[bold]", "").replace("[/bold]", "")
        m = m.replace("[green]", "").replace("[/green]", "")
        m = m.replace("[red]", "").replace("[/red]", "")
        m = m.replace("[blue]", "").replace("[/blue]", "")
        m = m.replace("[yellow]", "").replace("[/yellow]", "")
        print(m)
