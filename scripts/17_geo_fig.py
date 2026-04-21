"""Geographic distribution figure.

Two-panel:
  Left  — horizontal bar chart of authorships by country (Iberoamerica highlight)
  Right — choropleth world map (matplotlib with country polygons)

To avoid heavy GIS dependencies, we use naturalearth data downloaded from
cartopy-data if present, else fallback to bar-only layout. We'll implement
a lightweight choropleth using country centroids colored by count + bubble size.
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

# Expand country col (pipe-separated) into rows; 1 count per authorship
rows = []
for _, r in authors.iterrows():
    s = str(r.get("countries") or "")
    if not s or s == "nan":
        continue
    for c in s.split("|"):
        c = c.strip().upper()
        if c and len(c) == 2:
            rows.append(c)
cc = Counter(rows)

# Map ISO-2 to full name + Iberoamerica flag
IBEROAMERICA = {"EC", "CU", "VE", "CO", "MX", "PE", "AR", "CL", "BO", "UY", "PY",
                "CR", "PA", "HN", "GT", "NI", "SV", "DO", "PR", "BR", "ES"}
full = []
for iso, n in cc.most_common():
    try:
        name = pycountry.countries.get(alpha_2=iso).name
    except AttributeError:
        name = iso
    full.append({"iso": iso, "country": name, "authorships": n,
                 "group": "Iberoamerica" if iso in IBEROAMERICA else "Otros"})
df = pd.DataFrame(full)
df.to_csv(REP / "countries_full.csv", index=False, encoding="utf-8")

# ---------- Figure ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 6.5))

# Left — horizontal bars (top 15)
top = df.head(15).iloc[::-1]
colors = ["#c0392b" if g == "Iberoamerica" else "#7f8c8d" for g in top["group"]]
axes[0].barh(range(len(top)), top["authorships"], color=colors, alpha=0.85)
axes[0].set_yticks(range(len(top)))
axes[0].set_yticklabels([f"{row.country} ({row.iso})" for _, row in top.iterrows()], fontsize=10)
for i, v in enumerate(top["authorships"]):
    axes[0].text(v + 1, i, str(v), va="center", fontsize=9)
axes[0].set_xlabel("Autorias (OpenAlex)")
axes[0].set_title("Distribucion geografica de autorias\n(rojo: Iberoamerica)")
axes[0].grid(axis="x", alpha=0.3)

# Right — bubble-world map using lat/lon approx
# Hard-coded capital coords for the main countries; avoids shapefile deps
CENTROIDS = {
    "EC": (-78.5, -1.8), "CU": (-77.8, 21.5), "VE": (-66.6, 6.4),
    "CO": (-74.3, 4.6), "MX": (-102.5, 23.6), "PE": (-75.0, -9.2),
    "AR": (-63.6, -38.4), "CL": (-71.5, -35.7), "BO": (-64.7, -16.3),
    "UY": (-55.8, -32.5), "PY": (-58.4, -23.4), "CR": (-83.8, 9.7),
    "PA": (-80.8, 8.5), "HN": (-86.2, 15.2), "GT": (-90.2, 15.8),
    "DO": (-70.2, 18.7), "BR": (-51.9, -14.2), "ES": (-3.7, 40.4),
    "US": (-95.7, 37.1), "PT": (-8.2, 39.4),
    "JP": (138.3, 36.2), "IN": (78.9, 20.6), "CN": (104.2, 35.9),
    "BG": (25.5, 42.7), "RO": (24.9, 45.9), "IT": (12.6, 41.9),
    "FR": (2.2, 46.2), "DE": (10.5, 51.2), "GB": (-3.4, 55.4),
    "PL": (19.1, 51.9), "TR": (35.2, 38.9), "RU": (105.3, 61.5),
    "EG": (30.8, 26.8), "IR": (53.7, 32.4), "PK": (69.3, 30.4),
    "BD": (90.4, 23.7), "ID": (113.9, -0.8), "PH": (121.8, 12.9),
    "KR": (127.8, 35.9), "VN": (108.3, 14.1),
    "AU": (133.8, -25.3), "ZA": (22.9, -30.6),
    "CA": (-106.3, 56.1), "MA": (-7.1, 31.8), "NG": (8.7, 9.1),
}
ax = axes[1]
# Simple world outline via matplotlib basemap? use draw-polyline approx:
# Instead of a map, draw a grayed background rectangle (Mercator-ish) and plot points.
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)
ax.set_facecolor("#eaf2f8")
ax.set_aspect("equal")

# Draw continent boxes as rough background
ax.axhline(0, color="#b0b0b0", lw=0.3)
ax.axvline(0, color="#b0b0b0", lw=0.3)
for spine in ax.spines.values():
    spine.set_color("#b0b0b0")

max_count = df["authorships"].max() if not df.empty else 1
for _, row in df.iterrows():
    iso = row["iso"]
    c = CENTROIDS.get(iso)
    if c is None:
        continue
    size = 30 + 1800 * (row["authorships"] / max_count)
    color = "#c0392b" if row["group"] == "Iberoamerica" else "#2874a6"
    ax.scatter(c[0], c[1], s=size, color=color, alpha=0.55, edgecolor="white", lw=0.5)
    if row["authorships"] >= 3:
        ax.annotate(f"{iso} ({row['authorships']})", c, fontsize=7,
                    ha="center", va="center", color="black", fontweight="bold")

ax.set_title("Burbujas por pais (tamano = autorias)")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.grid(True, linestyle="--", alpha=0.2)

plt.suptitle("Distribucion geografica de autores NCML (subset OpenAlex, n = {} autorias)".format(
    int(df["authorships"].sum())), fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(REP / "geo.png", dpi=160, bbox_inches="tight")
plt.close()

print(f"Paises detectados: {len(df)}")
ib = df[df["group"] == "Iberoamerica"]["authorships"].sum()
total = df["authorships"].sum()
print(f"Iberoamerica: {ib} / {total} ({ib/total:.0%})")
top5 = ", ".join(f"{r['iso']}={r['authorships']}" for _, r in df.head(5).iterrows())
print(f"Top 5: {top5}")
print(f"Output: {REP / 'geo.png'}")
