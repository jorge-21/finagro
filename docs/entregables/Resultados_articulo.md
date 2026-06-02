# Resultados — Efecto de retroalimentación del IBC

> **Documento de trabajo (scratchpad).** Estructura del artículo + slots para los resultados. Llenar los `[?]` y `[FALTA: ...]` tras correr los notebooks. Cuando una cifra ya está conocida o validada, queda anotada con su fuente.
>
> Convenciones:
> - `[?]` — número/dato puntual a llenar
> - `[FALTA: descripción]` — bloque más largo o decisión narrativa a completar
> - `→ fuente` — de dónde sale el dato (notebook + sección)

---

## La pregunta central

> **¿Cómo la tasa de Finagro — limitada por políticas sociales/subsidios — impacta el IBC del crédito productivo rural?**

Todo el artículo converge en responder esta pregunta. Cada sección que sigue es un eslabón.

---

## 1. Motivación y el mecanismo de retroalimentación

**Idea narrativa:** introducir al lector al IBC y al techo de usura, y plantar la sospecha de que un actor con tasas subsidiadas (Finagro) puede estar moviendo el ancla que define el costo legal máximo del crédito en Colombia.

### Hechos institucionales que el lector necesita saber

- La SFC publica mensualmente el **IBC** (Índice Bancario de Crédito) como promedio ponderado por monto de las tasas efectivas desembolsadas en el mes anterior, por segmento de producto.
- El **techo de usura** vigente en un mes se fija como múltiplo del IBC publicado el mes anterior (≈ **1.5 × IBC** para Crédito de Consumo y Ordinario; otras reglas para microcrédito — [`Análisis/metodología de cálculo de la tasa de interés.docx`](../Análisis/metodología%20de%20cálculo%20de%20la%20tasa%20de%20interés.docx)).
- **Finagro** coloca crédito al sector agropecuario a tasas subsidiadas vía redescuento + garantías (FAG). Estas operaciones se reportan a la SFC y por tanto **entran al cálculo del IBC** que la propia SFC publica.

### La sospecha

Si Finagro pesa suficiente en el monto desembolsado de un segmento, su tasa baja deprime el IBC del segmento, lo cual baja el techo de usura del mes siguiente, lo cual restringe lo que la banca privada puede cobrar — y por consiguiente puede afectar a quién y a qué precio se le presta. Eso es la **retroalimentación**.

### ¿Por qué importa? — implicaciones de política

[FALTA: 1–2 párrafos. Punto de partida: si el efecto es solo mecánico, Finagro "se mete" en el IBC pero no presiona el equilibrio de mercado. Si hay pass-through al sector privado, Finagro funciona como instrumento de política monetaria sectorial — con o sin esa intención. La política agropecuaria estaría haciendo política de crédito de facto.]

---

## 2. Hipótesis: el mecanismo dual

La pregunta tiene **dos canales** que conviene separar desde el principio porque se confunden fácil:

### Canal A — Composición (mecánico / aritmético)

Por construcción del IBC:

$$\text{IBC}_p = w_F^p \cdot \text{tasa}_{\text{finagro}}^p + (1 - w_F^p) \cdot \text{tasa}_{\text{no\_finagro}}^p$$

Como `tasa_finagro` < `tasa_no_finagro` y `w_F` > 0, el IBC queda más bajo que la tasa de mercado. **Esto no es comportamiento — es aritmética del promedio.**

### Canal B — Pass-through al mercado privado (comportamiento)

¿La existencia de Finagro hace que los bancos *privados* bajen su tasa? Dos sub-canales:

- **B1 — Competencia directa de precios:** Bancos ven la tasa Finagro y reaccionan inmediatamente (lag ≈ 0).
- **B2 — Vía techo de usura:** Finagro deprime IBC → techo de usura baja al mes siguiente → bancos privados se ajustan al nuevo techo (lag ≈ 1 mes).

**Tesis central del artículo:** [FALTA: el autor escoge la hipótesis. Tentativamente: *ambos canales existen, pero el canal B vía techo es el dominante para el crédito productivo rural, donde el peso de Finagro es mayor*. Confirmar tras ver §6.]

---

## 3. Datos y metodología

### 3.1 Fuentes

