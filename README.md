# Efecto de retroalimentación del IBC

Análisis del efecto de retroalimentación del **IBC** (Índice Bancario de Crédito) sobre el crédito rural en Colombia, construido a partir de microdatos de **Finagro** y datos de la **SFC** (Superintendencia Financiera) publicados en `datos.gov.co`.

La hipótesis central: como Finagro coloca volumen importante a tasas bajas, **deprime mecánicamente el IBC** que la SFC publica cada mes, y por consiguiente baja el **techo de usura** que rige al mes siguiente — afectando al crédito que *no es* Finagro. El objetivo del análisis es cuantificar ese efecto producto por producto y separarlo del ciclo macro de BanRep.

Idioma de trabajo: **español**. Archivos con tildes y espacios — siempre entrecomillar rutas en shell. Convenciones de datos, columnas y notas operativas viven en [CLAUDE.md](CLAUDE.md); este README cuenta **el paso a paso del análisis**.

---

## Estructura del repositorio

```
finagro/
├── notebooks/                    código del pipeline (ordenado por etapa)
│   ├── 0_ingesta/                Ingesta_Finagro · Ingesta_SFC · Ingesta_BanRep
│   ├── 1_consolidacion/          Consolidación_Finagro_y_SFC
│   ├── 2_analisis/               Cálculo_IBC · Peso_Finagro_en_SFC · Gap_Tasas_Finagro_vs_NoFinagro (el cierre)
│   └── 3_exploratorio/           Descriptiva_Finagro · Exploratorio_nuevos_créditos
├── data/                         insumos y salidas (los multi-GB van por Drive — ver data/README.md)
│   ├── raw/                      series macro descargadas (dtf, ibr, tes, …)
│   └── processed/                datasets generados por la ingesta
├── docs/
│   ├── metodologia/              referencias de cálculo del IBC y la tasa
│   └── entregables/              artículo y presentaciones
├── README.md                     este archivo — el paso a paso del análisis
├── CLAUDE.md                     convenciones de datos y notas operativas
└── requirements.txt
```

Los notebooks corren en Colab y leen sus insumos **por nombre de archivo pelado**; la ubicación en disco no afecta su ejecución (ver [`data/README.md`](data/README.md)).

---

## 0. Consolidación de datos (prerrequisito)

**Notebook:** [`notebooks/1_consolidacion/Consolidación_Finagro_y_SFC.ipynb`](notebooks/1_consolidacion/Consolidación_Finagro_y_SFC.ipynb)
**Inputs:** [`data/processed/dataset_finagro.csv`](data/processed/) (839 MB), [`data/processed/datos_procesados (1).csv`](data/processed/) (1.55 GB)

ETL que une el lado Finagro con el lado SFC, aplica cotas (rangos válidos de tasa, plazo y monto), clasifica créditos por garantía (FAG / FNG / sin garantía) y por tipo de beneficiario (Productivo / Popular × Rural / Urbano), y agrega a **frecuencia semanal con cierre de viernes** (`Agrupar por viernes`) para alinear contra series macro.

La tasa "fuente de verdad" del lado Finagro es la columna `tasa_credito` (no `tasa_indexacion` ni `tasa_credito_new`).

---

## 1. Cálculo del IBC por tipo de crédito

**Notebook:** [`notebooks/2_analisis/Cálculo_IBC.ipynb`](notebooks/2_analisis/Cálculo_IBC.ipynb)

Reproduce la metodología SFC/BanRep para calcular el IBC en los **5 segmentos de Crédito Productivo**:

- Crédito Productivo (agregado)
- Crédito Productivo **Rural**
- Crédito Productivo **Popular Rural**
- Crédito Productivo **Urbano**
- Crédito Productivo **Popular Urbano**

**Fórmula** — promedio ponderado por monto desembolsado dentro de cada segmento y semana:

$$\text{IBC}_{p,t} = \frac{\sum_i \text{tasa\\_efectiva\\_promedio}_i \cdot \text{montos\\_desembolsados}_i}{\sum_i \text{montos\\_desembolsados}_i}$$

Referencias metodológicas: [`docs/metodologia/Tasas IBC Crédito Productivo.xlsx`](docs/metodologia/Tasas%20IBC%20Cr%C3%A9dito%20Productivo.xlsx), [`docs/metodologia/metodología de cálculo de la tasa de interés.docx`](docs/metodologia/), [`docs/metodologia/ibc11_25 (2).docx`](docs/metodologia/).

---

## 2. Validación contra el IBC publicado por BanRep/SFC

**Referencia:** [`docs/metodologia/Tasas IBC Crédito Productivo.xlsx`](docs/metodologia/Tasas%20IBC%20Cr%C3%A9dito%20Productivo.xlsx) — comparación mes a mes entre `TIBC certificada` (oficial SFC) y `IBC Manual` (calculado en el paso 1).

**Estado: parcialmente completa.** Para los segmentos validados el ajuste es muy bueno y el método se considera correcto:

