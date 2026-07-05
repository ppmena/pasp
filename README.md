# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis, specifically optimized for use in mobile environments like **Android with Termux**, as well as any other terminal.

## Features

- **v0.3.5 Robust CLI**: Improved command-line interface that supports both direct file analysis and subcommands seamlessly.
- **v0.3.4 Easy Updates**: Use the `update` command to stay on the latest version from GitHub.
- **v0.3.3 Visual Insights**: Use the `--plot` flag with independent samples t-tests to see a comparative histogram.
- **v0.3.2 Non-parametric Depth**: Automatic **Dunn's Test** with Bonferroni correction for Kruskal-Wallis post-hoc analysis.
- **v0.3.1 Fully in English**: All results and reports are displayed in English.
- **v0.3 Intelligent Analysis**: Automatic verification of statistical assumptions (Normality, Homogeneity) with robust (Welch) or non-parametric fallbacks.
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

# Independent T-Test with plot
pasp data.csv --ttest-ind score group --plot
```

### Style B: Subcommands

```bash
pasp descriptives data.csv
pasp anova data.csv score group
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
