"""Author disambiguation for NCML dataset.

Rules (in order):
  1. Same ORCID -> same cluster (highest confidence).
  2. Same OpenAlex author_id -> same cluster.
  3. Same canonical normalized name (strip accents, collapse spaces,
     lowercase) -> same cluster.
  4. Given name initial + full surnames match (e.g., "M. Leyva Vazquez"
     ~= "Maikel Leyva Vazquez") -> MERGE candidate.

Outputs:
  data/authors_canon.csv   — per authorship row + cluster_id + canonical name
  data/author_clusters.csv — one row per cluster with aggregated counts
  reports/authors_review_top.csv — top 100 clusters for manual review
"""
from __future__ import annotations
import sys
import re
import unicodedata
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
AUTHORS = ROOT / "data" / "authors.csv"
OUT_ROWS = ROOT / "data" / "authors_canon.csv"
OUT_CLUSTERS = ROOT / "data" / "author_clusters.csv"
REPORT = ROOT / "reports" / "authors_review_top.csv"


def strip_accents(s: str) -> str:
    if not isinstance(s, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


PARTICLES = {"de", "del", "la", "las", "los", "y", "e", "da", "do", "dos", "das", "van", "von"}


def canon_name(name: str) -> str:
    """Canonical form: lowercase, no accents, particles removed, sorted tokens of length > 1."""
    if not isinstance(name, str):
        return ""
    s = strip_accents(name).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    tokens = [t for t in s.split() if len(t) > 1 and t not in PARTICLES]
    # Sort tokens so that "Leyva Maikel" == "Maikel Leyva"
    return " ".join(sorted(tokens))


def surname_initials_key(name: str) -> str:
    """Initial + surnames key for lighter matching."""
    if not isinstance(name, str):
        return ""
    s = strip_accents(name).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    tokens = [t for t in s.split() if len(t) > 1 and t not in PARTICLES]
    if len(tokens) < 2:
        return ""
    # "Maikel Leyva Vazquez" -> "m_leyva_vazquez" (initial of first token + other tokens sorted)
    initial = tokens[0][0]
    rest = sorted(tokens[1:])
    return initial + "|" + " ".join(rest)


df = pd.read_csv(AUTHORS)
print(f"Input rows: {len(df)}")

# 1. build cluster keys
df["canon"] = df["name"].fillna("").astype(str).map(canon_name)
df["init_key"] = df["name"].fillna("").astype(str).map(surname_initials_key)
df["orcid_clean"] = df["orcid"].fillna("").astype(str).str.strip()
df["oa_id_clean"] = df["oa_author_id"].fillna("").astype(str).str.strip()

# Union-find implementation
parent = {}

def find(x):
    while parent.get(x, x) != x:
        parent[x] = parent.get(parent[x], parent[x])
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

# Seed each row with its own cluster
for i in df.index:
    parent[i] = i

# Build inverted indexes
orcid_to_rows = {}
oaid_to_rows = {}
canon_to_rows = {}
init_to_rows = {}
for i, r in df.iterrows():
    if r["orcid_clean"]:
        orcid_to_rows.setdefault(r["orcid_clean"], []).append(i)
    if r["oa_id_clean"]:
        oaid_to_rows.setdefault(r["oa_id_clean"], []).append(i)
    if r["canon"]:
        canon_to_rows.setdefault(r["canon"], []).append(i)
    if r["init_key"]:
        init_to_rows.setdefault(r["init_key"], []).append(i)

# 1) Union by ORCID (strongest)
for rows in orcid_to_rows.values():
    for j in rows[1:]:
        union(rows[0], j)

# 2) Union by OpenAlex author id
for rows in oaid_to_rows.values():
    for j in rows[1:]:
        union(rows[0], j)

# 3) Union by canonical name (same as other rows in same canon group)
for rows in canon_to_rows.values():
    for j in rows[1:]:
        union(rows[0], j)

# 4) Union by initial+surnames key, but ONLY when no ORCID conflict
for rows in init_to_rows.values():
    if len(rows) < 2:
        continue
    # Check that all involved rows have either the same ORCID or empty
    orcids = set(df.loc[rows, "orcid_clean"]) - {""}
    if len(orcids) <= 1:
        for j in rows[1:]:
            union(rows[0], j)

# Assign cluster ids
df["cluster_root"] = df.index.map(find)
# Remap to sequential cluster_id
uniq = {r: i for i, r in enumerate(sorted(df["cluster_root"].unique()))}
df["cluster_id"] = df["cluster_root"].map(uniq)

# Pick canonical display name per cluster: most frequent original name
display_map = df.groupby("cluster_id")["name"].agg(
    lambda s: s.fillna("").value_counts().idxmax() if s.fillna("").ne("").any() else ""
)
df["name_canonical"] = df["cluster_id"].map(display_map)

df.to_csv(OUT_ROWS, index=False, encoding="utf-8")

# Cluster-level aggregation
clusters = (
    df.groupby("cluster_id")
    .agg(
        name_canonical=("name_canonical", "first"),
        articles=("doi", "nunique"),
        orcid=("orcid_clean", lambda s: "|".join(sorted(set(x for x in s if x)))),
        institutions=("institutions", lambda s: "|".join(sorted(set(i for row in s.fillna("") for i in str(row).split("|") if i))) ),
        countries=("countries", lambda s: "|".join(sorted(set(c for row in s.fillna("") for c in str(row).split("|") if c))) ),
        name_variants=("name", lambda s: " ;; ".join(sorted(set(x for x in s.fillna("") if x)))),
        first_year=("year", "min"),
        last_year=("year", "max"),
    )
    .reset_index()
    .sort_values("articles", ascending=False)
)
clusters.to_csv(OUT_CLUSTERS, index=False, encoding="utf-8")

# Review file: top 100 clusters with all variants for manual verification
review = clusters.head(100)[["cluster_id", "name_canonical", "articles", "orcid", "name_variants", "countries", "institutions"]]
review.to_csv(REPORT, index=False, encoding="utf-8")

print(f"Input: {len(df)} authorship rows, {df['name'].nunique()} unique raw names")
print(f"Clusters: {len(clusters)}")
print(f"Merged: {df['name'].nunique() - len(clusters)} raw name variants collapsed")
print(f"\nTop 20 clusters:")
for _, r in clusters.head(20).iterrows():
    v = r["name_variants"].split(" ;; ")
    print(f"  {int(r['articles']):>3}  {r['name_canonical']:<40}  variants={len(v)}  ORCID={'Y' if r['orcid'] else '-'}")
print(f"\nReview file for manual audit: {REPORT}")