| Segmento | Meses validados | Rango | Mediana de error | MAE | Error rel. medio |
|---|---|---|---|---|---|
| Crédito Productivo Rural | 22 | abr-2024 → ene-2026 | **+0.01pp** | 0.26pp | 1.4 % |
| Crédito Productivo Popular Rural | 24 | ene-2024 → dic-2025 | **+0.05pp** | 0.41pp | 0.9 % |

Mediana ≈ 0 → **no hay sesgo sistemático**. MAE de basis points sobre tasas de 17–50 % es buen ajuste para una replicación con microdatos.

**Pendiente:** validar los otros 3 segmentos que el paso 1 calcula y que la SFC sí publica certificados:

- Crédito Productivo (agregado)
- Crédito Productivo Urbano
- Crédito Productivo Popular Urbano

**Caveats:**

- El Excel es **manual** — cada mes hay que copiar el output del notebook y comparar a ojo. No hay trazabilidad de qué versión del cálculo produjo cada número, y se detectaron strings con formato custom corrupto en filas tardías al parsearlo programáticamente.
- Forma sólida a futuro: un notebook `notebooks/2_analisis/Validación_IBC.ipynb` que (a) ingiera las TIBC oficiales, (b) corra el cálculo del paso 1, (c) produzca esta tabla y stats automáticamente. Convierte una hoja frágil en métrica reproducible.

---

## 3. Carga de benchmarks macro de BanRep

**Notebook:** [`notebooks/0_ingesta/Ingesta_BanRep.ipynb`](notebooks/0_ingesta/Ingesta_BanRep.ipynb)
**Output:** `tasas_banrep_semanal.csv`

Descarga desde *suameca* tres series de referencia del mercado, agregadas a cierre de viernes (`W-FRI`, `.last()`) para alinear con el grano del análisis:

- **TES** — Cero Cupón Títulos de Tesorería, pesos, 1 año (serie 640001)
- **IBR** — Indicador Bancario de Referencia, overnight nominal
- **DTF** — Depósitos a Término Fijo, 90 días, semanal

No son la tasa que se valida; son **controles macro** que entran como regresores en el paso 8 para responder "¿la tendencia que vemos es Finagro o es BanRep?".

---

## 4. Peso de Finagro en el mercado por producto

**Notebooks:** [`notebooks/2_analisis/Peso_Finagro_en_SFC.ipynb`](notebooks/2_analisis/Peso_Finagro_en_SFC.ipynb), sección 3 de [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb)

Para entender qué tan fuerte podría ser el efecto Finagro sobre el IBC del mes siguiente, primero hay que medir cuánto pesa Finagro en cada producto. Como en la SFC no hay un flag explícito "esto es Finagro", se construye con **tres reglas** sobre las marcas disponibles, de la más conservadora a la más laxa:

| Regla | Definición | Participación nacional |
|---|---|---|
| `es_finagro_lb` (Lower Bound) | Rural **+** Redescuento | **22.2 %** del monto |
| `es_finagro_lb_plus` | Rural **+** Redescuento **+** FAG | 11.8 % |
| `es_finagro_ub` (Upper Bound) | Redescuento **+** FNG | 23.5 % |

Se reporta participación tanto en **monto desembolsado** como en **número de créditos**, agrupado por `year_month` y por `producto_de_credito_red`. Banagrario concentra el 32.8 % del canal Finagro-FAG.

El bound LB es el que se usa después como definición operativa de "Finagro" en el análisis del gap, por ser el más conservador.

---

## 5. Brecha de tasa Finagro vs no-Finagro

**Notebook:** [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) (secciones 4–7)

Para cada combinación `(fecha_corte, producto, is_finagro_lb)`, tasa ponderada por monto:

$$\bar{r} = \frac{\sum_i \text{tasa\\_efectiva\\_promedio}_i \cdot \text{montos\\_desembolsados}_i}{\sum_i \text{montos\\_desembolsados}_i}$$

Se pivota a `tasa_finagro` / `tasa_no_finagro` / `gap = no_finagro − finagro` por producto y se grafica la evolución (tres líneas por panel, eje Y independiente). El **Crédito Productivo Rural** es el único producto donde Finagro tiene mayoría (~64 % del monto) y el único donde el gap **se está cerrando**.

---

## 6. ¿De dónde viene el cambio? — descomposición shift-share

**Notebook:** [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) (sección 8)

Que la tasa no-Finagro rural esté cayendo puede venir de tres canales distintos. Distinguirlos importa porque cada uno tiene una lectura económica diferente. Shift-share entre la ventana inicial (primeras 12 semanas) y la final (últimas 12 semanas):

$$\Delta \bar{r} = \underbrace{\sum_e w_e^0 \cdot \Delta r_e}_{\text{within}} + \underbrace{\sum_e r_e^0 \cdot \Delta w_e}_{\text{between}} + \underbrace{\sum_e \Delta w_e \cdot \Delta r_e}_{\text{cross}} + \text{entrants} - \text{exits}$$