- **Microdatos Finagro** — un registro por crédito desembolsado, con tasa (`tasa_credito`), municipio, tipo de productor, garantía FAG, etc. Construido en [`Fuentes de Datos/Creación_DF.ipynb`](../Fuentes%20de%20Datos/Creación_DF.ipynb).
- **SFC vía Socrata API (`datos.gov.co`)** — desembolsos del sistema financiero con tasa efectiva promedio, monto, entidad, producto, tipo de garantía. Construido en [`Fuentes de Datos/Dataset___Retroalimentación.ipynb`](../Fuentes%20de%20Datos/Dataset___Retroalimentación.ipynb).
- **Tasas BanRep** (TES 1y, IBR overnight, DTF 90d) — controles macro a frecuencia semanal. [`Fuentes de Datos/BanRep_Tasas_Semanales.ipynb`](../Fuentes%20de%20Datos/BanRep_Tasas_Semanales.ipynb).

Cobertura temporal: [FALTA: rango temporal — primer y último viernes con observaciones]. Frecuencia de análisis: **semanal con cierre de viernes**.

### 3.2 Cálculo del IBC

Replicamos la metodología SFC/BanRep — promedio ponderado por monto desembolsado por segmento y semana:

$$\text{IBC}_{p,t} = \frac{\sum_i \text{tasa}_i \cdot \text{monto}_i}{\sum_i \text{monto}_i}$$

Se calcula para 5 segmentos de Crédito Productivo (agregado, Rural, Popular Rural, Urbano, Popular Urbano). → [`Análisis/Análisis___Retroalimentación.ipynb`](../Análisis/Análisis___Retroalimentación.ipynb).

### 3.3 Validación del IBC calculado

Contrastamos el IBC calculado contra el IBC oficial publicado por la SFC. Resultado:

| Segmento | Meses | Rango | Bias (mediana) | MAE | Error rel. medio |
|---|---|---|---|---|---|
| Crédito Productivo Rural | 22 | abr-2024 → ene-2026 | **+0.01 pp** | 0.26 pp | 1.4 % |
| Crédito Productivo Popular Rural | 24 | ene-2024 → dic-2025 | **+0.05 pp** | 0.41 pp | 0.9 % |

→ [`Análisis/Tasas IBC Crédito Productivo.xlsx`](../Análisis/Tasas%20IBC%20Crédito%20Productivo.xlsx).

**Mediana ≈ 0 en ambos segmentos → método sin sesgo sistemático.** MAE en orden de basis points sobre tasas de 17–50 % → buen ajuste para replicación con microdatos.

**Pendiente:** validar los otros 3 segmentos (Productivo agregado, Urbano, Popular Urbano) que la SFC sí publica. **Nota para el lector:** en el artículo declarar explícitamente que la validación cubre solo los segmentos rurales y se asume que la metodología transferirá a los urbanos.

---

## 4. Hechos estilizados — el campo de juego

### 4.1 Peso de Finagro por segmento

Como en la SFC no hay flag explícito "esto es Finagro", construimos **tres reglas operativas** sobre las marcas disponibles, de la más conservadora a la más laxa:

| Regla | Definición | Participación nacional (monto) |
|---|---|---|
| Finagro-LB (Lower Bound) | Rural ∧ Redescuento | **22.2 %** |
| Finagro-LB⁺ | Rural ∧ Redescuento ∧ FAG | 11.8 % |
| Finagro-UB (Upper Bound) | Redescuento ∧ FNG | 23.5 % |

→ [`Análisis/Análisis___Finagro_en_la_SFC.ipynb`](../Análisis/Análisis___Finagro_en_la_SFC.ipynb).

**Definición operativa adoptada:** Finagro-LB (más conservadora).

#### Peso de Finagro **por producto** (clave para identificación)

| Producto | w_F medio (% monto) | w_F medio (% número) |
|---|---|---|
| Crédito Productivo Rural | **~64 %** | [?] |
| Crédito Productivo Popular Rural | [?] | [?] |
| Crédito Productivo (agregado) | [?] | [?] |
| Crédito Productivo Urbano | [?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?] |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §3.

**Banagrario concentra el 32.8 %** del canal FAG-Finagro nacional. [?: ¿otra entidad relevante a mencionar?]

> **Por qué importa:** la heterogeneidad de `w_F` entre productos es el principal recurso de identificación. Si el canal B es real, debería verse más fuerte donde `w_F` es mayor (rural).

