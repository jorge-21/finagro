# How subsidized rural credit may affect Colombia's lending-rate benchmark

> An applied data and policy analysis using Finagro and Colombian Financial Superintendency microdata.

[![Python](https://img.shields.io/badge/Python-data%20analysis-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Status](https://img.shields.io/badge/status-research%20in%20progress-F59E0B)](#project-status)
[![Language](https://img.shields.io/badge/notebooks-Spanish-6B7280)](#repository-guide)

## The question

Finagro channels a material share of Colombian rural credit at comparatively low rates. Those operations are included in the data used to calculate the **IBC** (*Interés Bancario Corriente*), a benchmark published by the Colombian Financial Superintendency.

This project investigates a potential feedback mechanism:

1. Finagro lending enters the observed market-rate calculation.
2. Lower-rate lending may reduce the measured IBC for a credit segment.
3. Because regulatory interest-rate caps are derived from certified benchmark rates under product-specific rules, this composition effect may also influence the rate ceiling faced by other lenders.

The objective is to estimate the magnitude of that accounting effect by credit product and distinguish it from broader monetary and market trends.

> **Interpretation:** this is an observational and decomposition-based analysis. It does not claim that the regression coefficients identify a clean causal effect.

## Why it matters

A benchmark intended to describe market credit conditions may also be affected by subsidized or policy-driven lending included in its calculation. If that effect is economically material, it changes how the benchmark should be interpreted and may have consequences for credit supply outside Finagro.

The project connects:

- financial regulation and public policy;
- large-scale public-data engineering;
- benchmark replication and validation;
- market composition and rate decomposition;
- time-series modeling with macroeconomic controls.

## Data

The analysis combines:

| Source | Role in the analysis |
|---|---|
| **Finagro microdata** | Credit-level operations, rates, borrower and geographic attributes |
| **SFC open data** | Market disbursements and effective rates by institution and product |
| **Banco de la República** | DTF, IBR and one-year TES macro-financial controls |
| **DIVIPOLA** | Geographic standardization across sources |

The two main processed datasets are approximately **839 MB** and **1.55 GB**. Large files are excluded from Git and downloaded separately; sources and file lineage are documented in [data/README.md](data/README.md).

## Analytical approach

```text
Public sources
      ↓
Ingestion and geographic standardization
      ↓
Finagro–SFC consolidation and quality bounds
      ↓
IBC replication and validation
      ↓
Finagro / non-Finagro rate and market-share analysis
      ↓
Shift-share decomposition + macro-controlled time-series models
      ↓
Estimated benchmark and regulatory-cap accounting effect
```

The main methods are:

- amount-weighted rate aggregation by product and period;
- replication of the official IBC methodology across five productive-credit segments;
- comparison against certified SFC benchmark rates;
- Finagro identification using observable channel and guarantee attributes;
- rate-gap and market-share decomposition;
- shift-share analysis of within-institution and between-institution changes;
- OLS with Newey–West HAC standard errors;
- reduced-model and Mann–Kendall robustness checks.

See [the detailed methodology](docs/METHODOLOGY.md) for formulas, assumptions and notebook-level documentation.

## Validation evidence

Benchmark replication has been validated for two rural productive-credit segments:

| Segment | Validated months | Period | Median error | MAE | Mean relative error |
|---|---:|---|---:|---:|---:|
| Productive Rural Credit | 22 | Apr 2024–Jan 2026 | +0.01 pp | 0.26 pp | 1.4% |
| Popular Productive Rural Credit | 24 | Jan 2024–Dec 2025 | +0.05 pp | 0.41 pp | 0.9% |

The near-zero median errors provide evidence against systematic bias in the replicated calculations for these segments. Validation remains pending for the aggregate, urban and popular-urban segments.

## Project status

**Research in progress.** The data pipeline and core analyses are implemented, but the final policy estimate should not be treated as definitive until the following work is complete:

- automate comparison with official certified rates;
- validate the remaining three productive-credit segments;
- reconcile and document the alternative Finagro identification rules;
- add sensitivity analysis for classification assumptions;
- produce a small, fully reproducible public sample;
- separate accounting decomposition from causal interpretation.

## Repository guide

| Path | Purpose |
|---|---|
| [`notebooks/0_ingesta`](notebooks/0_ingesta) | Finagro, SFC and Banco de la República ingestion |
| [`notebooks/1_consolidacion`](notebooks/1_consolidacion) | Source harmonization, filters and weekly aggregation |
| [`notebooks/2_analisis`](notebooks/2_analisis) | IBC replication, validation, rate gaps and final decomposition |
| [`notebooks/3_exploratorio`](notebooks/3_exploratorio) | Descriptive analysis of rural credit and borrower segments |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | Detailed analytical workflow, formulas and assumptions |
| [`docs/entregables`](docs/entregables) | Article and presentation deliverables |
| [`data/README.md`](data/README.md) | Dataset lineage, sizes and download instructions |
| [`CLAUDE.md`](CLAUDE.md) | Data schemas and operational conventions |

The working language of the notebooks and narrative deliverables is **Spanish**.

## Reproducing the analysis

```bash
git clone https://github.com/jorge-21/finagro.git
cd finagro
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The notebooks were authored in Google Colab. Large processed datasets are downloaded using the IDs and commands in [data/README.md](data/README.md). The SFC ingestion notebook requires a Socrata token supplied through the `SOCRATA_APP_TOKEN` environment variable.

### Current reproducibility limitation

Some ingestion notebooks still write to personal Google Drive paths, so the repository is reproducible for reading and downstream analysis but not yet as a fully portable end-to-end pipeline. This limitation is tracked explicitly rather than hidden.

## Tools

Python · pandas · Polars · NumPy · statsmodels · Altair · Plotly · Socrata API · Google Colab

## Author

**Jorge Fuentes**  
Business strategy, product analytics and applied data science.

This repository is part of an applied research project on financial inclusion and rural credit in Colombia.
