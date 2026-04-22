"""Neutrosophic aggregation experiment: rank NCML authors using SVNWA
(Ye 2014) across four neutrosophic dimensions and compare with the
classical count-based ranking.

Dimensions (each author receives a (T, I, F) triple per dimension):

  D1. Productivity — based on total articles.
      T = sigmoid(articles / 10), I = peak at mid-range, F = 1 - T - I
  D2. Citational evidence — mean per-article source-agreement class.
      T = share of articles cited in both OpenAlex and Scholar (verified)
      I = share of articles cited in only one source (disagreement)
      F = share of articles with no citation evidence
      NOTE: we only have Scholar counts for the 26 sampled articles;
      for other authors we use the OpenAlex-only approximation with
      higher I.
  D3. Coauthorship centrality — mean T_collab of the author's edges
      (already computed in neutrosophic_coauth_edges.csv).
      T = mean T_collab, I = mean I_collab, F = mean F_collab
  D4. Theoretical focus — share of the author's articles assigned to
      theory-heavy topics (T7, T16, T2).
      T = share of theory articles, F = share of purely applied articles
      (legal/medical case topics), I = share of border/other topics.

Aggregation: SVNWA with four equal weights (0.25 each).
Score: Smarandache S(T,I,F) = (2 + T - I - F) / 3  [in [0, 1]]

Outputs:
  paper2_neutrosophic/data/neutrosophic_author_ranking.csv
  paper2_neutrosophic/figures/ranking_comparison.png
  paper2_neutrosophic/data/ranking_divergence_stats.json
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kendalltau, spearmanr

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
P2 = ROOT / "paper2_neutrosophic"
DATA_OUT = P2 / "data"
FIG_OUT = P2 / "figures"

# --- Load data ---
authors = pd.read_csv(ROOT / "data" / "authors_canon.csv")
clusters = pd.read_csv(ROOT / "data" / "author_clusters.csv")
sample = pd.read_csv(ROOT / "data" / "scholar_sample_clean.csv")
docs_topics = pd.read_csv(ROOT / "data" / "topics_docs.csv")
edges_n = pd.read_csv(P2 / "data" / "neutrosophic_coauth_edges.csv")

# Only authors with >= 3 articles (manageable ranking universe)
top = clusters[clusters["articles"] >= 3].copy().reset_index(drop=True)
print(f"Authors in ranking universe (>=3 articles): {len(top)}")

# Lookup: doi -> topic
doi_topic = dict(zip(docs_topics["doi"].astype(str), docs_topics["topic"]))

# Theory-heavy topics from the paper-1 analysis
THEORY_TOPICS = {7, 16, 2}           # theoretical / methods
LEGAL_MED_TOPICS = {0, 9, 17, 22, 12, 20, 23, 11, 13, 3, 10, 1}  # applied

# Lookup: doi -> OpenAlex cite count (fallback for non-sampled)
works = pd.read_csv(ROOT / "data" / "works.csv")
works["oa_cites"] = pd.to_numeric(works["oa_cited_by"], errors="coerce").fillna(0).astype(int)
doi_oa = dict(zip(works["doi"].astype(str), works["oa_cites"]))

# Scholar sample lookup
sample["oa_cites"] = pd.to_numeric(sample["oa_cited_by"], errors="coerce").fillna(0).astype(int)
sample["scholar"] = pd.to_numeric(sample["scholar_cites"], errors="coerce").fillna(0).astype(int)
sample_dois = set(sample["doi"].astype(str))
doi_scholar = dict(zip(sample["doi"].astype(str), sample["scholar"]))


def sigmoid(x, k=0.5, x0=5):
    return 1 / (1 + np.exp(-k * (x - x0)))


def bell(x, mu=5, s=3):
    return np.exp(-((x - mu) ** 2) / (2 * s * s))


# For each author compute per-dimension N-triple
rows = []
for _, a in top.iterrows():
    cid = int(a["cluster_id"])
    name = a["name_canonical"]
    n_articles = int(a["articles"])

    # Author's DOIs
    author_pubs = authors[authors["cluster_id"] == cid]
    author_dois = author_pubs["doi"].astype(str).unique().tolist()

    # D1 Productivity
    T1 = sigmoid(n_articles, k=0.35, x0=8)
    I1 = bell(n_articles, mu=5, s=4) * 0.5
    F1 = max(0, 1 - T1 - I1)

    # D2 Citational evidence
    T_cnt = I_cnt = F_cnt = 0
    total = 0
    for d in author_dois:
        total += 1
        oa = doi_oa.get(d, 0)
        if d in sample_dois:
            sch = doi_scholar.get(d, 0)
            if oa >= 1 and sch >= 1:
                T_cnt += 1
            elif oa == 0 and sch == 0:
                F_cnt += 1
            else:
                I_cnt += 1
        else:
            # Unsampled: use OpenAlex with high I penalty
            if oa >= 1:
                T_cnt += 0.6
                I_cnt += 0.4
            else:
                # Undersampled negative evidence
                I_cnt += 0.5
                F_cnt += 0.5
    if total > 0:
        T2 = T_cnt / total
        I2 = I_cnt / total
        F2 = F_cnt / total
    else:
        T2, I2, F2 = 0.0, 1.0, 0.0

    # D3 Coauthorship centrality: mean T_collab over edges touching this author
    my_edges = edges_n[(edges_n["source"] == cid) | (edges_n["target"] == cid)]
    if len(my_edges) > 0:
        T3 = float(my_edges["T_collab"].mean())
        I3 = float(my_edges["I_collab"].mean())
        F3 = float(my_edges["F_collab"].mean())
    else:
        T3, I3, F3 = 0.0, 0.0, 1.0  # isolated author

    # D4 Theoretical focus
    t_count = f_count = i_count = 0
    for d in author_dois:
        t = doi_topic.get(d)
        if t is None:
            i_count += 1
            continue
        t = int(t)
        if t in THEORY_TOPICS:
            t_count += 1
        elif t in LEGAL_MED_TOPICS:
            f_count += 1
        else:
            i_count += 1
    ttl = t_count + f_count + i_count
    if ttl > 0:
        T4, I4, F4 = t_count / ttl, i_count / ttl, f_count / ttl
    else:
        T4, I4, F4 = 0.0, 1.0, 0.0

    rows.append({
        "cluster_id": cid, "name": name, "articles": n_articles,
        "T_prod": round(T1, 3), "I_prod": round(I1, 3), "F_prod": round(F1, 3),
        "T_cite": round(T2, 3), "I_cite": round(I2, 3), "F_cite": round(F2, 3),
        "T_coauth": round(T3, 3), "I_coauth": round(I3, 3), "F_coauth": round(F3, 3),
        "T_theory": round(T4, 3), "I_theory": round(I4, 3), "F_theory": round(F4, 3),
    })

df = pd.DataFrame(rows)
print(f"Computed N-triples for {len(df)} authors")
print(df.head(3).to_string())
print()

# --- Aggregation: SVNWA (Ye 2014) ---
# SVNWA((T_j, I_j, F_j); w_j) = (1 - prod(1 - T_j)^w_j, prod(I_j)^w_j, prod(F_j)^w_j)
weights = np.array([0.25, 0.25, 0.25, 0.25])  # equal

T_cols = [["T_prod", "I_prod", "F_prod"],
          ["T_cite", "I_cite", "F_cite"],
          ["T_coauth", "I_coauth", "F_coauth"],
          ["T_theory", "I_theory", "F_theory"]]


def svnwa(row):
    T_products = 1.0
    I_products = 1.0
    F_products = 1.0
    for (tc, ic, fc), w in zip(T_cols, weights):
        T_products *= (1 - max(min(row[tc], 1), 1e-9)) ** w
        I_products *= max(min(row[ic], 1), 1e-9) ** w
        F_products *= max(min(row[fc], 1), 1e-9) ** w
    T_agg = 1 - T_products
    I_agg = I_products
    F_agg = F_products
    return pd.Series({"T_agg": T_agg, "I_agg": I_agg, "F_agg": F_agg})


agg = df.apply(svnwa, axis=1)
df = pd.concat([df, agg], axis=1)

# Score function (Smarandache)
df["score"] = (2 + df["T_agg"] - df["I_agg"] - df["F_agg"]) / 3

# Classical ranking (count only)
df["rank_classical"] = df["articles"].rank(ascending=False, method="min").astype(int)
df["rank_neutro"] = df["score"].rank(ascending=False, method="min").astype(int)
df["rank_change"] = df["rank_classical"] - df["rank_neutro"]

# Sort by neutrosophic rank
df_sorted = df.sort_values("rank_neutro").reset_index(drop=True)
df_sorted.to_csv(DATA_OUT / "neutrosophic_author_ranking.csv", index=False, encoding="utf-8")

# --- Divergence stats ---
tau, tau_p = kendalltau(df["rank_classical"], df["rank_neutro"])
rho, rho_p = spearmanr(df["rank_classical"], df["rank_neutro"])

# Top-10 overlap
top10_classical = set(df.nsmallest(10, "rank_classical")["cluster_id"])
top10_neutro = set(df.nsmallest(10, "rank_neutro")["cluster_id"])
overlap_10 = len(top10_classical & top10_neutro)
jaccard_10 = overlap_10 / len(top10_classical | top10_neutro)

# Largest rank changes
df["abs_change"] = df["rank_change"].abs()
biggest_rises = df.nlargest(5, "rank_change")[["name", "articles", "rank_classical", "rank_neutro", "score"]]
biggest_falls = df.nsmallest(5, "rank_change")[["name", "articles", "rank_classical", "rank_neutro", "score"]]

print(f"Kendall tau: {tau:.3f} (p={tau_p:.4f})")
print(f"Spearman rho: {rho:.3f} (p={rho_p:.4f})")
print(f"Top-10 overlap: {overlap_10}/10 (Jaccard {jaccard_10:.2f})")
print()
print("Biggest RISES in neutrosophic ranking:")
print(biggest_rises.to_string(index=False))
print()
print("Biggest FALLS in neutrosophic ranking:")
print(biggest_falls.to_string(index=False))

stats = {
    "kendall_tau": round(float(tau), 3),
    "kendall_p": round(float(tau_p), 4),
    "spearman_rho": round(float(rho), 3),
    "spearman_p": round(float(rho_p), 4),
    "top10_overlap": int(overlap_10),
    "top10_jaccard": round(float(jaccard_10), 3),
    "n_authors": int(len(df)),
    "weights_D1_D2_D3_D4": weights.tolist(),
}
(DATA_OUT / "ranking_divergence_stats.json").write_text(json.dumps(stats, indent=2))

# --- Visualization ---
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Left: rank change scatter
ax = axes[0]
ax.scatter(df["rank_classical"], df["rank_neutro"], alpha=0.6, s=40, color="#2874a6")
max_r = max(df["rank_classical"].max(), df["rank_neutro"].max())
ax.plot([1, max_r], [1, max_r], "--", color="gray", lw=0.8, label="No change")
# Highlight top-5 biggest moves
for _, r in pd.concat([biggest_rises.head(3), biggest_falls.head(3)]).iterrows():
    ax.annotate(r["name"][:20], (r["rank_classical"], r["rank_neutro"]),
                fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_xlabel("Classical rank (by article count)")
ax.set_ylabel("Neutrosophic SVNWA rank")
ax.set_title(f"Rank divergence: classical vs neutrosophic\n"
             f"Kendall τ = {tau:.2f}, top-10 overlap = {overlap_10}/10")
ax.invert_xaxis()
ax.invert_yaxis()
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

# Right: top-15 side by side
ax = axes[1]
top_classical = df.nsmallest(15, "rank_classical")[["name", "articles"]].copy()
top_classical["kind"] = "Classical"
top_neutro = df.nsmallest(15, "rank_neutro")[["name", "articles", "score"]].copy()
top_neutro["kind"] = "Neutrosophic"
# Show bars: x=rank (1=top), bar length = score normalized
y = np.arange(15)
nam_c = [n[:28] for n in top_classical["name"].values[::-1]]
nam_n = [n[:28] for n in top_neutro["name"].values[::-1]]

ax.barh(y - 0.2, top_classical["articles"].values[::-1] / top_classical["articles"].max(),
        height=0.4, color="#7f8c8d", alpha=0.85, label="Classical (articles)")
ax.barh(y + 0.2, top_neutro["score"].values[::-1],
        height=0.4, color="#27ae60", alpha=0.85, label="Neutrosophic (score)")
ax.set_yticks(y)
ax.set_yticklabels([f"C: {c}\nN: {n}" for c, n in zip(nam_c, nam_n)], fontsize=7)
ax.set_xlabel("Normalized rank value")
ax.set_title("Top 15 by each ranking (side by side)")
ax.legend(fontsize=9, loc="lower right")
ax.grid(axis="x", alpha=0.3)

plt.suptitle("Neutrosophic SVNWA Aggregate Ranking of NCML Authors — Comparison with Classical Count",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(FIG_OUT / "ranking_comparison.png", dpi=160, bbox_inches="tight")
plt.close()
print(f"\nFigure: {FIG_OUT / 'ranking_comparison.png'}")