### 4.2 Brecha de tasa Finagro vs no-Finagro

Tasa ponderada por monto, por (semana × producto × es_finagro_LB). **Gap = tasa_no_finagro − tasa_finagro**.

| Producto | tasa_finagro media | tasa_no_finagro media | Gap promedio | Evolución del gap |
|---|---|---|---|---|
| Crédito Productivo Rural | [?] | [?] | [?] | **Cerrándose** (único producto donde ocurre) |
| Crédito Productivo Popular Rural | [?] | [?] | [?] | [?] |
| Crédito Productivo (agregado) | [?] | [?] | [?] | [?] |
| Crédito Productivo Urbano | [?] | [?] | [?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?] | [?] | [?] |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §4–7.

**Observación clave:** el crédito productivo rural es **el único producto donde**: (a) Finagro tiene mayoría (~64 % del monto), y (b) el gap se está cerrando. Eso lo convierte en el caso de estudio principal.

### 4.3 Evolución temporal — gráficos a incluir

- Gráfico 1: Tasa Finagro, tasa no-Finagro y gap por producto (5 paneles, eje Y independiente). → notebook Gap §6.
- Gráfico 2: Participación de Finagro en el monto desembolsado por producto, evolución semanal. → notebook Gap §3.

---

## 5. Canal A — el efecto mecánico sobre el IBC

### 5.1 La cantidad clave

Por la construcción del IBC:

$$\text{efecto}_F^p = \text{IBC}^p - \text{tasa}_{\text{no\_finagro}}^p = -w_F^p \cdot \text{gap}^p$$

Es **cuántos puntos porcentuales más bajo queda el IBC del segmento por la presencia de Finagro**. Magnitud crece con `w_F` y con `gap`.

### 5.2 Resultados por segmento

| Producto | efecto_F (pp) | IC 95% | Δ techo de usura (pp) |
|---|---|---|---|
| Crédito Productivo Rural | [?] | [?, ?] | [?] |
| Crédito Productivo Popular Rural | [?] | [?, ?] | [?] |
| Crédito Productivo (agregado) | [?] | [?, ?] | [?] |
| Crédito Productivo Urbano | [?] | [?, ?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?, ?] | [?] |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §11, tabla `resumen_ibc`.

### 5.3 El número del paper (lectura)

> En crédito productivo rural, **Finagro deprime el IBC en [?] pp** en promedio. El techo de usura del mes siguiente queda en [?] % en lugar de los [?] % que correspondería a la tasa privada — una diferencia de **[?] pp en lo que la banca legalmente puede cobrar** al segmento.

[FALTA: el autor afila el mensaje principal de esta sección — debe quedar como cita citable para resúmenes ejecutivos.]

### 5.4 Aclaración importante (caveats)

- Multiplicador 1.5 × aplica a Crédito de Consumo y Ordinario; **para microcrédito y otros productos las reglas SFC difieren** — referencia exacta en metodología SFC.
- El efecto mecánico **no implica causalidad sobre el equilibrio del mercado** — es aritmética. La pregunta de comportamiento se aborda en §6.

---

## 6. Canal B — ¿hay pass-through al mercado privado?

Si solo existiera el canal A, el IBC sería bajo pero la tasa privada estaría libre del efecto Finagro. La sospecha del artículo es que **el techo de usura, al bajar por la presencia de Finagro, disciplina lo que la banca privada cobra**. Para confirmar o refutar esto, miramos la dinámica de `tasa_no_finagro` directamente.

### 6.1 ¿De dónde viene la caída de la tasa privada rural? — Shift-share

Único producto donde Finagro tiene mayoría y el gap se cierra → la pregunta interesante es si la tasa **no-Finagro** rural está cayendo, y si sí, **por qué**:

$$\Delta \bar{r} = \underbrace{\sum_e w_e^0 \Delta r_e}_{\text{within}} + \underbrace{\sum_e r_e^0 \Delta w_e}_{\text{between}} + \text{cross + entrants − exits}$$

| Componente | Contribución (pp) | % del total |
|---|---|---|
| Within (cada banco baja su tasa) | [?] | [?] |
| Between (reasignación de cuota) | [?] | [?] |
| Cross | [?] | [?] |
| Entradas | [?] | [?] |
| Salidas | [?] | [?] |
| **Total** | [?] | 100 % |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §8.

