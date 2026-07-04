# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis, specifically optimized for use in mobile environments like **Android with Termux**, as well as any other terminal.

## Features

- **v0.3.3 Visual Insights**: Use the `--plot` flag with independent samples t-tests to see a comparative histogram in your terminal.
- **v0.3.2 Non-parametric Depth**: Automatic **Dunn's Test** with Bonferroni correction for Kruskal-Wallis post-hoc analysis.
- **v0.3.1 Fully in English**: All results and reports are displayed in English.
- **v0.3 Intelligent Analysis**: Automatic verification of statistical assumptions (Normality, Homogeneity).
- **v0.3 Robust Tests**: Automatically applies corrections (Welch) or non-parametric alternatives (Mann-Whitney, Wilcoxon, Kruskal-Wallis) when assumptions fail.
- **Descriptive Statistics**: Automatic variable classification (Nominal, Ordinal, Scale) with APA-style tables.
- **T-Tests**: One-sample, Independent samples, and Paired samples.
- **ANOVA**: One-way Analysis of Variance with automatic Post-Hoc comparisons (Bonferroni).
- **Correlation**: Pearson correlation matrix.
- **Linear Regression**: Simple linear regression.
- **Beautiful Output**: Clean tables and plots in your terminal using `rich`.
- **Lightweight & Lazy**: Fast startup; heavy dependencies are only loaded when needed.

## Installation

### Quick Installation

```bash
pip install git+https://github.com/ppmena/pasp
```

### Recommended Installation for Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python clang make cmake pkg-config ninja meson
pip install git+https://github.com/ppmena/pasp
```

## Usage

### Style A: Direct usage on a file

```bash
pasp data.csv --auto
pasp data.csv --ttest-ind score gender --plot
```

### Style B: Subcommands

```bash
pasp descriptives data.csv var1 var2
pasp ttest-ind data.csv score gender --plot
```

## Diagnostics and Help

```bash
pasp doctor
pasp install-help
pasp examples
```

## Example Datasets

PASP includes several example datasets to help you get started:

- **`ejemplo_anova.csv`**: Data for ANOVA.
- **`ejemplo_ttest.csv`**: Data for T-tests.
- **`ejemplo_ttest_one.csv`**: Data for one-sample tests.
- **`ejemplo_ttest_paired.csv`**: Data for paired samples tests.
- **`ejemplo_correlacion.csv`**: Data for correlation.
- **`ejemplo_regresion.csv`**: Data for regression.

You can view them by running `pasp examples`.

## License

MIT
