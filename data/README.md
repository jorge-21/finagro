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
| `tasas_banrep_semanal.csv` | 0.05 MB | ✅ | `notebooks/0_ingesta/Ingesta_BanRep.ipynb` | `1GGsdRufXrUE651qFNEeTEepRJnDDK3B3` |

Para descargar los grandes:

```bash
pip install gdown
gdown 1KMwal7BjIhbOV2k4UC1duRqQXrEM5Gxi -O "data/processed/dataset_finagro.csv"
gdown 1pqULCPNUfiZ1H9bvtahu2gJOBbHPnVMr -O "data/processed/datos_procesados (1).csv"
```

## IDs auxiliares de Drive (hoy solo dentro de los notebooks)

Estos insumos no son salidas del pipeline pero los notebooks los bajan con
`gdown` en Colab. Se documentan aquí para que el grafo de datos tenga **una sola
fuente de verdad** y no haya que abrir cada notebook para reconstruirlo. Versiones
equivalentes de `ibr`/`dtf` viven además en `raw/` (mismos datos, distinto formato).

| Insumo | Usado por | Drive ID |
|---|---|---|
| `divipola.xlsx` (DIVIPOLA municipios) | `Ingesta_Finagro.ipynb`, `Ingesta_SFC.ipynb` | `17nXNQBaf2gi1O9ODFOtBUg_cR0j7s4rS` |
| `ibr.csv` (insumo IBR) | `Ingesta_Finagro.ipynb` | `1Mciuo3swfSSoyWhJ3QZfnKzxeZzWYeUw` |
| `dtf.csv` (insumo DTF) | `Ingesta_Finagro.ipynb` | `10PwPBPrEAjLtAGKqVQJ1rx-ov0UPtZYC` |

> **Nota de reproducibilidad:** las ingestas de Finagro y BanRep escriben su salida
> a rutas personales de Drive (`/content/drive/MyDrive/U/Maestría/...` y
> `/MyDrive/finagro/...`). Por eso re-correr una ingesta no actualiza por sí solo
> el archivo que los notebooks de aguas abajo bajan por ID — para otra persona el
> pipeline solo es reproducible de lectura (vía los IDs de arriba), no de escritura.
