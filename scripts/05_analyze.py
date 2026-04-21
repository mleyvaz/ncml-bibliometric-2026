"""Bibliometric analysis on the enriched NCML dataset.

Writes a text report to reports/summary.md plus several CSVs in reports/.
"""
from __future__ import annotations
import sys
import re
import unicodedata
from collections import Counter
from itertools import combinations
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

works = pd.read_csv(ROOT / "data" / "works.csv")
authors = pd.read_csv(ROOT / "data" / "authors.csv")
concepts = pd.read_csv(ROOT / "data" / "concepts.csv")

# Normalize author names for aggregation (strip accents, lower, collapse)
def canon(name: str) -> str:
    if not isinstance(name, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in nfkd if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s).strip().lower()
    # Remove obvious replacement chars left from page encoding issues
    s = s.replace("\ufffd", "")
    return s

authors["name_canon"] = authors["name"].fillna("").astype(str).map(canon)
authors = authors[authors["name_canon"] != ""].copy()

lines = []
w = lines.append

w("# NCML Bibliometric Report")
w("")
w(f"- Articles total: **{len(works)}**")
w(f"- Volumes: **{works['volume'].nunique()}** covering years **{int(works['year'].min())}–{int(works['year'].max())}**")
w(f"- Articles with OpenAlex record: **{(works['oa_id'] != '').sum()}** ({(works['oa_id']!='').mean():.0%})")
w(f"- Articles with DataCite record: **{works['dc_pubyear'].notna().sum()}**")
w("")

# --- Per-year and per-volume ---
w("## Articles per year / volume")
yearly = works.groupby("year").size().rename("articles")
w("```\n" + yearly.to_string() + "\n```")
w("")
vol_tbl = works.groupby(["year", "volume"]).size().rename("articles").reset_index()
vol_tbl.to_csv(REPORTS / "by_volume.csv", index=False)
w(f"Per-volume table: `reports/by_volume.csv`")
w("")

# --- Citations (OpenAlex) ---
cited = pd.to_numeric(works["oa_cited_by"], errors="coerce").fillna(0).astype(int)
w("## Citations (OpenAlex)")
w(f"- Total citations: **{cited.sum()}**")
w(f"- Articles with ≥1 citation: **{(cited >= 1).sum()}** ({(cited >= 1).mean():.1%})")
w(f"- Mean / median cites per article: **{cited.mean():.2f}** / **{cited.median():.0f}**")
w(f"- Max citations: **{cited.max()}**")
# h-index of the journal
cited_sorted = sorted(cited, reverse=True)
h = 0
for i, c in enumerate(cited_sorted, 1):
    if c >= i:
        h = i
    else:
        break
w(f"- Journal h-index (OpenAlex-visible): **{h}**")
w("")
top_cited = (
    works.assign(cites=cited)
    .sort_values("cites", ascending=False)
    .loc[:, ["cites", "year", "volume", "title_local", "authors_local", "doi"]]
    .head(15)
)
top_cited.to_csv(REPORTS / "top_cited.csv", index=False)
w("Top 10 cited (local):")
w("```")
for _, r in top_cited.head(10).iterrows():
    w(f"  {r['cites']:>3} cites | Vol.{r['volume']} ({r['year']}) | {str(r['title_local'])[:90]}")
w("```")
w("")

# --- Views / downloads (Zenodo via DataCite) ---
views = pd.to_numeric(works["dc_views"], errors="coerce").fillna(0).astype(int)
dls = pd.to_numeric(works["dc_downloads"], errors="coerce").fillna(0).astype(int)
w("## Zenodo usage (DataCite)")
w(f"- Total views: **{views.sum():,}**   Total downloads: **{dls.sum():,}**")
w(f"- Mean views per article: **{views.mean():.0f}**   Mean downloads: **{dls.mean():.0f}**")
top_dl = (
    works.assign(views=views, dls=dls)
    .sort_values("dls", ascending=False)
    .loc[:, ["dls", "views", "volume", "year", "title_local", "doi"]]
    .head(15)
)
top_dl.to_csv(REPORTS / "top_downloads.csv", index=False)
w("Top downloaded:")
w("```")
for _, r in top_dl.head(10).iterrows():
    w(f"  {r['dls']:>5} dl | {r['views']:>5} v | Vol.{r['volume']} | {str(r['title_local'])[:80]}")
w("```")
w("")

# --- Author productivity (Lotka) ---
w("## Author productivity")
per_author = authors.groupby("name_canon").size().rename("articles").reset_index()
# Prefer a display name: pick most common original casing per canon
disp = (authors.groupby("name_canon")["name"]
        .agg(lambda s: s.value_counts().idxmax()))
