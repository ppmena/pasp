# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis. While specifically optimized for mobile environments like **Android with Termux**, PASP is **fully cross-platform** and can be installed on any operating system (Windows, macOS, Linux) with Python and pip.

## Features

- **v0.4.3 Advanced Regression**: Preliminary descriptives (Mean, SD, Skewness, Kurtosis) and terminal scatter plots for regression.
- **v0.4.2 Smart Correlation**: Automatic bivariate normality checks with Spearman fallback and optimized text output.
- **v0.4.1 UI Polish**: Fixed p-value formatting for numeric group labels and enhanced descriptive tables.
- **v0.4.0 Variable Indexing**: Refer to variables by their index (e.g., `anova 2 4`) or their name.
- **v0.3.8 ANOVA Boxplots**: Use the `--plot` flag with ANOVA to see group-wise horizontal boxplots.
- **v0.3.7 Strict ANOVA Evaluation**: Detailed verification of residuals' normality, homogeneity of variances, and outlier detection.
- **v0.3.5 Robust CLI**: Improved command-line interface supporting both direct file analysis and subcommands seamlessly.
- **v0.3.4 Easy Updates**: Use the `update` command to stay on the latest version from GitHub.
- **v0.3.3 Visual Insights**: Use the `--plot` flag with independent samples t-tests to see a comparative histogram.
- **v0.3 Intelligent Analysis**: Automatic verification of statistical assumptions with robust (Welch) or non-parametric fallbacks.
- **Beautiful Output**: Clean APA-style tables in your terminal using `rich`.

## Installation

### Quick Installation

```bash
pip install git+https://github.com/ppmena/pasp
```

### Update to Latest Version

```bash
pasp update
```

### Recommended Installation for Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python clang make cmake pkg-config ninja meson
pip install git+https://github.com/ppmena/pasp
```

## Usage

PASP supports two styles of usage. For more details, run `pasp --help`.

### Style A: Direct usage on a file

```bash
# Automatic analysis
pasp data.csv --auto

# One-way ANOVA using indices (e.g., column 3 as DV, column 5 as Group)
pasp data.csv --anova 3 5 --plot

# Independent T-Test with comparative histogram
pasp data.csv --ttest-ind score gender --plot
```

### Style B: Subcommands

```bash
pasp anova data.csv 3 5 --plot
```

## Diagnostics and Help

```bash
pasp doctor
pasp examples
pasp install-help
```

## Example Datasets

Run `pasp examples` to see the list of included CSV files for testing.

## License

MIT
