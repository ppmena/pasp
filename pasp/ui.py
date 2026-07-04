def display_header(title):
    try:
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.print(Panel(f"[bold blue]{title}[/bold blue]", expand=False))
    except ImportError:
        print(f"\n=== {title} ===")

def display_table(df, title=None):
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
            formatted_row = []
            for val in row:
                if isinstance(val, float):
                    formatted_row.append(f"{val:.3f}")
                else:
                    formatted_row.append(str(val))
            table.add_row(*formatted_row)

        console.print(table)
    except ImportError:
        if title:
            print(f"\n{title}")
        print(df.to_string())

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
        # Strip rich tags if possible or just print
        console.print(message)
    except ImportError:
        # Simple cleanup of common rich tags
        m = message.replace("[bold]", "").replace("[/bold]", "")
        m = m.replace("[green]", "").replace("[/green]", "")
        m = m.replace("[red]", "").replace("[/red]", "")
        m = m.replace("[blue]", "").replace("[/blue]", "")
        m = m.replace("[yellow]", "").replace("[/yellow]", "")
        print(m)
