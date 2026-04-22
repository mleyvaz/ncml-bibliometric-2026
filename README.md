# NCML Bibliometric Retrospective 2018-2026

Codigo y datos del estudio bibliometrico de la revista *Neutrosophic Computing
and Machine Learning* (NCML) durante el periodo 2018-2026. Acompana al paper:

> Leyva Vazquez, M.; Gonzalez Vargas, Y.; Smarandache, F. (2026).
> **Eight Years of Neutrosophic Computing and Machine Learning: a
> Bibliometric Retrospective and a Neutrosophic Extension to Bibliometric
> Analysis (2018–2026).** [manuscript under review].
>
> Manuscript: `paper_combined/NCML_Leyva_et_al_2026_Combined.docx`

## Que hay aqui

Un pipeline reproducible de **30 scripts Python** que:

1. Scrapea los 762 articulos del sitio oficial de NCML.
2. Descarga los PDF (728/762 = 95.5% exito por problemas de encoding en origen).
3. Extrae texto, autores, abstracts, palabras clave y referencias.
4. Enriquece con OpenAlex y DataCite.
5. Desambigua autores por union-find (4 reglas jerarquicas).
6. Ajusta las leyes de Lotka y Bradford.
7. Construye la red de coautoria (Louvain).
8. Modela topicos con embeddings multilingues + UMAP + KMeans.
9. Triangula impacto citacional entre OpenAlex, Scholar Metrics y un muestreo
   Scholar estratificado.
10. **Computa extensiones neutrosoficas (T, I, F) para 5 indicadores:**
    N-h-index, N-Lotka, N-Bradford, N-topic membership, N-coauthorship.
11. **Agrega autores via SVNWA (Ye 2014)** y compara con el ranking clasico.
12. Genera 13 figuras PNG y un Excel de 19 hojas con el dataset completo.

## Hallazgos resumidos

| Indicador | Valor |
|---|---|
| Articulos totales | 762 (42 volumenes, 2018-2026 parcial) |
| Autores unicos (desambiguados) | 1.363 |
| CAGR articulos 2018-2025 | 42% |
| Lotka α | 2.03 (SE 0.03, clasica) |
| Bradford: nucleo | 5 revistas concentran 33% citas |
| Modularidad red coautoria | 0.96 (81 comunidades disjuntas) |
| Google Scholar h5-index | 10 |
| OpenAlex h-index | 1 (cobertura parcial; factor 10x de discrepancia) |
| Iberoamerica share autorias | 94.9% |
| Topicos identificados | 24 |
| Cambio identidad: T14 Educacion | -21.6 puntos porcentuales 2018-20 vs 2023-25 |

## Estructura del repositorio

```
.
├── README.md
├── LICENSE-CODE            MIT (codigo)
├── LICENSE-DATA            CC-BY 4.0 (datos y figuras)
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── scripts/                Los 30 scripts numerados (01-30)
├── data/                   Datos intermedios (CSVs, JSONL)
├── paper/                  Primera version (ES, retrospectiva clasica)
│                           └─ NCML_Leyva_et_al_2026-Final-Rev2.docx
│                           └─ cover_letter_NCML.docx
├── paper2_neutrosophic/    Segunda version (EN, framework neutrosofico)
│                           └─ Leyva_et_al_2026_Neutrosophic_Bibliometric_Framework.docx
│                           └─ data/ (9 CSVs y JSONs con indicadores N-T/I/F)
│                           └─ figures/ (ranking_comparison.png, neutrosophic_indicators.png)
├── paper_combined/         **VERSION FINAL** (EN, retrospectiva + framework)
│                           └─ NCML_Leyva_et_al_2026_Combined.docx
│                           └─ email_to_smarandache.docx (propuesta al coautor)
├── figures/                13 PNGs de alta resolucion
└── docs/                   Documentacion (INSTALL, REPRODUCE, DATASET)
```

**NO incluido en el repo** (por tamano):
- Los 728 PDFs originales (~438 MB): disponibles bajo peticion o via el script 07.
- Los textos completos extraidos (.txt, ~50 MB): regenerables con el script 08.

## Reproduccion rapida

