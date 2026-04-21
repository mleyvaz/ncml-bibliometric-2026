"""Fetch OpenAlex + DataCite data for all valid DOIs.

Uses a thread pool for speed. Writes:
  data/openalex_raw.jsonl  (one JSON line per resolved work)
  data/datacite_raw.jsonl  (one JSON line per resolved record)
"""
from __future__ import annotations
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
from tqdm import tqdm

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
IN = ROOT / "data" / "articles_clean.csv"
OA_OUT = ROOT / "data" / "openalex_raw.jsonl"
DC_OUT = ROOT / "data" / "datacite_raw.jsonl"

UA = {"User-Agent": "ncml-bibliometrics/1.0 (mailto:mleyvaz@gmail.com)"}

df = pd.read_csv(IN)
dois = df.loc[df["doi_valid"] == True, "doi"].dropna().unique().tolist()
print(f"Valid DOIs: {len(dois)}")


def fetch(url: str) -> dict | None:
    for attempt in range(3):
        try:
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                time.sleep(1.5 * (attempt + 1))
                continue
            return None
        except requests.RequestException:
            time.sleep(1.5)
    return None


def fetch_openalex(doi: str):
    j = fetch(f"https://api.openalex.org/works/doi:{doi}")
    return doi, j


def fetch_datacite(doi: str):
    j = fetch(f"https://api.datacite.org/dois/{doi}")
    return doi, j


def run_parallel(fn, label, out_path, max_workers=8):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    resolved = 0
    with out_path.open("w", encoding="utf-8") as f_out, ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(fn, d): d for d in dois}
        for fut in tqdm(as_completed(futs), total=len(futs), desc=label):
            doi, j = fut.result()
            if j is None:
                continue
            resolved += 1
            f_out.write(json.dumps({"_doi": doi, "data": j}, ensure_ascii=False) + "\n")
    print(f"{label}: resolved {resolved} / {len(dois)}")


run_parallel(fetch_openalex, "OpenAlex", OA_OUT, max_workers=8)
run_parallel(fetch_datacite, "DataCite", DC_OUT, max_workers=6)