per_author["name_display"] = per_author["name_canon"].map(disp)
per_author = per_author.sort_values("articles", ascending=False)
per_author.to_csv(REPORTS / "authors_productivity.csv", index=False)
w(f"- Unique authors: **{len(per_author):,}**")
w(f"- Authors with ≥5 articles: **{(per_author['articles'] >= 5).sum()}**")
w(f"- Authors with ≥10 articles: **{(per_author['articles'] >= 10).sum()}**")
w("")
w("Top 20 most prolific:")
w("```")
for _, r in per_author.head(20).iterrows():
    w(f"  {int(r['articles']):>3}  {r['name_display']}")
w("```")
w("")

# Lotka distribution
lotka = per_author.groupby("articles").size().rename("n_authors").reset_index()
lotka.to_csv(REPORTS / "lotka.csv", index=False)
w("Lotka-style distribution (n_authors per #articles):")
w("```")
for _, r in lotka.sort_values("articles").head(15).iterrows():
    w(f"  {int(r['articles']):>3} articles -> {int(r['n_authors'])} authors")
w("```")
w("")

# --- Co-authorship network (degree only; full graph skipped) ---
w("## Co-authorship (top pairs)")
pair_counter = Counter()
for doi, grp in authors.groupby("doi"):
    names = sorted(set(n for n in grp["name_canon"] if n))
    for a, b in combinations(names, 2):
        pair_counter[(a, b)] += 1
pairs_df = pd.DataFrame(
    [(a, b, c) for (a, b), c in pair_counter.most_common(300)],
    columns=["author_a", "author_b", "coauth_count"],
)
pairs_df.to_csv(REPORTS / "coauth_top.csv", index=False)
w(f"- Unique author pairs: **{len(pair_counter):,}**")
w("Top 10 co-authoring pairs:")
w("```")
for _, r in pairs_df.head(10).iterrows():
    w(f"  {r['coauth_count']:>3}x  {r['author_a']}  ---  {r['author_b']}")
w("```")
w("")

# --- Country / institution distribution (OpenAlex) ---
w("## Countries and institutions (OpenAlex subset)")
country_rows = []
for s in authors["countries"].fillna(""):
    for c in str(s).split("|"):
        c = c.strip()
        if c:
            country_rows.append(c)
country_df = pd.DataFrame(Counter(country_rows).most_common(), columns=["country", "authorships"])
country_df.to_csv(REPORTS / "countries.csv", index=False)
w("```")
for _, r in country_df.head(15).iterrows():
    w(f"  {r['country']:<4} {r['authorships']:>5}")
w("```")
w("")

inst_rows = []
for s in authors["institutions"].fillna(""):
    for inst in str(s).split("|"):
        inst = inst.strip()
        if inst:
            inst_rows.append(inst)
inst_df = pd.DataFrame(Counter(inst_rows).most_common(50), columns=["institution", "authorships"])
inst_df.to_csv(REPORTS / "institutions.csv", index=False)
w("Top 15 institutions:")
w("```")
for _, r in inst_df.head(15).iterrows():
    w(f"  {r['authorships']:>4}  {str(r['institution'])[:80]}")
w("```")
w("")

# --- OpenAlex concepts (topical map) ---
w("## OpenAlex concepts (L0-L2, top per level)")
concepts_f = concepts[concepts["level"].isin([0, 1, 2])]
for lvl in [0, 1, 2]:
    top = (concepts_f[concepts_f["level"] == lvl]
           .groupby("concept").size().rename("n").reset_index()
           .sort_values("n", ascending=False).head(10))
    w(f"Level {lvl}:")
    w("```")
    for _, r in top.iterrows():
        w(f"  {int(r['n']):>4}  {r['concept']}")
    w("```")
top_concepts_all = (concepts.groupby("concept").size().rename("n").reset_index()
                    .sort_values("n", ascending=False).head(80))
top_concepts_all.to_csv(REPORTS / "concepts_top.csv", index=False)
w("")

# --- Title keywords (simple n-gram on local titles) ---
w("## Title keyword frequency (local)")
import string
stop = set("""de la el los las en y para con una un del a al por que su sus como entre mas analisis caso estudio
evaluar evaluacion metodo metodos multicriterio neutrosofico neutrosofica neutrosoficas neutrosoficos mapa cognitivo
study case method approach neutrosophic analysis assessment model based""".split())
titles = works["title_local"].fillna("").astype(str).tolist()
toks = []
for t in titles:
    t2 = re.sub(r"[^\w\sñáéíóúÁÉÍÓÚÑ]", " ", canon(t))
    for tok in t2.split():
        if len(tok) > 3 and tok not in stop:
            toks.append(tok)
tok_df = pd.DataFrame(Counter(toks).most_common(50), columns=["token", "count"])
tok_df.to_csv(REPORTS / "title_tokens_top.csv", index=False)
w("Top 20 content words (ignoring neutrosofico/multicriterio/mapa/etc.):")
w("```")
for _, r in tok_df.head(20).iterrows():
    w(f"  {int(r['count']):>4}  {r['token']}")
w("```")
w("")

# --- Write the report ---
(REPORTS / "summary.md").write_text("\n".join(lines), encoding="utf-8")
print("Wrote reports/summary.md + csv breakdowns")