**Lectura:** [FALTA: si within domina → los bancos individualmente están bajando tasa, consistente con disciplina del techo. Si between domina → es solo composición — bancos baratos ganan cuota. Cuál de los dos sale.]

**Entidades que más contribuyen al efecto within (top 3):** [?], [?], [?]. → notebook Gap §8 (subsección `Top entidades por contribución al efecto within`).

### 6.2 ¿Cuánto del movimiento de la tasa privada explica el ciclo macro?

Si BanRep mueve sus tasas, la tasa privada las sigue. La pregunta es: **después de controlar por macro, ¿queda residuo no explicado?**

Modelo macro-only: `tasa_no_finagro ~ DTF + IBR + TES` (sin tendencia).

| Producto | R² | n | Lectura |
|---|---|---|---|
| Crédito Productivo Rural | [?] | [?] | [?] |
| Crédito Productivo Popular Rural | [?] | [?] | [?] |
| Crédito Productivo (agregado) | [?] | [?] | [?] |
| Crédito Productivo Urbano | [?] | [?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?] | [?] |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §10.

**Tendencia residual anualizada** (sobre el residuo del modelo macro):

| Producto | β_t (pp/año) | IC 95% | Significancia |
|---|---|---|---|
| Crédito Productivo Rural | [?] | [?, ?] | [?] |
| Otros | [?] | [?, ?] | [?] |

> **Lectura clave:** si el rural tiene **R² bajo** (macro no explica todo) y **β_t residual significativamente negativo**, hay algo no-macro empujando la tasa privada rural hacia abajo. Ese "algo" es candidato a ser Finagro vía el canal B.

### 6.3 Pass-through directo (sec. 12, recién agregada)

Modelo:

$$\text{tasa\_no\_finagro}_{t,p} = \alpha_p + \gamma_0^p\,\text{tasa\_finagro}_{t,p} + \gamma_4^p\,\text{tasa\_finagro}_{t-4,p} + \beta_t^p\,t + \beta_{\text{macro}}^p X_t + \varepsilon$$

| Producto | γ₀ (contemp.) | p₀ | γ₄ (lag 4 sem) | p₄ | γ_total = γ₀ + γ₄ |
|---|---|---|---|---|---|
| Crédito Productivo Rural | [?] | [?] | [?] | [?] | [?] |
| Crédito Productivo Popular Rural | [?] | [?] | [?] | [?] | [?] |
| Crédito Productivo (agregado) | [?] | [?] | [?] | [?] | [?] |
| Crédito Productivo Urbano | [?] | [?] | [?] | [?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?] | [?] | [?] | [?] |

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §12.

**Interpretación de los lags:**
- **γ₀** = canal de competencia directa (precio Finagro visible → bancos reaccionan inmediatamente)
- **γ₄** = canal vía techo de usura (~ 1 mes para que el IBC publicado y el nuevo techo se trasladen al pricing privado)

**Robustez con lag 8 (≈ 2 meses):** [FALTA: si γ₈ todavía aporta → transmisión más lenta. Llenar tras correr celda 62 del notebook.]

### 6.4 Cross-product: identificación implícita

**Si el canal B es real, γ_total debe crecer con w_F** entre productos. Si γ_total es plano respecto a w_F, la asociación es ruido.

| Producto | w_F medio | γ_total |
|---|---|---|
| Crédito Productivo Rural | ~0.64 | [?] |
| Crédito Productivo Popular Rural | [?] | [?] |
| Crédito Productivo (agregado) | [?] | [?] |
| Crédito Productivo Urbano | [?] | [?] |
| Crédito Productivo Popular Urbano | [?] | [?] |

Pendiente de la regresión cross-product **γ_total = α + β · w_F**: β = [?], p = [?].

→ [`Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb`](../Análisis/Gap_Tasas_Finagro_vs_NoFinagro.ipynb) §12, scatter final.

**Lectura:**
- β > 0 significativo → evidencia consistente con canal causal de competencia/techo.
- β ≈ 0 → la presencia de Finagro no escala su efecto sobre la tasa privada con su peso. Difícil sostener narrativa causal.
- β < 0 → pasaría algo raro — la asociación va contra la hipótesis. Investigar.

### 6.5 Robustez

