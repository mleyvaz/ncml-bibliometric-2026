"""Compute neutrosophic extensions of classical bibliometric indicators
on the NCML 2018-2026 dataset.

Implements:
  1. Neutrosophic h-index (T, I, F) triangulating OpenAlex / Scholar / DataCite
  2. Neutrosophic Lotka exponent (alpha as SVN with bootstrap-based I, F)
  3. Neutrosophic Bradford zone membership (graded zone assignment)
  4. Neutrosophic topic membership from KMeans soft assignment
  5. Neutrosophic co-authorship edge weights (T = repeated, I = single,
     F = absent given conventional thresholds)

Outputs to paper2_neutrosophic/data/ and figures/.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
P2 = ROOT / "paper2_neutrosophic"
DATA_OUT = P2 / "data"
FIG_OUT = P2 / "figures"
DATA_OUT.mkdir(exist_ok=True)
FIG_OUT.mkdir(exist_ok=True)

works = pd.read_csv(ROOT / "data" / "works.csv")
clusters = pd.read_csv(ROOT / "data" / "author_clusters.csv")
sample = pd.read_csv(ROOT / "data" / "scholar_sample_clean.csv")
bradford = pd.read_csv(ROOT / "reports" / "clean" / "bradford_sources.csv")
docs_topics = pd.read_csv(ROOT / "data" / "topics_docs.csv")

# ====================================================================
# 1. Neutrosophic h-index — triangulating sources
# ====================================================================
# OpenAlex: full coverage but undercount (h=1)
# Scholar Metrics journal-level: h5=10 (5-year window, journal aggregate)
# Scholar sample: per-article counts on n=26 stratified sample
#
# Strategy: for each article in the sample, compare cite count between
# OpenAlex and Scholar; classify into:
#   T (truth)        = cited in both (clear positive evidence)
#   F (falsity)      = cited in neither (clear negative evidence)
#   I (indeterminacy)= cited in one but not the other (disagreement)
#
# Then aggregate to estimate the neutrosophic h-index of NCML, which is
# defined as the triple (h_T, h_I, h_F) where:
#   h_T = h-index considering only articles with T=1
#   h_I = additional articles whose status is indeterminate
#   h_F = articles with no citation evidence

sample["oa_cites"] = pd.to_numeric(sample["oa_cited_by"], errors="coerce").fillna(0).astype(int)
sample["scholar"] = pd.to_numeric(sample["scholar_cites"], errors="coerce").fillna(0).astype(int)


def classify(oa, sch):
    if oa >= 1 and sch >= 1:
        return "T"
    if oa == 0 and sch == 0:
        return "F"
    return "I"


sample["status"] = sample.apply(lambda r: classify(r["oa_cites"], r["scholar"]), axis=1)
status_counts = sample["status"].value_counts()
n = len(sample)
nT = int(status_counts.get("T", 0))
nI = int(status_counts.get("I", 0))
nF = int(status_counts.get("F", 0))
print(f"Sample n={n}: T={nT}, I={nI}, F={nF}")

# h-indices on sample using max(oa, scholar) for "best evidence"
sample["best"] = sample[["oa_cites", "scholar"]].max(axis=1)
def h_index(cs):
    cs = sorted(cs, reverse=True)
    h = 0
    for i, c in enumerate(cs, 1):
        if c >= i: h = i
        else: break
    return h

# h_T: only T-class articles
hT = h_index(sample.loc[sample["status"] == "T", "best"])
# h_T+I: T plus I (give credit for partial evidence)
hTI = h_index(sample.loc[sample["status"].isin(("T", "I")), "best"])
# h_T (alpha) computed if we counted only OpenAlex (most conservative)
h_oa = h_index(sample["oa_cites"])
# h_T scholar only
h_sch = h_index(sample["scholar"])

# Membership values: degree to which the journal "is" h-indexed at level 10
# We anchor on Scholar Metrics h5=10 as the union of evidences.
SCHOLAR_H5 = 10
DATACITE_OBSERVED_H = 0  # DataCite citation_count is empty for all NCML

T_h = nT / n
I_h = nI / n
F_h = nF / n
print(f"Sample Neutrosophic h-index decomposition:  T={T_h:.2f}  I={I_h:.2f}  F={F_h:.2f}")

# Triangulated h estimate
h_neut = {
    "h_T_sample": int(hT),
    "h_TI_sample": int(hTI),
    "h_OpenAlex_sample": int(h_oa),
    "h_Scholar_sample": int(h_sch),
    "h_Scholar_journal_h5": SCHOLAR_H5,
    "T_membership": round(T_h, 3),
    "I_membership": round(I_h, 3),
    "F_membership": round(F_h, 3),
    "interpretation": {
        "T": "Articles with >=1 citation in BOTH OpenAlex and Scholar (verified positive)",
        "I": "Articles with citation in only ONE source (evidential disagreement)",
        "F": "Articles with no citation in any source",
    },
    "neutrosophic_h_index_aggregate": {
        "lower_bound": int(min(hT, h_oa)),
        "upper_bound": int(SCHOLAR_H5),
        "consensus": int(hTI),
    },
}
(DATA_OUT / "neutrosophic_h_index.json").write_text(json.dumps(h_neut, indent=2))
print(f"  -> Aggregate N-h-index: ({h_neut['T_membership']}, {h_neut['I_membership']}, {h_neut['F_membership']})")
print(f"  -> Bounds: [{h_neut['neutrosophic_h_index_aggregate']['lower_bound']}, {h_neut['neutrosophic_h_index_aggregate']['upper_bound']}]")
print()

# ====================================================================
# 2. Neutrosophic Lotka exponent (bootstrap)
# ====================================================================
# Classical alpha = 2.03; KS fails. We bootstrap to get distribution
# and define:
#   T = degree of consistency with classical Lotka (alpha in [1.9, 2.1] AND KS passes)
#   I = degree where alpha is in range but KS fails
#   F = alpha outside [1.9, 2.1]

from scipy.special import zeta

x = clusters["articles"].astype(int).to_numpy()
x = x[x >= 1]
N = len(x)


def fit_alpha(xs):
    return 1 + len(xs) / np.sum(np.log(xs / 0.5))


def ks_stat(xs, alpha):
    vals, counts = np.unique(xs, return_counts=True)
    pmf_emp = counts / counts.sum()
    cdf_emp = np.cumsum(pmf_emp)
    xgrid = np.arange(1, xs.max() + 1)
    pmf_th = xgrid.astype(float) ** (-alpha) / zeta(alpha, 1)
    cdf_th = np.cumsum(pmf_th)
    cdf_th_at = cdf_th[vals - 1]
    return float(np.max(np.abs(cdf_emp - cdf_th_at)))


B = 1000
rng = np.random.default_rng(42)
boot_alphas = []
boot_ks = []
for _ in range(B):
    sample_b = rng.choice(x, size=N, replace=True)
    a = fit_alpha(sample_b)
    boot_alphas.append(a)
    boot_ks.append(ks_stat(sample_b, a))
boot_alphas = np.array(boot_alphas)
boot_ks = np.array(boot_ks)
ks_crit = 1.36 / np.sqrt(N)

mean_alpha = float(boot_alphas.mean())
ci95 = [float(np.percentile(boot_alphas, 2.5)), float(np.percentile(boot_alphas, 97.5))]

# Neutrosophic membership of "Lotka classical"
T_lot = float(np.mean((boot_alphas >= 1.9) & (boot_alphas <= 2.1) & (boot_ks <= ks_crit)))
I_lot = float(np.mean((boot_alphas >= 1.9) & (boot_alphas <= 2.1) & (boot_ks > ks_crit)))
F_lot = float(np.mean((boot_alphas < 1.9) | (boot_alphas > 2.1)))

lotka_neut = {
    "alpha_mean_bootstrap": round(mean_alpha, 3),
    "alpha_95CI": [round(c, 3) for c in ci95],
    "ks_critical_5pct": round(ks_crit, 4),
    "T_classical_Lotka": round(T_lot, 3),
    "I_alpha_in_range_KS_fails": round(I_lot, 3),
    "F_alpha_outside_range": round(F_lot, 3),
    "B": B,
    "interpretation": (
        "T captures the degree to which NCML's productivity distribution is "
        "fully consistent with classical Lotka (alpha in [1.9, 2.1] AND K-S "
        "passes). I captures partial consistency (exponent matches but the "
        "distribution shape diverges). F captures clear non-Lotka behaviour."
    ),
}
(DATA_OUT / "neutrosophic_lotka.json").write_text(json.dumps(lotka_neut, indent=2))
print(f"Lotka N-membership:  T={T_lot:.2f}  I={I_lot:.2f}  F={F_lot:.2f}  (alpha={mean_alpha:.3f}, 95% CI {ci95})")
print()

# ====================================================================
# 3. Neutrosophic Bradford zone membership
# ====================================================================
# A journal cited X times has degrees of membership in (zone1, zone2, zone3).
# Classical: hard partition by cumulative citations.
# Neutrosophic: each journal has (T, I, F) for "is in nucleus".
#
# Define for each journal its cite-share s = X / total. Map to:
#   T(nucleus) = 1 / (1 + exp(-(s - s_threshold) / k))
#   F(nucleus) = 1 - T(nucleus) - I
#   I(nucleus) = saturation in transition zones

cum = bradford["cites"].cumsum().to_numpy()
total = cum[-1]
share = bradford["cites"].to_numpy() / total

# Threshold: where cumulative reaches 1/3 (nucleus boundary)
nucleus_idx = np.searchsorted(cum, total / 3) + 1
s_threshold = share[nucleus_idx - 1] if nucleus_idx <= len(share) else share[0]

# Logistic membership for "belongs to nucleus"
k = max(s_threshold * 0.4, 1e-3)
T_nuc = 1 / (1 + np.exp(-(share - s_threshold) / k))
# Indeterminacy peak around the boundary (Gaussian-like)
I_nuc = np.exp(-((share - s_threshold) ** 2) / (2 * (k * 1.5) ** 2)) * 0.4
F_nuc = np.maximum(0, 1 - T_nuc - I_nuc)

bradford_n = bradford.copy()
bradford_n["T_nucleus"] = T_nuc.round(3)
bradford_n["I_nucleus"] = I_nuc.round(3)
bradford_n["F_nucleus"] = F_nuc.round(3)
bradford_n.head(30).to_csv(DATA_OUT / "neutrosophic_bradford_top30.csv", index=False, encoding="utf-8")

print("Top 5 Bradford journals with neutrosophic nucleus membership:")
for _, r in bradford_n.head(5).iterrows():
    print(f"  {r['source'][:50]:<50} T={r['T_nucleus']:.2f}  I={r['I_nucleus']:.2f}  F={r['F_nucleus']:.2f}")
print()

# ====================================================================
# 4. Neutrosophic topic membership
# ====================================================================
# We compute distance from each document to each cluster centroid in 5D UMAP
# space, then map distances to (T, I, F) memberships per topic.

# Reload UMAP coords from topics_docs
docs_topics["topic"] = docs_topics["topic"].astype(int)

# We don't have per-doc soft probabilities saved, so we compute on the fly:
# distance to assigned-cluster vs distance to nearest other cluster.
# T = high relative confidence, I = ambiguous, F = clearly far from a topic.

# Use UMAP 2D coords as proxy (already saved) for the demonstrative computation
coords = docs_topics[["umap_x", "umap_y"]].to_numpy()
labels = docs_topics["topic"].to_numpy()
centroids = np.array([coords[labels == t].mean(axis=0) for t in sorted(np.unique(labels))])

# distance to assigned vs second-closest
import scipy.spatial.distance as dist
all_dists = dist.cdist(coords, centroids)
own = np.array([all_dists[i, labels[i]] for i in range(len(coords))])
sorted_dists = np.sort(all_dists, axis=1)
nearest_other = sorted_dists[:, 1]

# Membership: Gaussian relative to scale
scale = np.median(own) + 1e-6
T_doc = np.exp(-(own ** 2) / (2 * scale ** 2))
margin = nearest_other - own
I_doc = np.exp(-(margin ** 2) / (2 * (scale * 0.5) ** 2)) * 0.5
F_doc = np.maximum(0, 1 - T_doc - I_doc)

docs_n = docs_topics.copy()
docs_n["T_topic"] = T_doc.round(3)
docs_n["I_topic"] = I_doc.round(3)
docs_n["F_topic"] = F_doc.round(3)
docs_n.to_csv(DATA_OUT / "neutrosophic_topics_docs.csv", index=False, encoding="utf-8")

# Aggregate per topic
agg = docs_n.groupby("topic").agg(
    n_docs=("doi", "count"),
    T_mean=("T_topic", "mean"),
    I_mean=("I_topic", "mean"),
    F_mean=("F_topic", "mean"),
).round(3).reset_index()
agg.to_csv(DATA_OUT / "neutrosophic_topics_agg.csv", index=False, encoding="utf-8")

print(f"Documentos con T(asignacion topica) >= 0.7: {(T_doc >= 0.7).sum()} / {len(T_doc)} ({(T_doc >= 0.7).mean():.0%})")
print(f"Documentos con I(ambigua) >= 0.3: {(I_doc >= 0.3).sum()} / {len(I_doc)}")
print()

# ====================================================================
# 5. Neutrosophic co-authorship edge weights
# ====================================================================
# Reload pair counts from earlier run
edges = pd.read_csv(ROOT / "reports" / "clean" / "network_edges.csv")
# w = number of shared articles between pair
# T = saturating function (>=2 articles strongly verified)
# I = exactly 1 article (single-coauthorship, may be opportunistic)
# F = pairs that didn't appear (out of scope here; we only have positive edges)

w = edges["weight"].to_numpy()
T_edge = 1 - np.exp(-(w - 1) / 2)  # saturates as w grows
I_edge = np.where(w == 1, 1.0, np.exp(-(w - 1) / 1.5)) * 0.5
F_edge = np.maximum(0, 1 - T_edge - I_edge)

edges_n = edges.copy()
edges_n["T_collab"] = T_edge.round(3)
edges_n["I_collab"] = I_edge.round(3)
edges_n["F_collab"] = F_edge.round(3)
edges_n.to_csv(DATA_OUT / "neutrosophic_coauth_edges.csv", index=False, encoding="utf-8")

print(f"Aristas T>=0.5 (colaboracion verificada): {(T_edge >= 0.5).sum()} / {len(T_edge)}")
print(f"Aristas I>=0.5 (colaboracion unica): {(I_edge >= 0.5).sum()} / {len(I_edge)}")
print()

# ====================================================================
# Composite figure
# ====================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# A. h-index neutrosophic decomposition
ax = axes[0, 0]
labels_h = ["T (verified)", "I (uncertain)", "F (no evidence)"]
vals_h = [T_h, I_h, F_h]
colors_h = ["#27ae60", "#f39c12", "#c0392b"]
ax.bar(labels_h, vals_h, color=colors_h, alpha=0.85)
for x_, v in zip(range(3), vals_h):
    ax.text(x_, v + 0.01, f"{v:.2f}", ha="center", fontsize=11, fontweight="bold")
ax.set_ylim(0, 1)
ax.set_title("A. Neutrosophic h-index decomposition\n(sample n=26, NCML)", fontsize=11)
ax.set_ylabel("Membership degree")

# B. Bootstrap distribution of Lotka alpha
ax = axes[0, 1]
ax.hist(boot_alphas, bins=40, color="#2874a6", alpha=0.85)
ax.axvline(2.0, color="black", ls="--", lw=1, label="Lotka classical (α=2)")
ax.axvline(mean_alpha, color="red", lw=2, label=f"NCML mean α={mean_alpha:.2f}")
ax.fill_betweenx([0, ax.get_ylim()[1]], ci95[0], ci95[1], alpha=0.2, color="red", label="95% CI bootstrap")
ax.set_title(f"B. Neutrosophic Lotka — α distribution\nT={T_lot:.2f}  I={I_lot:.2f}  F={F_lot:.2f}", fontsize=11)
ax.set_xlabel("α (bootstrap, B=1000)")
ax.set_ylabel("Frequency")
ax.legend(fontsize=8)

# C. Bradford neutrosophic memberships
ax = axes[1, 0]
top10 = bradford_n.head(10).iloc[::-1]
y = np.arange(len(top10))
ax.barh(y - 0.25, top10["T_nucleus"], height=0.25, color="#27ae60", label="T")
ax.barh(y, top10["I_nucleus"], height=0.25, color="#f39c12", label="I")
ax.barh(y + 0.25, top10["F_nucleus"], height=0.25, color="#c0392b", label="F")
ax.set_yticks(y)
ax.set_yticklabels([s[:35] for s in top10["source"]], fontsize=8)
ax.set_xlim(0, 1)
ax.legend(loc="lower right", fontsize=9)
ax.set_title("C. Neutrosophic Bradford nucleus membership\n(top 10 cited journals)", fontsize=11)
ax.set_xlabel("Membership degree")

# D. Document-topic confidence histogram
ax = axes[1, 1]
ax.hist(T_doc, bins=30, color="#8e44ad", alpha=0.85, label="T(topic)")
ax.hist(I_doc, bins=30, color="#f39c12", alpha=0.5, label="I(topic)")
ax.set_title(f"D. Neutrosophic topic membership\n({len(T_doc)} docs)", fontsize=11)
ax.set_xlabel("Membership degree")
ax.set_ylabel("Number of documents")
ax.legend(fontsize=9)

plt.suptitle("Neutrosophic Bibliometric Indicators — NCML Case Study", fontsize=13, y=1.00)
plt.tight_layout()
plt.savefig(FIG_OUT / "neutrosophic_indicators.png", dpi=160, bbox_inches="tight")
plt.close()

print(f"Figura guardada: {FIG_OUT / 'neutrosophic_indicators.png'}")

# Summary
summary = {
    "neutrosophic_h_index": h_neut,
    "neutrosophic_lotka": lotka_neut,
    "bradford_top5_neutrosophic": bradford_n.head(5)[["source", "T_nucleus", "I_nucleus", "F_nucleus"]].to_dict("records"),
    "topics_aggregate": agg.head(5).to_dict("records"),
}
(DATA_OUT / "neutrosophic_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(f"\nResumen completo: {DATA_OUT / 'neutrosophic_summary.json'}")
