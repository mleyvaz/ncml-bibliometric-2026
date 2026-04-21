"""Geographic distribution figure — country + institution composite.

Three panels:
  A. Horizontal bars of authorships by country (Iberoamerica highlighted)
  B. Horizontal bars of top 15 institutions
  C. Ring chart: Iberoamerica vs Otros share (%)
"""
from __future__ import annotations
import sys
from pathlib import Path
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REP = ROOT / "reports" / "clean"
authors = pd.read_csv(ROOT / "data" / "authors_canon.csv")

IBEROAMERICA = {"EC", "CU", "VE", "CO", "MX", "PE", "AR", "CL", "BO", "UY", "PY",
                "CR", "PA", "HN", "GT", "NI", "SV", "DO", "PR", "BR", "ES", "PT"}

country_rows = []
inst_rows = []
for _, r in authors.iterrows():
    for c in str(r.get("countries") or "").split("|"):
        c = c.strip().upper()
        if c and len(c) == 2:
            country_rows.append(c)
    inst_s = str(r.get("institutions") or "")
    if inst_s and inst_s.lower() != "nan":
        for i in inst_s.split("|"):
            i = i.strip()
            if i and i.lower() != "nan":
                inst_rows.append(i)

cc = Counter(country_rows)
ic = Counter(inst_rows)

# Country df
cdata = []
for iso, n in cc.most_common():
    try:
        name = pycountry.countries.get(alpha_2=iso).name
    except AttributeError:
        name = iso
    if len(name) > 25:
        name = name.split(",")[0]
    cdata.append({"iso": iso, "country": name, "authorships": n,
                  "group": "Iberoamerica" if iso in IBEROAMERICA else "Otros"})
cdf = pd.DataFrame(cdata)

ib_total = cdf[cdf["group"] == "Iberoamerica"]["authorships"].sum()
ot_total = cdf[cdf["group"] == "Otros"]["authorships"].sum()
total = ib_total + ot_total

# Institution df
idf = pd.DataFrame(ic.most_common(15), columns=["institution", "authorships"])

# ---------- Figure ----------
fig = plt.figure(figsize=(16, 11))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, 0.55], hspace=0.5, wspace=0.35)

# Panel A: countries
ax = fig.add_subplot(gs[0, 0])
top = cdf.head(12).iloc[::-1]
colors = ["#c0392b" if g == "Iberoamerica" else "#7f8c8d" for g in top["group"]]
ax.barh(range(len(top)), top["authorships"], color=colors, alpha=0.9)
ax.set_yticks(range(len(top)))
ax.set_yticklabels([f"{row.country} ({row.iso})" for _, row in top.iterrows()], fontsize=9)
for i, v in enumerate(top["authorships"]):
    ax.text(v + 1, i, str(v), va="center", fontsize=8)
ax.set_xlabel("Autorias")
ax.set_title("A. Distribucion por pais (rojo: Iberoamerica; subset OpenAlex)", fontsize=11)
ax.grid(axis="x", alpha=0.3)

# Panel B: institutions
ax = fig.add_subplot(gs[0, 1])
top_i = idf.iloc[::-1]
ax.barh(range(len(top_i)), top_i["authorships"], color="#2874a6", alpha=0.85)
ax.set_yticks(range(len(top_i)))
ax.set_yticklabels([(s[:48] + "…") if len(s) > 48 else s for s in top_i["institution"]], fontsize=8)
for i, v in enumerate(top_i["authorships"]):
    ax.text(v + 0.3, i, str(v), va="center", fontsize=8)
ax.set_xlabel("Autorias")
ax.set_title("B. Top 15 instituciones", fontsize=11)
ax.grid(axis="x", alpha=0.3)

# Panel C: ring chart (spans both columns bottom)
ax = fig.add_subplot(gs[1, :])
ax.axis("off")
# Donut
donut_ax = fig.add_axes([0.03, 0.05, 0.30, 0.38])
donut_ax.pie([ib_total, ot_total], labels=[f"Iberoamerica\n{ib_total}", f"Otros\n{ot_total}"],
             colors=["#c0392b", "#7f8c8d"], autopct="%1.0f%%", startangle=90,
             wedgeprops=dict(width=0.35, edgecolor="white"), textprops={"fontsize": 10})
donut_ax.set_title(f"C. Concentracion regional\n(n = {total} autorias OpenAlex)", fontsize=10)

# Summary text box spanning right
ax.text(0.36, 0.85,
        f"Paises distintos: {len(cdf)}\n"
        f"Autorias Iberoamerica: {ib_total}/{total} ({ib_total/total:.1%})\n"
        f"Ecuador: {cdf.iloc[0]['authorships']} ({cdf.iloc[0]['authorships']/total:.1%})\n"
        f"Top 3 (EC+CU+VE): {cdf.head(3)['authorships'].sum()} ({cdf.head(3)['authorships'].sum()/total:.1%})\n"
        f"\nTop institucion: {idf.iloc[0]['institution'][:46]}\n"
        f"  con {idf.iloc[0]['authorships']} autorias",
        fontsize=11, verticalalignment="top", transform=ax.transAxes,
        family="monospace",
        bbox=dict(facecolor="#fcf3cf", edgecolor="#d4ac0d", alpha=0.85, boxstyle="round,pad=0.6"))

plt.suptitle("Distribucion geografica e institucional de NCML", fontsize=13, y=0.99)
plt.savefig(REP / "geo.png", dpi=160, bbox_inches="tight")
plt.close()

print(f"Paises: {len(cdf)}  Iberoamerica {ib_total}/{total} = {ib_total/total:.0%}")
print(f"Output: {REP / 'geo.png'}")
