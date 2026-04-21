"""Normalize DOIs in articles_raw.csv.

Some entries have 'https://zenodo.org/record/NNN' or similar URL forms
in place of a DOI. Convert them to the canonical '10.5281/zenodo.NNN' DOI.
"""
from __future__ import annotations
import sys
import re
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
IN = ROOT / "data" / "articles_raw.csv"
OUT = ROOT / "data" / "articles_clean.csv"

df = pd.read_csv(IN)

def norm_doi(v: str) -> str:
    if not isinstance(v, str) or not v:
        return ""
    v = v.strip().rstrip(".,;")
    # Direct zenodo record URL -> DOI
    m = re.search(r"zenodo\.org/record/(\d+)", v, re.I)
    if m:
        return f"10.5281/zenodo.{m.group(1)}"
    m = re.search(r"zenodo\.org/records?/(\d+)", v, re.I)
    if m:
        return f"10.5281/zenodo.{m.group(1)}"
    # Plain DOI variations
    for pref in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi.org/"):
        if v.lower().startswith(pref):
            return v[len(pref):]
    return v

df["doi_norm"] = df["doi"].fillna("").astype(str).map(norm_doi)
# Keep only records with DOI shape "10.NNNN/..."
df["doi_valid"] = df["doi_norm"].str.contains(r"^10\.\d{3,}/")
df["doi"] = df["doi_norm"]
df = df.drop(columns=["doi_norm"])
df.to_csv(OUT, index=False, encoding="utf-8")
print(f"Rows: {len(df)}  valid DOIs: {df['doi_valid'].sum()}")
print(df[~df["doi_valid"]].head(3)[["volume", "pdf_url", "doi"]].to_string())
