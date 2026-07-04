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
    """Specialized display for ANOVA and Post-Hoc results."""
    import pandas as pd

    global_df = pd.DataFrame([results['global']])
    # Clean up global display
    global_display = global_df[['Variable', 'Grouping', 'F', 'p']]
    display_header("One-way ANOVA (Omnibus Test)")
    display_table(global_display)

    # Show more details for global ANOVA
    details = global_df[['SS Between', 'df Between', 'MS Between', 'SS Error', 'df Error', 'MS Error']]
    display_table(details, title="ANOVA Summary Statistics")

    if results['post_hoc']:
        post_hoc_df = pd.DataFrame(results['post_hoc'])
        display_header("Post-Hoc Comparisons (Bonferroni)")
        footer = "* Nota: El ajuste de Bonferroni multiplica el p-valor por el número de comparaciones. La d de Cohen utiliza la raíz del MS_error del modelo global."
        display_table(post_hoc_df, footer=footer, highlight_col='p (bonf)', highlight_threshold=0.05)

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
