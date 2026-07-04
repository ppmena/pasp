# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis, specifically optimized for use in mobile environments like **Android with Termux**, as well as any other terminal.

## Features

- **v0.3 Intelligent Analysis**: Automatic verification of statistical assumptions (Normality, Homogeneity).
- **v0.3 Robust Tests**: Automatically applies corrections (Welch) or non-parametric alternatives (Mann-Whitney, Wilcoxon, Kruskal-Wallis) when assumptions fail.
- **Descriptive Statistics**: Automatic variable classification (Nominal, Ordinal, Scale) with APA-style tables.
- **T-Tests**: One-sample, Independent samples, and Paired samples.
- **ANOVA**: One-way Analysis of Variance with automatic Post-Hoc comparisons (Bonferroni).
- **Correlation**: Pearson correlation matrix.
- **Linear Regression**: Simple linear regression.
- **Beautiful Output**: Clean tables in your terminal using `rich` (with plain-text fallback).
- **Lightweight & Lazy**: Fast startup; heavy dependencies are only loaded when needed.

## Installation

### Quick Installation

```bash
pip install git+https://github.com/ppmena/PASP.git
```

### Recommended Installation for Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python clang make cmake pkg-config ninja meson
pip install git+https://github.com/ppmena/PASP.git
```

## Usage

### Style A: Direct usage on a file

```bash
pasp data.csv --auto
pasp data.csv --anova score group
pasp data.csv --ttest-ind score gender
```

### Style B: Subcommands

```bash
pasp descriptives data.csv var1 var2
pasp anova data.csv score group
pasp ttest-ind data.csv score gender
```

## Diagnostics and Help

```bash
pasp doctor
pasp install-help
pasp examples
```

## Example Datasets

- **`ejemplo_anova.csv`**: Data for ANOVA.
- **`ejemplo_ttest.csv`**: Data for T-tests.
- **`ejemplo_correlacion.csv`**: Data for correlation.
- **`ejemplo_regresion.csv`**: Data for regression.

## License

MIT
