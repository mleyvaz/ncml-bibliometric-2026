# Dataset guide

## NCML_bibliometric_dataset.xlsx (19 sheets)

| Sheet | Rows | Description |
|---|---|---|
| README | 12 | Metadata of the study |
| KPIs | 20 | Consolidated indicators |
| Articulos | 762 | Articles with DOI, volume, year, pages, URLs |
| Autores | 1,363 | Unique authors (post-disambiguation) |
| Autorias | 2,225 | Authorship rows with affiliations and ORCID |
| Topicos | 24 | Topics with size and top terms |
| Topicos_docs | 725 | Doc-to-topic assignment + UMAP 2D coordinates |
| Topicos_ano | 24 | Topic x year share matrix |
| Topicos_crec | 24 | Emerging vs declining topics |
| Bradford | 2,339 | Journals cited, ranked by frequency |
| Lotka_fit | 10 | Fit parameters + K-S diagnostics |
| Lotka_dist | 17 | Distribution n(x) vs number of authors |
| Comunidades | 81 | Louvain communities |
| Paises | 14 | Country distribution |
| Instituciones | 45 | Top institutions |
| Scholar_muestra | 26 | Scholar vs OpenAlex sample |
| Crecimiento | 9 | Articles and authors per year |
| Red_stats | 11 | Network metrics |
| Red_top_pares | 300 | Top 300 co-authoring pairs |

Each sheet is also available as a CSV in `data/` for programmatic access.
