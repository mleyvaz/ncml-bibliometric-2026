"""Re-run key bibliometric tables using disambiguated authors.

Writes to reports/clean/.
"""
from __future__ import annotations
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REP = ROOT / "reports" / "clean"
REP.mkdir(exist_ok=True, parents=True)

authors = pd.read_csv(ROOT / "data" / "authors_canon.csv")
works = pd.read_csv(ROOT / "data" / "works.csv")
print(f"Authorships: {len(authors)}   Works: {len(works)}")

# --- Productivity ---
prod = (authors.groupby(["cluster_id", "name_canonical"], dropna=False)["doi"]
        .nunique().rename("articles").reset_index()
        .sort_values("articles", ascending=False))
prod.to_csv(REP / "author_productivity_clean.csv", index=False)

# Lotka
lotka = prod.groupby("articles").size().rename("n_authors").reset_index().sort_values("articles")
lotka.to_csv(REP / "lotka_clean.csv", index=False)

# --- Co-authorship (using cluster_id now) ---
pair_counter = Counter()
for doi, grp in authors.groupby("doi"):
    clusters = sorted(set(grp["cluster_id"].dropna().astype(int).tolist()))
    for a, b in combinations(clusters, 2):
        pair_counter[(a, b)] += 1

# Map back to names for readability
name_map = dict(zip(prod["cluster_id"], prod["name_canonical"]))
pairs = pd.DataFrame(
    [(name_map.get(a, str(a)), name_map.get(b, str(b)), c) for (a, b), c in pair_counter.most_common(300)],
    columns=["author_a", "author_b", "coauth_count"],
)
pairs.to_csv(REP / "coauth_top_clean.csv", index=False)

# --- Temporal: productivity per author over time ---
per_year = (authors.groupby(["cluster_id", "year"])["doi"].nunique().rename("n").reset_index())
pivot = per_year.pivot(index="cluster_id", columns="year", values="n").fillna(0).astype(int)
pivot["total"] = pivot.sum(axis=1)
pivot = pivot.reset_index().merge(prod[["cluster_id", "name_canonical"]], on="cluster_id")
# Keep only authors with >=5 articles for readability
pivot_top = pivot[pivot["total"] >= 5].sort_values("total", ascending=False)
pivot_top.to_csv(REP / "author_timeline.csv", index=False)

# --- Country aggregation (OpenAlex-sourced; many authors don't have countries) ---
country_counts = Counter()
for s in authors["countries"].fillna(""):
    for c in str(s).split("|"):
        c = c.strip()
        if c:
            country_counts[c] += 1
cntdf = pd.DataFrame(country_counts.most_common(), columns=["country", "authorships"])
cntdf.to_csv(REP / "countries_clean.csv", index=False)

# --- Author nodes for Gephi/VOSviewer ---
nodes = prod.rename(columns={"cluster_id": "id", "name_canonical": "label", "articles": "weight"})
nodes[["id", "label", "weight"]].to_csv(REP / "network_nodes.csv", index=False)

# Edges
edges = pd.DataFrame(
    [(a, b, c) for (a, b), c in pair_counter.items()],
    columns=["source", "target", "weight"],
)
edges.to_csv(REP / "network_edges.csv", index=False)

print(f"""
Summary:
  Unique authors (clusters): {len(prod)}
  Authors with >=1 article: {(prod['articles']>=1).sum()}
  >=5 articles:             {(prod['articles']>=5).sum()}
  >=10 articles:            {(prod['articles']>=10).sum()}
  Top Lotka slots:
""")
for _, r in lotka.head(10).iterrows():
    print(f"    {int(r['articles']):>3} articles -> {int(r['n_authors'])} authors")
print(f"""
  Co-author pairs: {len(pair_counter):,}
  Network files: {REP / 'network_nodes.csv'} + network_edges.csv  (ready for Gephi/VOSviewer)
""")
