# Datos

Insumos y salidas del pipeline. Los datasets multi-GB **no están versionados**
(exceden el límite de 100 MB de GitHub) — se re-descargan desde Google Drive con
los IDs de abajo. Los esquemas completos de columnas viven en
[`../CLAUDE.md`](../CLAUDE.md).

> Los notebooks fueron escritos en Colab y leen sus insumos **por nombre de
> archivo pelado** (p. ej. `pd.read_csv('dataset_finagro.csv')`), asumiendo el
> archivo en el directorio de trabajo. Al correr localmente, copia el archivo
> junto al notebook o repunta el `read_csv` a la ruta correspondiente de aquí.

## `raw/` — insumos externos descargados tal cual

| Archivo | Tamaño | En repo | Fuente |
|---|---|---|---|
| `dtf.csv` | 0.06 MB | ✅ | DTF 90 días (BanRep) |
| `ibr.csv` | 0.15 MB | ✅ | IBR overnight (BanRep) |
| `tes.csv` | 0.23 MB | ✅ | TES Cero Cupón 1 año (BanRep) |
| `desembol-resumen.xls` | 0.09 MB | ✅ | Resumen de desembolsos |

## `processed/` — salidas generadas por los notebooks de ingesta

| Archivo | Tamaño | En repo | Generado por | Drive ID |
|---|---|---|---|---|
| `dataset_finagro.csv` | 839 MB | ❌ descarga | `notebooks/0_ingesta/Ingesta_Finagro.ipynb` | `1KMwal7BjIhbOV2k4UC1duRqQXrEM5Gxi` |
| `datos_procesados (1).csv` | 1.55 GB | ❌ descarga | `notebooks/0_ingesta/Ingesta_SFC.ipynb` | `1pqULCPNUfiZ1H9bvtahu2gJOBbHPnVMr` |
| `microcredito.csv` | 1.28 GB | ❌ descarga | `notebooks/0_ingesta/Ingesta_SFC.ipynb` | — |
| `microcredito.xlsx` | 1.99 MB | ✅ | versión muestreada/antigua del microcrédito | — |
| `tasas_banrep_semanal.csv` | 0.05 MB | ✅ | `notebooks/0_ingesta/Ingesta_BanRep.ipynb` | — |

Para descargar los grandes:

```bash
pip install gdown
gdown 1KMwal7BjIhbOV2k4UC1duRqQXrEM5Gxi -O "data/processed/dataset_finagro.csv"
gdown 1pqULCPNUfiZ1H9bvtahu2gJOBbHPnVMr -O "data/processed/datos_procesados (1).csv"
```