- **within** = cada entidad bajando su propia tasa
- **between** = reasignación de cuota hacia entidades más baratas
- **cross / entrants / exits** = términos residuales y de composición

Se reporta el ranking de entidades por contribución al efecto **within** y la evolución temporal de las top 8 por monto acumulado, para distinguir si el patrón es generalizado o concentrado en pocos bancos.

---

## 7. ¿Es Finagro o es macro? — regresión con controles

**Notebook:** [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) (sección 9)

Por producto, OLS con errores **Newey-West** (HAC, lags=4):

$$\text{tasa\\_total}_{t,p} = \alpha_p + \beta_{\text{time},p}\,t + \beta_{DTF,p}\,\text{DTF}_t + \beta_{IBR,p}\,\text{IBR}_t + \beta_{TES,p}\,\text{TES}_t + \beta_{F,p}\,\text{tasa\\_finagro}_{t,p} + \varepsilon_{t,p}$$

- $\beta_{\text{time}}$ — tendencia residual después de absorber macro y la tasa Finagro. Si el rural mantiene una pendiente negativa significativa, hay algo no-macro y no-Finagro moviendo el producto.
- $\beta_F$ — pass-through de la tasa Finagro a la tasa total. **Caveat**: como `tasa_total ≈ w·tasa_finagro + (1−w)·tasa_no_finagro`, $\beta_F$ mezcla composición y pass-through real — no es un coeficiente causal limpio.

**Robustez**:
- Modelo reducido `t + DTF + tasa_finagro` (descartando IBR/TES por colinealidad macro).
- **Mann-Kendall** no paramétrico sobre la serie cruda *y* sobre el residuo del modelo completo: si rural muestra `decreasing` significativo en ambos, la tendencia sobrevive a los controles.

---

## 8. ¿Cuánto explica el macro la tasa privada? — R² sin Finagro

**Notebook:** [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) (sección 10)

Para aislar la dinámica privada, sacamos a Finagro de la variable dependiente:

$$\text{tasa\\_no\\_finagro}_{t,p} = \alpha_p + \beta_{DTF,p}\,\text{DTF}_t + \beta_{IBR,p}\,\text{IBR}_t + \beta_{TES,p}\,\text{TES}_t + \varepsilon_{t,p}$$

La métrica clave es **R²**, no los betas individuales (la colinealidad DTF/IBR/TES rompe los betas individuales pero **no afecta la capacidad explicativa conjunta**).

- R² alto → tasas privadas siguen el ciclo BanRep, sin dinámica propia.
- R² bajo → algo no-macro está moviendo las tasas privadas (composición, Finagro indirecto, condiciones locales).

Sanity check visual: tasa no-Finagro real vs predicha por macro, contra IBR overnight, panel por producto.

---

## 9. Efecto Finagro sobre el IBC y el techo de usura — *el cierre*

**Notebook:** [`notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](notebooks/2_analisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) (sección 11)

Aquí cierra la historia. Por construcción del IBC publicado por la SFC:

$$\text{tasa\\_total} = w_F \cdot \text{tasa\\_finagro} + (1 - w_F) \cdot \text{tasa\\_no\\_finagro}$$

El **efecto Finagro sobre el IBC** es cuántos puntos porcentuales más bajo queda el IBC del producto por la presencia de Finagro:

$$\text{efecto}_F = \text{tasa\\_total} - \text{tasa\\_no\\_finagro} = -w_F \cdot \text{gap}$$

Y como el **techo de usura** se fija al mes siguiente como múltiplo del IBC observado (≈ 1.5× para Crédito de Consumo y Ordinario — para microcrédito las reglas SFC difieren), el efecto sobre el techo es:

$$\Delta\text{usura}_F \approx 1.5 \cdot \text{efecto}_F = -1.5 \cdot w_F \cdot \text{gap}$$

Este es el **número** del paper: cuánto más bajo queda el techo de usura por producto debido a la presencia de Finagro, y por consiguiente cuánto más caro (en pp) sería el crédito no-Finagro si Finagro no estuviera presente.

---

## Apartado: análisis exploratorios

No están en la línea causal del efecto IBC, pero soportan el contexto de negocio:

- [`notebooks/3_exploratorio/Descriptiva_Finagro.ipynb`](notebooks/3_exploratorio/Descriptiva_Finagro.ipynb) — descriptiva pura del lado Finagro: tendencias temporales, distribución por línea / tipo de productor / municipio, relación IBR-cartera.
- [`notebooks/3_exploratorio/Exploratorio_nuevos_créditos.ipynb`](notebooks/3_exploratorio/Exploratorio_nuevos_créditos.ipynb) — segmentación por tamaño (grande / mediano / microempresario), ruralidad vs no-ruralidad, tasas altas, nuevos destinatarios (Campesino, Comunidades Indígenas, …).

---

## Entregables narrativos

- **Artículo**: [`docs/entregables/Artículo_ Efecto de retroalimentación del IBC.docx`](docs/entregables/)
- **Presentaciones**: dos decks en [`docs/entregables/`](docs/entregables/)