- **Modelo reducido** (sin IBR/TES por colinealidad macro): los signos y orden entre productos coinciden con el modelo completo. → notebook Gap §9 (robustez).
- **Mann-Kendall (no paramétrico)** sobre tasa total cruda y sobre residuo del modelo completo:

| Producto | Trend (serie cruda) | p | Trend (residuo) | p |
|---|---|---|---|---|
| Crédito Productivo Rural | [?] | [?] | [?] | [?] |
| Otros | [?] | [?] | [?] | [?] |

→ notebook Gap §9 (Mann-Kendall).

---

## 7. Discusión

### 7.1 Veredicto sobre la pregunta central

> **¿Cómo la tasa de Finagro impacta el IBC del crédito productivo rural?**

**Respuesta corta:** [FALTA: una oración con el veredicto integrado. Plantilla:]
> *El efecto es de [magnitud] pp en el IBC vía el canal mecánico (composición), y [adicional] pp vía pass-through al mercado privado (vía techo de usura / vía competencia directa / ninguno significativo). El techo de usura del crédito productivo rural queda [X] pp por debajo de lo que sería sin la presencia de Finagro.*

### 7.2 Implicaciones de política

[FALTA: 1–2 párrafos. Puntos sugeridos:]
- Si la retroalimentación es real, Finagro funciona como instrumento de política monetaria sectorial vía techo de usura — *sin ser ese su mandato declarado*.
- Trade-off: el mismo mecanismo que abarata el crédito agropecuario podría estar reduciendo la oferta privada en segmentos donde el techo se aprieta (los bancos privados podrían salir de productos con baja rentabilidad post-techo).
- Pregunta abierta: ¿hay evidencia de retiro de oferta privada en segmentos con `w_F` alto? Sería un siguiente estudio.

### 7.3 Limitaciones

- **Validación parcial del IBC calculado** (2 de 5 segmentos validados; los 3 urbanos asumidos por extensión metodológica).
- **No hay shock exógeno explícito**. La identificación descansa en (a) controles macro, (b) variación cross-product de `w_F`, (c) lags. No es identificación causal estricta tipo natural experiment.
- **Definición operativa de "Finagro" (LB)** es conservadora. Si la regla correcta es UB, los pesos w_F suben y el efecto mecánico también — pero el pass-through también podría verse distinto. Robustez con UB: [FALTA: ¿se corrió? Si no, anotar como pendiente.]
- **Período de análisis**: [?] – [?]. Eventos macro relevantes en el período: [FALTA: ej. ciclo de bajada de tasas BanRep desde 2024, cambios en regulación FAG, etc.]

---

## 8. Conclusión

[FALTA: 2–3 párrafos cerrando la historia. Sugerencia de estructura:]

1. **Recap del hallazgo** — recapitular en una frase canal A + canal B con sus magnitudes.
2. **Por qué importa** — para regulador, para banca privada, para el agro.
3. **Qué sigue** — una o dos preguntas abiertas que el estudio no responde pero que abre.

---

## Apéndice — material exploratorio que no entra al cuerpo del artículo

- **Segmentación por tamaño del productor** (grande / mediano / micro), ruralidad vs no-ruralidad, nuevos beneficiarios. → [`Análisis/Exploratorio_nuevos_créditos.ipynb`](../Análisis/Exploratorio_nuevos_créditos.ipynb).
- **Descriptiva pura del lado Finagro** (líneas, cadenas, eslabones). → [`Análisis/Análisis___Finagro_Data.ipynb`](../Análisis/Análisis___Finagro_Data.ipynb).

---

## Checklist de números a llenar (orden de prioridad)

- [ ] §4.1 — w_F medio por producto (4 productos faltantes)
- [ ] §4.2 — tabla de gaps por producto
- [ ] §5.2 — tabla `efecto_F` por producto + Δ techo
- [ ] §5.3 — frase canónica del "número del paper"
- [ ] §6.1 — descomposición shift-share rural
- [ ] §6.2 — R² del macro + β_t residual por producto
- [ ] §6.3 — γ₀ y γ₄ por producto + robustez lag 8 (sec 12 recién agregada)
- [ ] §6.4 — pendiente β de γ_total vs w_F
- [ ] §6.5 — Mann-Kendall por producto
- [ ] §7.1 — veredicto sintetizado
- [ ] §7.2 — implicaciones de política
- [ ] §8 — conclusión
