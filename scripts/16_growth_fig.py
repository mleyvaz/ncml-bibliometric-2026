"""Growth figure: articulos por ano + evolucion de autores + cumulative.

Two-panel composite:
  Left  — bar of articles/year with overlaid line of cumulative articles
  Right — bar of unique authors per year + line of cumulative unique authors
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REP = ROOT / "reports" / "clean"
works = pd.read_csv(ROOT / "data" / "works.csv")
authors = pd.read_csv(ROOT / "data" / "authors_canon.csv")

# Drop 2026 partial? Keep but flag
# Articles per year
ay = works.groupby("year").size().reindex(range(2018, 2027), fill_value=0)
cum = ay.cumsum()

# First-time authors per year (new clusters appearing that year)
authors = authors[authors["cluster_id"].notna() & (authors["cluster_id"] != "")].copy()
authors["cluster_id"] = authors["cluster_id"].astype(int)
first_year = authors.groupby("cluster_id")["year"].min()
new_authors_per_year = first_year.value_counts().reindex(range(2018, 2027), fill_value=0).sort_index()
cum_authors = new_authors_per_year.cumsum()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Panel 1: articles
ax = axes[0]
bars = ax.bar(ay.index, ay.values, color="#2874a6", alpha=0.85, label="Articulos/ano")
# Highlight 2026 as partial
if 2026 in ay.index:
    idx = list(ay.index).index(2026)
    bars[idx].set_hatch("///")
    bars[idx].set_alpha(0.5)
ax.set_xlabel("Ano")
ax.set_ylabel("Articulos publicados")
ax.set_title("Crecimiento anual de NCML")
ax.grid(axis="y", alpha=0.3)
for x, v in zip(ay.index, ay.values):
    ax.text(x, v + 3, str(v), ha="center", fontsize=8, color="#1a3a5c")

ax2 = ax.twinx()
ax2.plot(cum.index, cum.values, "r-o", ms=5, lw=2, label="Acumulado")
ax2.set_ylabel("Articulos acumulados", color="red")
ax2.tick_params(axis="y", labelcolor="red")
# Note 2026 incomplete
ax.text(2026, ay.loc[2026] + 20, "(parcial)", ha="center", fontsize=7, color="#555",
        style="italic")
# Fit exponential to 2018-2025
years = np.array([y for y in ay.index if y <= 2025])
vals = np.array([ay.loc[y] for y in years])
# Simple exponential via log-linear
mask = vals > 0
if mask.sum() > 3:
    coefs = np.polyfit(years[mask], np.log(vals[mask]), 1)
    cagr = np.exp(coefs[0]) - 1
    ax.text(0.02, 0.95, f"Tasa anual (CAGR 2018-25): {cagr:.0%}",
            transform=ax.transAxes, fontsize=10, color="#1a3a5c",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="#2874a6"))

# Panel 2: authors
ax = axes[1]
ax.bar(new_authors_per_year.index, new_authors_per_year.values, color="#27ae60", alpha=0.85, label="Nuevos autores/ano")
ax.set_xlabel("Ano")
ax.set_ylabel("Nuevos autores (primera publicacion)", color="#1e7043")
ax.set_title("Incorporacion de autores y comunidad acumulada")
ax.grid(axis="y", alpha=0.3)
for x, v in zip(new_authors_per_year.index, new_authors_per_year.values):
    ax.text(x, v + 5, str(v), ha="center", fontsize=8, color="#1e7043")
ax2 = ax.twinx()
ax2.plot(cum_authors.index, cum_authors.values, "b-o", ms=5, lw=2, label="Autores acumulados")
ax2.set_ylabel("Autores acumulados (comunidad)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

plt.suptitle("NCML 2018-2026 — Crecimiento editorial y formacion de comunidad", fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(REP / "growth.png", dpi=160, bbox_inches="tight")
plt.close()

print(f"Articulos 2018 -> 2025: {ay.loc[2018]} -> {ay.loc[2025]}")
print(f"CAGR articulos 2018-2025: {cagr:.0%}")
print(f"Autores unicos total: {cum_authors.iloc[-1]}")
print(f"Output: {REP / 'growth.png'}")
