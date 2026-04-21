"""Temporal evolution of topics in NCML.

Inputs:
  data/topics_docs.csv   (doc, topic, year, volume, title)
  data/topics_labels.csv (topic, size, top_terms)

Outputs:
  reports/clean/topics_over_time.csv      (topic x year matrix, absolute)
  reports/clean/topics_over_time_norm.csv (topic x year, % of year total)
  reports/clean/topics_heatmap.png        heatmap normalized
  reports/clean/topics_trend.png          growth-rate table: emerging vs declining
  reports/clean/topics_temporal.md        narrative
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
DOCS = ROOT / "data" / "topics_docs.csv"
LABS = ROOT / "data" / "topics_labels.csv"
REP = ROOT / "reports" / "clean"
REP.mkdir(parents=True, exist_ok=True)

docs = pd.read_csv(DOCS)
labs = pd.read_csv(LABS)
labs["short"] = labs["top_terms"].fillna("").str.split(",").str[:3].map(lambda x: ", ".join(s.strip() for s in x))
label_map = dict(zip(labs["topic"], labs["short"]))

# Focus on 2018-2025 (2026 too sparse)
docs = docs[(docs["year"] >= 2018) & (docs["year"] <= 2025)].copy()

# Topic x Year matrix
mat = docs.groupby(["topic", "year"]).size().unstack(fill_value=0).astype(int)
mat = mat.reindex(sorted(labs["topic"]))
mat.to_csv(REP / "topics_over_time.csv")

# Normalize per year (% of that year)
norm = mat.div(mat.sum(axis=0).replace(0, np.nan), axis=1).fillna(0) * 100
norm.to_csv(REP / "topics_over_time_norm.csv")

# ---- Growth rate: (share in 2023-2025) - (share in 2018-2020)
early = norm.loc[:, [y for y in norm.columns if y in (2018, 2019, 2020)]].mean(axis=1)
late = norm.loc[:, [y for y in norm.columns if y in (2023, 2024, 2025)]].mean(axis=1)
growth = pd.DataFrame({
    "topic": mat.index,
    "label": [label_map.get(t, "") for t in mat.index],
    "size_total": mat.sum(axis=1).values,
    "share_early_%": early.values.round(1),
    "share_late_%": late.values.round(1),
    "delta_pp": (late - early).values.round(1),
}).sort_values("delta_pp", ascending=False)
growth.to_csv(REP / "topics_growth.csv", index=False, encoding="utf-8")

# ---- Heatmap (normalized % per year, rows sorted by total size) ----
order = mat.sum(axis=1).sort_values(ascending=False).index
heat = norm.loc[order]
labels_y = [f"T{t} ({label_map.get(t, '')[:32]})" for t in order]

fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(heat.values, aspect="auto", cmap="YlOrRd")
ax.set_xticks(range(len(heat.columns)))
ax.set_xticklabels(heat.columns, rotation=0)
ax.set_yticks(range(len(labels_y)))
ax.set_yticklabels(labels_y, fontsize=8)
ax.set_title("Share de topicos por ano (% del total anual)")
ax.set_xlabel("Ano")
# Annotate % values
for i in range(heat.shape[0]):
    for j in range(heat.shape[1]):
        v = heat.values[i, j]
        if v > 0.5:
            ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                    color="black" if v < 15 else "white", fontsize=7)
plt.colorbar(im, ax=ax, label="%")
plt.tight_layout()
plt.savefig(REP / "topics_heatmap.png", dpi=150)
plt.close()

# ---- Growth chart (emerging vs declining) ----
fig, ax = plt.subplots(figsize=(10, 8))
g = growth.sort_values("delta_pp")
colors = ["#c0392b" if v < 0 else "#2874a6" for v in g["delta_pp"]]
ax.barh(range(len(g)), g["delta_pp"], color=colors)
ax.set_yticks(range(len(g)))
ax.set_yticklabels([f"T{int(t)} {lab[:40]}" for t, lab in zip(g["topic"], g["label"])], fontsize=8)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Cambio en share (%) 2018-20 -> 2023-25 [puntos porcentuales]")
ax.set_title("Topicos emergentes (azul) vs declinantes (rojo)")
ax.grid(True, axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(REP / "topics_trend.png", dpi=150)
plt.close()

# ---- Narrative ----
md = ["# Evolucion temporal de topicos — NCML 2018-2025", "",
      f"- Documentos con abstract: {mat.values.sum()}",
      f"- Topicos: {len(mat)} (de paso 13)",
      "",
      "## Topicos mas emergentes (mayor alza en share 2018-20 -> 2023-25)",
      "",
      "| Topico | Label | Early % | Late % | Delta pp |",
      "|---|---|---|---|---|"]
for _, r in growth.head(7).iterrows():
    md.append(f"| T{int(r['topic'])} | {r['label'][:60]} | {r['share_early_%']} | {r['share_late_%']} | +{r['delta_pp']} |")
md.append("")
md.append("## Topicos declinantes")
md.append("")
md.append("| Topico | Label | Early % | Late % | Delta pp |")
md.append("|---|---|---|---|---|")
for _, r in growth.tail(7).iterrows():
    md.append(f"| T{int(r['topic'])} | {r['label'][:60]} | {r['share_early_%']} | {r['share_late_%']} | {r['delta_pp']} |")
md.append("")
md.append("![Heatmap](topics_heatmap.png)")
md.append("")
md.append("![Trend](topics_trend.png)")

(REP / "topics_temporal.md").write_text("\n".join(md), encoding="utf-8")

print("Topicos con mayor crecimiento:")
for _, r in growth.head(5).iterrows():
    print(f"  T{int(r['topic'])} delta=+{r['delta_pp']:>5.1f}pp  {r['label'][:70]}")
print("\nTopicos declinantes:")
for _, r in growth.tail(5).iterrows():
    print(f"  T{int(r['topic'])} delta={r['delta_pp']:>5.1f}pp  {r['label'][:70]}")
print(f"\nOutputs: {REP}")
