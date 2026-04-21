"""Export all analytical tables into a single Excel workbook with multiple sheets.

Hojas:
  README         — descripcion del contenido y metadatos del estudio
  KPIs           — indicadores consolidados
  Articulos      — works.csv (762)
  Autores        — author_clusters.csv (1363 desambiguados)
  Autorias       — authorships desambiguadas (2225)
  Topicos        — 24 topicos con tamano y terminos
  Topicos_docs   — asignacion documento-topico + UMAP coords
  Topicos_ano    — matriz topico x ano (share %)
  Topicos_crec   — emergentes vs declinantes
  Bradford       — 2339 fuentes citadas ranked
  Lotka          — distribucion n(x)
  Comunidades    — Louvain summary
  Paises         — distribucion geografica
  Instituciones  — top 15 + completa
  Scholar_muestra — sample Scholar vs OpenAlex (n=26)
  Crecimiento    — articulos y autores por ano
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
DATA = ROOT / "data"
REP = ROOT / "reports" / "clean"
OUT = ROOT / "NCML_bibliometric_dataset.xlsx"


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# README
readme = pd.DataFrame({
    "Campo": [
        "Titulo", "Fecha de corte", "Autores", "Fuente primaria",
        "Fuentes secundarias", "Total articulos", "Volumenes cubiertos",
        "Autores unicos", "Referencias parseadas", "Topicos identificados",
        "Pipeline", "Licencia datos",
    ],
    "Valor": [
        "NCML Bibliometric Dataset 2018-2026",
        "2026-04-19",
        "Leyva Vazquez, M.; Smarandache, F.; [tercer autor externo pendiente]",
        "https://fs.unm.edu/NCML/Articles.htm",
        "OpenAlex; DataCite; Google Scholar Metrics; Google Scholar (muestra)",
        762, 42, 1363, 11877, 24,
        "Python 3.14 (PyMuPDF, BeautifulSoup, sentence-transformers, UMAP, KMeans, networkx, python-louvain)",
        "CC-BY 4.0 (datos); MIT (codigo)",
    ],
})

sheets = {"README": readme}

# KPIs
if (REP / "kpis.json").exists():
    kpis = load_json(REP / "kpis.json")
    sheets["KPIs"] = pd.DataFrame(kpis.items(), columns=["Indicador", "Valor"])

# Articulos
works = pd.read_csv(DATA / "works.csv")
sheets["Articulos"] = works

# Autores
clusters = pd.read_csv(DATA / "author_clusters.csv")
sheets["Autores"] = clusters

# Autorias (desambiguadas)
authors = pd.read_csv(DATA / "authors_canon.csv")
# Quita columnas utilitarias que son redundantes
keep_cols = ["doi", "volume", "year", "source", "position", "name", "name_canonical",
             "orcid", "institutions", "countries", "cluster_id"]
authors_clean = authors[[c for c in keep_cols if c in authors.columns]]
sheets["Autorias"] = authors_clean

# Topicos
sheets["Topicos"] = pd.read_csv(DATA / "topics_labels.csv")

# Topicos docs
docs_topics = pd.read_csv(DATA / "topics_docs.csv")
sheets["Topicos_docs"] = docs_topics

# Topicos x ano
if (REP / "topics_over_time_norm.csv").exists():
    sheets["Topicos_ano"] = pd.read_csv(REP / "topics_over_time_norm.csv")

# Crecimiento / declive de topicos
if (REP / "topics_growth.csv").exists():
    sheets["Topicos_crec"] = pd.read_csv(REP / "topics_growth.csv")

# Bradford
if (REP / "bradford_sources.csv").exists():
    sheets["Bradford"] = pd.read_csv(REP / "bradford_sources.csv")

# Lotka
if (REP / "lotka_fit.json").exists():
    lotka_fit = load_json(REP / "lotka_fit.json")
    sheets["Lotka_fit"] = pd.DataFrame(lotka_fit.items(), columns=["Parametro", "Valor"])
# Lotka distribution
lotka_dist = clusters.groupby("articles").size().rename("n_autores").reset_index()
sheets["Lotka_dist"] = lotka_dist

# Comunidades
if (REP / "coauth_communities.csv").exists():
    sheets["Comunidades"] = pd.read_csv(REP / "coauth_communities.csv")

# Paises e instituciones
if (REP / "countries_full.csv").exists():
    sheets["Paises"] = pd.read_csv(REP / "countries_full.csv")

# Top instituciones: parse from authorships
from collections import Counter
inst_counter = Counter()
for s in authors["institutions"].fillna("").astype(str):
    for i in s.split("|"):
        i = i.strip()
        if i and i.lower() != "nan":
            inst_counter[i] += 1
inst_df = pd.DataFrame(inst_counter.most_common(), columns=["institucion", "autorias"])
sheets["Instituciones"] = inst_df

# Scholar sample
if (DATA / "scholar_sample_clean.csv").exists():
    sheets["Scholar_muestra"] = pd.read_csv(DATA / "scholar_sample_clean.csv")

# Crecimiento
growth = pd.DataFrame({"year": range(2018, 2027)})
growth["articulos"] = growth["year"].map(works.groupby("year").size()).fillna(0).astype(int)
growth["articulos_acumulado"] = growth["articulos"].cumsum()

# First-year per author
authors_valid = authors[authors["cluster_id"].notna() & (authors["cluster_id"] != "")].copy()
authors_valid["cluster_id"] = authors_valid["cluster_id"].astype(int)
first_year = authors_valid.groupby("cluster_id")["year"].min()
new_per_year = first_year.value_counts().sort_index()
growth["autores_nuevos"] = growth["year"].map(new_per_year).fillna(0).astype(int)
growth["autores_acumulado"] = growth["autores_nuevos"].cumsum()
sheets["Crecimiento"] = growth

# Red — stats + top pairs (as reference)
if (REP / "network_stats.json").exists():
    stats = load_json(REP / "network_stats.json")
    sheets["Red_stats"] = pd.DataFrame(stats.items(), columns=["Metrica", "Valor"])
if (REP / "coauth_top_clean.csv").exists():
    sheets["Red_top_pares"] = pd.read_csv(REP / "coauth_top_clean.csv")

# --------- Write to Excel ---------
print(f"Writing {OUT} with {len(sheets)} sheets...")

with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    for name, df in sheets.items():
        # Excel sheet name: max 31 chars, no forbidden chars
        safe = name[:31]
        # Trim extremely long text columns to avoid Excel cell limit issues
        df2 = df.copy()
        for col in df2.select_dtypes("object").columns:
            df2[col] = df2[col].astype(str).str.slice(0, 30000)
        df2.to_excel(writer, sheet_name=safe, index=False)

# Stats
total_rows = sum(len(df) for df in sheets.values())
print(f"Total rows across sheets: {total_rows:,}")
for name, df in sheets.items():
    print(f"  {name:<20} {len(df):>6,} rows")
print(f"\nFile: {OUT}")
print(f"Size: {OUT.stat().st_size / 1e6:.1f} MB")
