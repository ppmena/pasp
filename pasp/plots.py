import numpy as np

def render_comparative_histogram(g1_data, g2_data, g1_name, g2_name):
    """
    Renders a comparative histogram in the terminal using rich.
    """
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel

    console = Console()
    d1 = g1_data.dropna().values
    d2 = g2_data.dropna().values

    if len(d1) == 0 or len(d2) == 0: return

    NUM_BINS = 20
    MAX_HEIGHT = 10

    combined = np.concatenate([d1, d2])
    min_val, max_val = np.min(combined), np.max(combined)
    if min_val == max_val: max_val += 1

    bins = np.linspace(min_val, max_val, NUM_BINS + 1)
    freq1, _ = np.histogram(d1, bins=bins)
    freq2, _ = np.histogram(d2, bins=bins)

    max_freq = max(np.max(freq1), np.max(freq2))
    if max_freq == 0: return

    scale = MAX_HEIGHT / max_freq
    f1_s = (freq1 * scale).astype(int)
    f2_s = (freq2 * scale).astype(int)

    legend = Text.assemble((f"█", "bold cyan"), f" {g1_name}   ", (f"█", "bold magenta"), f" {g2_name}   ", (f"▒", "bold white"), " Overlap")
    console.print(Panel(legend, title="Distribution Plot", expand=False))

    for h in range(MAX_HEIGHT, 0, -1):
        line = Text("│", style="white")
        for b in range(NUM_BINS):
            char = " "
            style = ""
            in1, in2 = f1_s[b] >= h, f2_s[b] >= h
            if in1 and in2: char, style = "▒", "bold white"
            elif in1: char, style = "█", "bold cyan"
            elif in2: char, style = "█", "bold magenta"
            line.append(char * 2, style=style)
        console.print(line)

    console.print("└" + "─" * (NUM_BINS * 2))
    console.print(f"{min_val:.1f}".ljust(NUM_BINS) + f"{max_val:.1f}".rjust(NUM_BINS))

def render_boxplots(df, var, group_var):
    """
    Renders horizontal boxplots for multiple groups in the terminal.
    """
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel

    console = Console()
    clean_df = df[[var, group_var]].dropna()
    groups = sorted(clean_df[group_var].unique())

    all_min = clean_df[var].min()
    all_max = clean_df[var].max()
    width = 40 # chars

    def scale(val):
        if all_max == all_min: return 0
        return int((val - all_min) / (all_max - all_min) * width)

    console.print(Panel(f"Boxplots for [bold]{var}[/bold] by [bold]{group_var}[/bold]", expand=False))

    for i, g in enumerate(groups):
        data = clean_df[clean_df[group_var] == g][var].values
        if len(data) == 0: continue

        q1, median, q3 = np.percentile(data, [25, 50, 75])
        mi, ma = np.min(data), np.max(data)

        s_mi, s_q1, s_me, s_q3, s_ma = map(scale, [mi, q1, median, q3, ma])

        # Build the horizontal line
        line = [" "] * (width + 1)

        # Whiskers
        for j in range(s_mi, s_q1): line[j] = "─"
        for j in range(s_q3 + 1, s_ma + 1): line[j] = "─"

        # Box
        line[s_q1] = "├"
        for j in range(s_q1 + 1, s_q3): line[j] = "█"
        line[s_q3] = "┤"

        # Median
        line[s_me] = "║"

        # End caps
        line[s_mi] = "╟" if line[s_mi] == "─" else line[s_mi]
        line[s_ma] = "╢" if line[s_ma] == "─" else line[s_ma]

        # Colors: Cycle through cyan, magenta, yellow, green
        colors = ["cyan", "magenta", "yellow", "green"]
        color = colors[i % len(colors)]

        row = Text(f"{str(g)[:10]:>10} │ ")
        row.append("".join(line), style=f"bold {color}")
        console.print(row)

    # Scale legend
    footer = Text(" " * 13 + "└" + "─" * width + "┘")
    console.print(footer)
    labels = Text(" " * 13 + f"{all_min:.1f}".ljust(width // 2) + f"{all_max:.1f}".rjust(width // 2 + (width % 2)))
    console.print(labels)
