import numpy as np

def render_comparative_histogram(g1_data, g2_data, g1_name, g2_name):
    """
    Renders a comparative histogram in the terminal using rich.
    g1_data, g2_data: pandas Series or numpy arrays.
    """
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel

    console = Console()

    # Handle NaNs
    d1 = g1_data.dropna().values
    d2 = g2_data.dropna().values

    if len(d1) == 0 or len(d2) == 0:
        return

    # Constraints for Termux/Mobile
    MAX_WIDTH = 40
    MAX_HEIGHT = 10
    NUM_BINS = 20

    # Calculate global range
    combined = np.concatenate([d1, d2])
    min_val, max_val = np.min(combined), np.max(combined)

    if min_val == max_val:
        max_val += 1

    bins = np.linspace(min_val, max_val, NUM_BINS + 1)

    # Calculate frequencies
    freq1, _ = np.histogram(d1, bins=bins)
    freq2, _ = np.histogram(d2, bins=bins)

    # Normalize frequencies to MAX_HEIGHT
    max_freq = max(np.max(freq1), np.max(freq2))
    if max_freq == 0: return

    scale = MAX_HEIGHT / max_freq
    f1_scaled = (freq1 * scale).astype(int)
    f2_scaled = (freq2 * scale).astype(int)

    # Legend
    legend = Text.assemble(
        (f"█", "bold cyan"), f" {g1_name}   ",
        (f"█", "bold magenta"), f" {g2_name}   ",
        (f"▒", "bold white"), " Overlap"
    )
    console.print(Panel(legend, title="Distribution Plot", expand=False))

    # Render from top to bottom
    for h in range(MAX_HEIGHT, 0, -1):
        line = Text()
        # Add Y axis
        line.append("│", style="white")

        for b in range(NUM_BINS):
            char = " "
            style = ""

            in_g1 = f1_scaled[b] >= h
            in_g2 = f2_scaled[b] >= h

            if in_g1 and in_g2:
                char = "▒"
                style = "bold white"
            elif in_g1:
                char = "█"
                style = "bold cyan"
            elif in_g2:
                char = "█"
                style = "bold magenta"

            # Use 2 chars per bin for better visibility
            line.append(char * 2, style=style)

        console.print(line)

    # X Axis
    x_axis = Text("└" + "─" * (NUM_BINS * 2))
    console.print(x_axis)

    # X labels
    labels = Text(f"{min_val:.1f}".ljust(NUM_BINS) + f"{max_val:.1f}".rjust(NUM_BINS))
    console.print(labels)
