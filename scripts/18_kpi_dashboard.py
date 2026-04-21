"""KPI dashboard — one figure that summarizes the paper at a glance.

Panels:
  A. Key numbers (text box)
  B. Articles over time (compact bar)
  C. Topic size distribution (horizontal bar, top 10)
  D. Bradford Zone 1 top sources (horizontal bar)
  E. Top co-author communities
  F. Scholar vs OpenAlex citation comparison (bar)
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
REP = ROOT / "reports" / "clean"

works = pd.read_csv(ROOT / "data" / "works.csv")
authors = pd.read_csv(ROOT / "data" / "authors_canon.csv")
topics = pd.read_csv(ROOT / "data" / "topics_labels.csv")
bradford = pd.read_csv(REP / "bradford_sources.csv")
with open(REP / "lotka_fit.json") as f:
    lotka = json.load(f)
with open(REP / "bradford_zones.json") as f:
    bz = json.load(f)
with open(REP / "network_stats.json") as f:
    ns = json.load(f)
comm = pd.read_csv(REP / "coauth_communities.csv")

# ---- Load Scholar sample (validated) ----
try:
    sch = pd.read_csv(ROOT / "data" / "scholar_sample_clean.csv")
except FileNotFoundError:
    sch = pd.read_csv(ROOT / "data" / "scholar_sample_results.csv")
    sch.loc[sch["volume"] == 10, "scholar_cites"] = 1  # manual fix for known bad row

# ---- Compute KPIs ----
years = works["year"]
kpis = {
    "articles_total": len(works),
    "articles_with_doi": int((works["doi"].fillna("").str.startswith("10.")).sum()),
    "volumes": works["volume"].nunique(),
    "year_range": f"{int(years.min())}-{int(years.max())}",
    "unique_authors": int(authors["cluster_id"].nunique()),
    "lotka_alpha": lotka["alpha"],
    "lotka_ks_pass": lotka["ks_pass"],
    "bradford_nucleus": bz["zone1_nucleus"],
    "bradford_nucleus_share": f"{bz['zone1_cites']/bz['total_citations']:.0%}",
    "references_parsed": bz["total_citations"],
    "topics": len(topics),
    "network_nodes": ns["nodes"],
    "network_largest_cc_share": ns["largest_component_share"],
    "network_modularity": 0.96,  # from script
    "scholar_h5": 10,
    "scholar_h5_median": 25,
    "oa_h": 1,
    "oa_total_citations": int(pd.to_numeric(works["oa_cited_by"], errors="coerce").fillna(0).sum()),
    "scholar_sample_mean": round(pd.to_numeric(sch["scholar_cites"], errors="coerce").fillna(0).mean(), 1),
    "scholar_sample_pct_cited": round((pd.to_numeric(sch["scholar_cites"], errors="coerce").fillna(0) >= 1).mean() * 100, 1),
}
pd.Series(kpis).to_csv(REP / "kpis.csv", header=False, encoding="utf-8")
with open(REP / "kpis.json", "w") as f:
    json.dump(kpis, f, indent=2, default=str)

# ---- Figure ----
fig = plt.figure(figsize=(16, 11))
gs = fig.add_gridspec(3, 3, height_ratios=[1.1, 1, 1], hspace=0.55, wspace=0.38)

# A — key numbers box
axA = fig.add_subplot(gs[0, 0])
axA.axis("off")
txt = (
    f"COBERTURA\n"
    f"  Articulos totales:     {kpis['articles_total']}\n"
    f"  Volumenes:             {kpis['volumes']}  ({kpis['year_range']})\n"
    f"  Autores unicos:        {kpis['unique_authors']:,}\n"
    f"  Referencias parseadas: {kpis['references_parsed']:,}\n"
    f"  Topicos identificados: {kpis['topics']}\n\n"
    f"IMPACTO\n"
    f"  Scholar h5-index:      {kpis['scholar_h5']}\n"
    f"  Scholar h5-mediana:    {kpis['scholar_h5_median']}\n"
    f"  OpenAlex h-index:      {kpis['oa_h']}  (cobertura parcial)\n"
    f"  Muestra Scholar:       {kpis['scholar_sample_pct_cited']}% con >=1 cita\n"
    f"  Media cites Scholar:   {kpis['scholar_sample_mean']}/articulo\n\n"
    f"ESTRUCTURA\n"
    f"  Lotka alpha:           {kpis['lotka_alpha']:.2f}\n"
    f"  Modularidad red:       {kpis['network_modularity']}\n"
    f"  Componente principal:  {kpis['network_largest_cc_share']:.0%} autores\n"
    f"  Bradford nucleo:       {kpis['bradford_nucleus']} revistas = {kpis['bradford_nucleus_share']} citas"
)
axA.text(0, 1, txt, fontsize=10, family="monospace", va="top",
         bbox=dict(facecolor="#fef9e7", edgecolor="#d4ac0d", boxstyle="round,pad=0.7"))
axA.set_title("A. Indicadores clave", fontsize=11, loc="left")

# B — articles over time
axB = fig.add_subplot(gs[0, 1:])
ay = works.groupby("year").size().reindex(range(2018, 2027), fill_value=0)
bars = axB.bar(ay.index, ay.values, color="#2874a6", alpha=0.85)
bars[-1].set_hatch("///"); bars[-1].set_alpha(0.5)
for x, v in zip(ay.index, ay.values):
    axB.text(x, v + 3, str(v), ha="center", fontsize=8)
axB.set_title("B. Articulos publicados por ano (2026 parcial)", fontsize=11, loc="left")
axB.set_ylabel("Articulos")
axB.grid(axis="y", alpha=0.3)

# C — Topics top 10
axC = fig.add_subplot(gs[1, 0])
top_t = topics.head(10).iloc[::-1]
axC.barh(range(len(top_t)), top_t["size"], color="#8e44ad", alpha=0.85)
labels = [f"T{int(t)}: {s.split(',')[0][:25]}" for t, s in zip(top_t["topic"], top_t["top_terms"])]
axC.set_yticks(range(len(top_t)))
axC.set_yticklabels(labels, fontsize=8)
for i, v in enumerate(top_t["size"]):
    axC.text(v + 0.4, i, str(int(v)), va="center", fontsize=8)
axC.set_title("C. 10 topicos mas grandes", fontsize=11, loc="left")
axC.set_xlabel("Articulos")
axC.grid(axis="x", alpha=0.3)

# D — Bradford top sources
axD = fig.add_subplot(gs[1, 1])
top_b = bradford.head(10).iloc[::-1]
colors_b = ["#c0392b" if "neutrosophic" in s.lower() else "#2874a6" for s in top_b["source"]]
axD.barh(range(len(top_b)), top_b["cites"], color=colors_b, alpha=0.85)
ticks_b = [(s[:38] + "…") if len(s) > 38 else s for s in top_b["source"]]
axD.set_yticks(range(len(top_b)))
axD.set_yticklabels(ticks_b, fontsize=8)
for i, v in enumerate(top_b["cites"]):
    axD.text(v + 10, i, str(int(v)), va="center", fontsize=8)
axD.set_title("D. Top 10 revistas citadas\n(rojo: ecosistema neutrosofico)", fontsize=11, loc="left")
axD.set_xlabel("Citas en referencias")
axD.grid(axis="x", alpha=0.3)

# E — Communities
axE = fig.add_subplot(gs[1, 2])
top_c = comm.head(10).iloc[::-1]
axE.barh(range(len(top_c)), top_c["total_articles"], color="#16a085", alpha=0.85)
labels_e = [f"C{int(c)}: {a.split(';;')[0][:28]}" for c, a in zip(top_c["community"], top_c["top_authors"])]
axE.set_yticks(range(len(top_c)))
axE.set_yticklabels(labels_e, fontsize=8)
for i, v in enumerate(top_c["total_articles"]):
    axE.text(v + 0.7, i, str(int(v)), va="center", fontsize=8)
axE.set_title("E. Comunidades de coautoria (Louvain)\ntop 10 por produccion", fontsize=11, loc="left")
axE.set_xlabel("Articulos")
axE.grid(axis="x", alpha=0.3)

# F — Scholar vs OpenAlex comparison
axF = fig.add_subplot(gs[2, 0])
cats = ["OpenAlex h", "Scholar h5"]
vals = [kpis["oa_h"], kpis["scholar_h5"]]
bars = axF.bar(cats, vals, color=["#7f8c8d", "#e67e22"], alpha=0.85)
for b, v in zip(bars, vals):
    axF.text(b.get_x() + b.get_width()/2, v + 0.3, str(v), ha="center", fontsize=11, fontweight="bold")
axF.set_title("F. Discrepancia OpenAlex vs Scholar", fontsize=11, loc="left")
axF.set_ylabel("h-index")
axF.grid(axis="y", alpha=0.3)
axF.text(0.5, 0.95, f"Factor: {kpis['scholar_h5']/max(1,kpis['oa_h']):.0f}x",
         transform=axF.transAxes, ha="center", fontsize=10,
         bbox=dict(facecolor="#fdf2e9", edgecolor="#e67e22"))

# G — Lotka concentration (Pareto)
axG = fig.add_subplot(gs[2, 1])
per = authors.groupby("cluster_id")["doi"].nunique().rename("n")
per = per[per > 0].sort_values(ascending=False).reset_index(drop=True)
cum_share = (per.cumsum() / per.sum()) * 100
x_frac = (np.arange(1, len(per) + 1) / len(per)) * 100
axG.plot(x_frac, cum_share, "r-", lw=2)
axG.fill_between(x_frac, cum_share, 0, alpha=0.2, color="red")
axG.plot([0, 100], [0, 100], "--", color="#7f8c8d", lw=0.8)
axG.set_xlabel("% de autores (ranking)")
axG.set_ylabel("% de articulos acumulados")
axG.set_title("G. Concentracion de autoria (Pareto)", fontsize=11, loc="left")
axG.grid(alpha=0.3)
# Annotate 80/20
idx80 = (cum_share >= 80).idxmax() if any(cum_share >= 80) else len(per) - 1
pct80 = x_frac[idx80] if idx80 < len(x_frac) else 100
axG.axhline(80, ls=":", color="gray", lw=0.7)
axG.annotate(f"80% articulos\n⇐ {pct80:.1f}% autores", xy=(pct80, 80), xytext=(pct80 + 10, 60),
             arrowprops=dict(arrowstyle="->", color="gray"), fontsize=9)

# H — Topic evolution: T14 education vs T0 legal (biggest swings)
axH = fig.add_subplot(gs[2, 2])
docs = pd.read_csv(ROOT / "data" / "topics_docs.csv")
for tid, color, label in [(14, "#c0392b", "T14 Educacion (↓)"), (7, "#8e44ad", "T7 Teoria (↓)"),
                          (0, "#2874a6", "T0 Legal/Ecuador (↑)"), (22, "#16a085", "T22 Odontologia (↑)")]:
    series = docs[docs["topic"] == tid].groupby("year").size().reindex(range(2018, 2026), fill_value=0)
    axH.plot(series.index, series.values, "-o", ms=4, color=color, label=label, lw=1.5)
axH.set_title("H. Cambio de identidad tematica", fontsize=11, loc="left")
axH.set_ylabel("Articulos/ano")
axH.set_xlabel("Ano")
axH.legend(fontsize=8, loc="upper left")
axH.grid(alpha=0.3)

plt.suptitle("NCML 2018-2026 — Dashboard bibliometrico", fontsize=14, y=0.995)
plt.savefig(REP / "dashboard.png", dpi=170, bbox_inches="tight")
plt.close()

# Narrative table
md_lines = [
    "# KPIs del estudio bibliometrico NCML 2018-2026",
    "",
    "| Indicador | Valor |",
    "|---|---|",
]
for k, v in kpis.items():
    md_lines.append(f"| {k.replace('_', ' ')} | {v} |")
md_lines.extend([
    "",
    "## Figura resumen",
    "![Dashboard](dashboard.png)",
])
(REP / "kpis.md").write_text("\n".join(md_lines), encoding="utf-8")

print(json.dumps(kpis, indent=2, default=str))
print(f"\nOutput: {REP / 'dashboard.png'}, {REP / 'kpis.csv'}, {REP / 'kpis.md'}")
