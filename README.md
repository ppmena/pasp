# PASP: Portable Android Statistics Program

PASP is a lightweight, local statistical analysis tool designed for the terminal. Inspired by the philosophy of JASP, it aims to provide a clean and intuitive interface for statistical analysis, specifically optimized for use in mobile environments like **Android with Termux**, as well as any other terminal.

## Features

- **Descriptive Statistics**: Mean, Median, Mode, Standard Deviation, Skewness, Kurtosis, and more.
- **T-Tests**: One-sample, Independent samples, and Paired samples t-tests.
- **Linear Regression**: Simple linear regression with key diagnostic statistics.
- **Beautiful Output**: Clean, APA-style tables in your terminal using `rich`.
- **Lightweight**: Fast execution and minimal dependencies, perfect for mobile devices.

## Installation

You can install PASP directly from GitHub:

```bash
pip install git+https://github.com/user/pasp.git
```

Or for local development:

```bash
git clone https://github.com/user/pasp.git
cd pasp
pip install .
```

## Usage

PASP is designed to be used from the command line.

### Basic Descriptive Statistics

```bash
pasp descriptives data.csv --vars height weight
```

### T-Tests

```bash
# Independent samples t-test
pasp ttest-ind data.csv --group gender --vars score

# Paired samples t-test
pasp ttest-paired data.csv --vars pre_test post_test
```

### Linear Regression

```bash
pasp regression data.csv --dep weight --indep height
```

## License

MIT