```bash
# 1. Clonar
git clone https://github.com/mleyvaz/ncml-bibliometric-2026.git
cd ncml-bibliometric-2026

# 2. Ambiente (Python 3.11-3.14)
python -m venv venv
source venv/bin/activate   # Linux/Mac
# o
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# 3. Correr el pipeline en orden. Los scripts son idempotentes
#    y producen cada uno un CSV o imagen.
python scripts/01_scrape.py                # raw.html + articles_raw.csv
python scripts/02b_normalize_dois.py       # articles_clean.csv
python scripts/03_fetch_apis.py            # openalex + datacite (requiere internet)
python scripts/04_build_tables.py          # works.csv, authors.csv, concepts.csv
python scripts/07_download_pdfs.py         # 728 PDFs (~438 MB, 5 min con 10 hilos)
python scripts/08_extract_text.py          # pdf_extract.csv + fulltext .txt
python scripts/09_disambiguate_authors.py  # authors_canon.csv, author_clusters.csv
python scripts/10_analyze_clean.py         # bibliometrix core tables
python scripts/11_lotka.py                 # Lotka fit + figura
python scripts/12_bradford.py              # Bradford zones + figura
python scripts/13_topic_model.py           # 24 topicos (requiere 600MB RAM)
python scripts/14_topics_over_time.py      # evolucion temporal
python scripts/15_coauth_network.py        # red de coautoria + 3 figuras
python scripts/16_growth_fig.py            # figura de crecimiento
python scripts/17b_geo_fig.py              # distribucion geografica
python scripts/18_kpi_dashboard.py         # dashboard final (8 paneles)
python scripts/19_export_excel.py          # Excel con 19 hojas consolidado

# 4. (Opcional) regenerar el backup y el .docx final
python scripts/20_backup.py
python scripts/21_generate_docx.py
```

Tiempo total estimado: **~30 minutos** en una laptop moderna con conexion decente.
El paso mas lento es el modelado de topicos (scripts/13, ~3 min GPU o ~10 min CPU
para 725 embeddings de 384 dimensiones).

## Datos disponibles

El directorio `data/` contiene los CSVs regenerables:

- `articles_clean.csv` — 762 articulos con DOI, volumen, año, URL PDF.
- `works.csv` — articulos enriquecidos con OpenAlex + DataCite (cobertura 88%).
- `authors_canon.csv` — 2.225 autorias con `cluster_id` de desambiguacion.
- `author_clusters.csv` — 1.363 autores unicos con nombre canonico.
- `topics_labels.csv` — 24 topicos con terminos top c-TF-IDF.
- `topics_docs.csv` — asignacion documento-topico + coordenadas UMAP 2D.
- `NCML_bibliometric_dataset.xlsx` — **dataset consolidado en 19 hojas** listo
  para analisis externo en Excel, R o Python.

Para los PDFs originales: ejecutar `scripts/07_download_pdfs.py` (descarga
desde `fs.unm.edu/NCML/`). Los hashes SHA-256 publicados en el paper permiten
verificacion de integridad.

## Figuras

Las 11 figuras del paper estan en `figures/`:

1. `growth.png` — Crecimiento anual 2018-2026 + autores acumulados
2. `geo.png` — Distribucion geografica e institucional
3. `lotka_loglog.png` — Ley de Lotka (log-log + CDF comparacion)
4. `bradford.png` — Ley de Bradford (curva acumulada + top 20 revistas)
5. `topics_umap.png` — Mapa UMAP 2D de 24 topicos
6. `topics_heatmap.png` — Topico x Año (share %)
7. `topics_trend.png` — Crecimiento vs declive de topicos
8. `coauth_main.png` — Red: componente conexo principal
9. `coauth_core.png` — Red: nucleo productivo (>=4 articulos)
10. `coauth_full.png` — Red completa filtrada (>=2 articulos)
11. `dashboard.png` — Dashboard KPI (8 paneles)

## Licencias

- **Codigo** (scripts/, requirements.txt): MIT, ver `LICENSE-CODE`.
- **Datos y figuras** (data/, figures/): CC-BY 4.0, ver `LICENSE-DATA`.
- **PDFs originales**: derechos de sus autores y de NSS/NCML; no redistribuidos
  en el repositorio. Recuperables desde `fs.unm.edu/NCML/`.

## Citacion

Si usas este repositorio o el dataset, por favor cita:

```bibtex
@article{leyva2026ncml,
  author  = {Leyva Vazquez, Maikel and Gonzalez Vargas, Yismandry and
             Smarandache, Florentin},
  title   = {Neutrosophic Computing and Machine Learning (2018-2026): una
             retrospectiva bibliometrica editorial},
  year    = {2026},
  journal = {[en revision]},
  url     = {https://github.com/mleyvaz/ncml-bibliometric-2026}
}
```

## Contacto

**Corresponding author:** Maikel Leyva Vazquez <mleyvaz@gmail.com>

Para reportar errores, extender el analisis, o solicitar dataset completo:
- Abrir un issue en este repositorio.
- Contactar a mleyvaz@gmail.com.

## Declaracion de conflicto de interes

Leyva Vazquez y Smarandache son Editors-in-Chief de NCML y NSS respectivamente.
El analisis empirico, el codigo y los datos intermedios fueron preparados de
forma independiente. El tercer autor, Gonzalez Vargas (ALCN), aporto
validacion independiente del pipeline. Los autores declararon el conflicto al
editor asignado durante el proceso de revision por pares.

## Agradecimientos

A la comunidad NSIA Publishing y a la Asociacion Latinoamericana de Ciencias
Neutrosoficas por facilitar el acceso al corpus historico de NCML. A los
desarrolladores de OpenAlex, DataCite, BERTopic, UMAP, NetworkX y Python-Louvain
por sus herramientas de codigo abierto que hicieron posible este estudio.
