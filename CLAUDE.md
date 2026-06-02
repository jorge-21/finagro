# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this workspace is

Data-analysis repository studying rural credit in Colombia and the feedback effect of the IBC (Índice Bancario de Crédito) — built from Finagro microdatos and SFC (Superintendencia Financiera) data published on `datos.gov.co`. It is a git repo with a `requirements.txt` (pinned scientific stack), but **no build/lint/test tooling** — the work is Colab-authored Jupyter notebooks, large CSVs, and the Word/PowerPoint deliverables they support.

Working language is Spanish. Filenames use accented characters (`Análisis`, `Consolidación`, `créditos`) and spaces — always quote paths in shell commands.

The narrative source of truth for the analysis is [`README.md`](README.md), which walks the pipeline step by step (sections 0–9). This file documents data conventions and operational gotchas.

## Repository layout

```
notebooks/   código del pipeline, ordenado por etapa (0_ingesta → 1_consolidacion → 2_analisis → 3_exploratorio)
data/        insumos (raw/) y salidas (processed/); los multi-GB no están versionados — ver data/README.md
docs/        metodologia/ (referencias de cálculo) y entregables/ (artículo y presentaciones)
```

The notebooks were authored in Google Colab and read their inputs **by bare filename** (`pd.read_csv('datos.csv')`), assuming the file sits in the working directory (`/content/` in Colab). On-disk folder structure therefore does **not** affect notebook execution — only the path repointing you do when running locally.

## Pipeline overview

Two ingestion notebooks produce the bulk datasets, one consolidation notebook joins them, and the analysis notebooks run downstream. Read them in this order to understand any column or metric:

1. **Ingesta — Finagro** — [`notebooks/0_ingesta/Ingesta_Finagro.ipynb`](notebooks/0_ingesta/Ingesta_Finagro.ipynb) builds `dataset_finagro.csv` (839 MB) from raw Finagro microdatos joined with DIVIPOLA (municipios), IBR, and DTF series. Authoritative rate column is **`tasa_credito`** — a markdown cell explicitly says *"nos vamos con tasa_credito como fuente de verdad"*; do not switch downstream code to `tasa_indexacion` or `tasa_credito_new` without checking with the user.
2. **Ingesta — SFC** — [`notebooks/0_ingesta/Ingesta_SFC.ipynb`](notebooks/0_ingesta/Ingesta_SFC.ipynb) pulls SFC data via the Socrata API (`www.datos.gov.co`, `sodapy` client) and writes `datos_procesados.csv` (1.55 GB) and `microcredito.csv` (1.28 GB). **Security note:** the Socrata `APP_TOKEN` that was previously hard-coded here has been moved to the `SOCRATA_APP_TOKEN` environment variable. The old token leaked in the source workspace — treat it as compromised and rotate it on datos.gov.co; never re-inline a token into a notebook.
3. **Ingesta — BanRep** — [`notebooks/0_ingesta/Ingesta_BanRep.ipynb`](notebooks/0_ingesta/Ingesta_BanRep.ipynb) pulls TES / IBR / DTF macro benchmark series and writes `tasas_banrep_semanal.csv` (weekly, Friday close) — the macro controls used in the regressions.
4. **Consolidación** — [`notebooks/1_consolidacion/Consolidación_Finagro_y_SFC.ipynb`](notebooks/1_consolidacion/Consolidación_Finagro_y_SFC.ipynb) joins Finagro and SFC sides, applies bounds, computes weekly aggregations (`Agrupar por viernes`), and FAG % series.
5. **Análisis** — in `notebooks/2_analisis/`:
   - [`Cálculo_IBC.ipynb`](notebooks/2_analisis/Cálculo_IBC.ipynb) — IBC computation across the 5 Crédito Productivo segments (the headline feedback analysis; weighted by montos desembolsados).
   - [`Peso_Finagro_en_SFC.ipynb`](notebooks/2_analisis/Peso_Finagro_en_SFC.ipynb) — Finagro's market share by product, with lower/upper bound definitions.
   - [`Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) — **the payoff**: tasa gap Finagro vs no-Finagro, shift-share, Newey-West regressions, and the final number (efecto Finagro sobre el IBC + techo de usura). Despite the historical naming, the quantitative close lives here, not in the IBC notebook.
6. **Exploratorio** — in `notebooks/3_exploratorio/`:
   - [`Descriptiva_Finagro.ipynb`](notebooks/3_exploratorio/Descriptiva_Finagro.ipynb) — descriptive view of the Finagro side: temporal trends, distribution by línea / tipo de productor / municipio, IBR-cartera relationship.
   - [`Exploratorio_nuevos_créditos.ipynb`](notebooks/3_exploratorio/Exploratorio_nuevos_créditos.ipynb) — producer-size segmentation (grande / mediano / microempresario), ruralidad vs no-ruralidad, tasas altas, nuevos destinatarios.

Narrative outputs in `docs/entregables/` (Spanish) are what these notebooks support: the article `Artículo_ Efecto de retroalimentación del IBC.docx` plus two decks. Methodology references live in `docs/metodologia/`: `Tasas IBC Crédito Productivo.xlsx` (also the IBC validation artifact), `metodología de cálculo de la tasa de interés.docx`, `ibc11_25 (2).docx`, `Anexo 1.3 Condiciones Financieras (2025).xlsx`, `Documento_Referencia-Antecedentes_F._414 (1).docx`.

## Datasets and schemas

The large CSVs are **not versioned** (they exceed GitHub's 100 MB limit) — they live in `data/processed/` locally and are re-downloaded from Google Drive with the IDs in [`data/README.md`](data/README.md). **Do not re-run the `gdown` cells** blindly — they exist for Colab and would re-download multi-GB files. When running locally, repoint `pd.read_csv('datos.csv')` / `pd.read_csv('dataset_finagro.csv')` at the corresponding file under `data/`.

- **`data/processed/dataset_finagro.csv`** (839 MB) — Finagro microdatos, one row per credit. Drive ID `1KMwal7BjIhbOV2k4UC1duRqQXrEM5Gxi`. Columns: `id_credito, fecha_credito, cod_municipio, tipo_cartera, tipo_intermediario, tipo_productor, tipo_beneficiario, tipo_persona, sexo, cod_destino, linea_credito, cadena, eslabon_cadena, valor_credito, valor_inversion, plazo, periodo_gracia, cuotas, cuotas_capital, tasa_indexacion, periodicidad_tasa_indexacion, puntos_adicionales, garantia_fag, nombre_programa, indicador_lec, valor_subsidio, nuevo, cod_departamento, nombre_departamento, nombre_municipio, tipo_municipio, tasa_indexacion_valor, tasa_credito, tasa_credito_new`. Always read with `dtype={'cod_municipio': str, 'cod_departamento': str}` (these are categorical codes, not numbers).
- **`data/processed/datos_procesados (1).csv`** (1.55 GB) — SFC processed full dataset (post-`Ingesta_SFC.ipynb`), with municipio join, `year_month`, `tasa_ponderada`, `costo_credito`, `costo_credito_ponderado`. Drive ID `1pqULCPNUfiZ1H9bvtahu2gJOBbHPnVMr`. Columns: `tipo_entidad, nombre_tipo_entidad, codigo_entidad, nombre_entidad, fecha_corte, tipo_de_persona, sexo, tama_o_de_empresa, tipo_de_cr_dito, tipo_de_garant_a, producto_de_cr_dito, plazo_de_cr_dito, tasa_efectiva_promedio, margen_adicional_a_la, montos_desembolsados, numero_de_creditos, grupo_etnico, antiguedad_de_la_empresa, tipo_de_tasa, rango_monto_desembolsado, clase_deudor, codigo_ciiu, cod_municipio, plazo_de_cr_dito_num, tasa_ponderada, mes, year, year_month, costo_credito, costo_credito_ponderado, cod_departamento, nombre_departamento, nombre_municipio, tipo_municipio`.
- **`data/processed/microcredito.csv`** (1.28 GB) — SFC microcredit subset, narrower schema (no `year_month`, `tasa_ponderada`, `costo_credito*`, municipio join). Use this when restricted to microcredit; use `datos_procesados (1).csv` for full coverage.
- **`data/processed/microcredito.xlsx`** (2 MB) — older or sampled version of the microcredit data.
- **`data/raw/`** — small external series kept in-repo: `dtf.csv`, `ibr.csv`, `tes.csv`, `desembol-resumen.xls`.

The underscored columns like `tipo_de_cr_dito`, `tama_o_de_empresa`, `tipo_de_garant_a`, `plazo_de_cr_dito` are accent-stripped artifacts from the upstream Socrata feed (originally `tipo_de_crédito`, `tamaño_de_empresa`, etc.). **Do not "fix" them** — code throughout the analysis notebooks references these names exactly.

## Working notes

- All notebooks were authored in Google Colab; they reference `/content/...` paths and use `gdown` to fetch sources. When running locally, swap to the corresponding file under `data/` rather than redownloading.
- The Finagro-side notebooks use `polars` for the heavier passes and fall back to `pandas` for plotting and joins; SFC-side and consolidation are pure `pandas` + `altair`. Match the pattern of the notebook you're editing.
- Non-stdlib pip dependencies are minimal: `squarify` (treemaps in the Finagro notebooks) and `sodapy` (Socrata client in the SFC ingestion notebook). Everything else is the standard scientific stack: pandas, numpy, polars, matplotlib, seaborn, altair, plotly, requests. Pinned versions in `requirements.txt`.
- Notebook outputs are committed (large embedded PNGs / base64), which is why `notebooks/0_ingesta/Ingesta_SFC.ipynb` is ~32 MB and `notebooks/3_exploratorio/Exploratorio_nuevos_créditos.ipynb` is ~9 MB. Be deliberate about regenerating cells — clear outputs you don't intend to ship, or the file size compounds. (`.claude/hooks/strip-notebook.py` exists to help with this.)
- `.claude/settings.local.json` exists for permissions only (and is gitignored); don't put project conventions there — extend this file instead.
