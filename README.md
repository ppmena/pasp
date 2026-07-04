# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis, specifically optimized for use in mobile environments like **Android with Termux**, as well as any other terminal.

## Features

- **Descriptive Statistics**: Mean, Median, Mode, Standard Deviation, Skewness, Kurtosis, and more.
- **T-Tests**: One-sample, Independent samples, and Paired samples t-tests.
- **ANOVA**: One-way Analysis of Variance.
- **Correlation**: Pearson correlation matrix.
- **Linear Regression**: Simple linear regression with key diagnostic statistics.
- **Beautiful Output**: Clean, APA-style tables in your terminal using `rich` (with plain-text fallback).
- **Lightweight & Lazy**: Fast startup; heavy dependencies are only loaded when needed.
- **Diagnostics**: Built-in tools to check your environment and fix installation issues.

## Installation

### Quick Installation

```bash
pip install git+https://github.com/ppmena/PASP.git
```

### Recommended Installation for Termux (Android)

To avoid issues with scientific dependencies, follow these steps:

1. **Update packages**:
   ```bash
   pkg update && pkg upgrade
   ```
2. **Install build tools and dependencies**:
   ```bash
   pkg install python clang make cmake pkg-config ninja meson
   ```
3. **Install PASP**:
   ```bash
   pip install git+https://github.com/ppmena/PASP.git
   ```

## Usage

PASP supports two styles of usage.

### Style A: Direct usage on a file

```bash
# Automatic summary and descriptives
pasp data.csv --auto

# Show data summary only
pasp data.csv --summary

# Run specific analyses
pasp data.csv --descriptives --vars height weight
pasp data.csv --anova score group
pasp data.csv --correlation var1 var2 var3
pasp data.csv --ttest-ind score gender
pasp data.csv --ttest-one height 170
pasp data.csv --ttest-paired pre post
pasp data.csv --regression weight height
```

### Style B: Subcommands

```bash
pasp descriptives data.csv var1 var2
pasp anova data.csv score group
pasp correlation data.csv var1 var2 var3
pasp ttest-ind data.csv score gender
pasp ttest-one data.csv height 170
pasp ttest-paired data.csv pre post
pasp regression data.csv weight height
```

## Diagnostics and Help

If you encounter issues, use the built-in diagnostic tools (these work even without dependencies):

```bash
# Check system and dependencies
pasp doctor

# Show detailed installation help for Termux/Linux/macOS
pasp install-help

# List available example datasets
pasp examples
```

## Example Datasets

PASP includes example datasets. You can list them with `pasp examples`.

- **`ejemplo_anova.csv`**: Data for ANOVA and descriptives.
  - *Usage*: `pasp anova examples/ejemplo_anova.csv score age`
- **`ejemplo_correlacion.csv`**: Data for correlation analysis.
  - *Usage*: `pasp correlation examples/ejemplo_correlacion.csv var1 var2 var3`
- **`ejemplo_ttest.csv`**: Data for independent samples t-test.
  - *Usage*: `pasp ttest-ind examples/ejemplo_ttest.csv recovery_time treatment`
- **`ejemplo_regresion.csv`**: Relationship between hours studied and exam scores.
  - *Usage*: `pasp regression examples/ejemplo_regresion.csv exam_score hours_studied`

## Troubleshooting

### `ninja` or `mesonpy` errors in Termux
Do not install `ninja` or `meson` via `pip`. Install them using `pkg`:
```bash
pkg install ninja meson
```

### `pasp` command not found
Ensure your Python bin directory is in your PATH. In Termux:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## License

MIT
