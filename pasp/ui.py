from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pandas as pd

console = Console()

def display_header(title):
    console.print(Panel(f"[bold blue]{title}[/bold blue]", expand=False))

def display_table(df, title=None):
    if title:
        console.print(f"\n[bold]{title}[/bold]")

    table = Table(show_header=True, header_style="bold magenta")

    for column in df.columns:
        table.add_column(column)

    for _, row in df.iterrows():
        formatted_row = []
        for val in row:
            if isinstance(val, float):
                formatted_row.append(f"{val:.3f}")
            else:
                formatted_row.append(str(val))
        table.add_row(*formatted_row)

    console.print(table)

def display_dict_as_table(data_dict, title=None):
    df = pd.DataFrame([data_dict])
    display_table(df, title)

def display_error(message):
    console.print(f"[bold red]Error:[/bold red] {message}")
