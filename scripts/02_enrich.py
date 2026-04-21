"""Enrich NCML articles with OpenAlex metadata.

Reads data/articles_raw.csv -> writes data/articles_enriched.csv plus
data/authorships.csv (one row per (article, author) pair) and
data/concepts.csv (one row per (article, concept)).
"""
from __future__ import annotations
import sys
import time
import json
import csv
from pathlib import Path
import requests
import pandas as pd
from tqdm import tqdm

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
RAW = ROOT / "data" / "articles_raw.csv"
OUT_WORKS = ROOT / "data" / "articles_enriched.csv"
OUT_AUTH = ROOT / "data" / "authorships.csv"
OUT_CONCEPTS = ROOT / "data" / "concepts.csv"
OUT_RAWJSON = ROOT / "data" / "openalex_raw.jsonl"

UA = {"User-Agent": "ncml-bibliometrics/1.0 (mailto:mleyvaz@gmail.com)"}

df = pd.read_csv(RAW)
dois = [d for d in df["doi"].dropna().unique().tolist() if d]
print(f"Unique DOIs to query: {len(dois)}")

works = {}  # doi -> openalex work
sess = requests.Session()
sess.headers.update(UA)

def fetch_one(doi):
    url = f"https://api.openalex.org/works/doi:{doi}"
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                time.sleep(2 + attempt * 2)
                continue
            return None
        except requests.RequestException:
            time.sleep(2)
    return None

missed = []
with OUT_RAWJSON.open("w", encoding="utf-8") as raw_out:
    for d in tqdm(dois, desc="OpenAlex"):
        w = fetch_one(d)
        if w is None:
            missed.append(d)
            continue
        works[d.lower()] = w
        raw_out.write(json.dumps(w, ensure_ascii=False) + "\n")
        time.sleep(0.11)  # ~9 req/s, within polite pool (10/s)

print(f"Missed (not in OpenAlex): {len(missed)}")
(ROOT / "data" / "openalex_missed.txt").write_text("\n".join(missed), encoding="utf-8")

print(f"Resolved {len(works)} / {len(dois)} via OpenAlex")

# Build enriched works table
work_rows = []
auth_rows = []
concept_rows = []

for _, row in df.iterrows():
    doi = (row["doi"] or "").lower() if isinstance(row["doi"], str) else ""
    w = works.get(doi)
    base = {
        "doi": doi,
        "volume": row["volume"],
        "year": row["year"],
        "title_local": row["title"],
        "authors_local": row["authors_raw"],
        "pdf_url": row["pdf_url"],
    }
    if not w:
        base.update({"openalex_id": "", "title_oa": "", "cited_by_count": "", "n_authors": "",
                     "is_oa": "", "type": "", "publication_date": "",
                     "countries": "", "institutions": ""})
        work_rows.append(base)
        continue
    authorships = w.get("authorships", []) or []
    countries, insts = set(), set()
    for au in authorships:
        for c in au.get("countries", []) or []:
            countries.add(c)
        for inst in au.get("institutions", []) or []:
            if inst.get("display_name"):
                insts.add(inst["display_name"])
            for c in inst.get("country_code", "") or []:
                countries.add(c)
        # Authorship row
        author = au.get("author", {}) or {}
        auth_rows.append({
            "doi": doi,
            "volume": row["volume"],
            "year": row["year"],
            "author_position": au.get("author_position"),
            "author_name": author.get("display_name"),
            "author_orcid": (author.get("orcid") or "").replace("https://orcid.org/", ""),
            "openalex_author_id": author.get("id"),
            "institutions": "|".join(i.get("display_name", "") for i in (au.get("institutions") or []) if i.get("display_name")),
            "countries": "|".join(au.get("countries") or []),
        })
    for c in (w.get("concepts") or []):
        concept_rows.append({
            "doi": doi,
            "concept": c.get("display_name"),
            "level": c.get("level"),
            "score": c.get("score"),
        })
    base.update({
        "openalex_id": w.get("id"),
        "title_oa": w.get("title"),
        "cited_by_count": w.get("cited_by_count"),
        "n_authors": len(authorships),
        "is_oa": (w.get("open_access") or {}).get("is_oa"),
        "type": w.get("type"),
        "publication_date": w.get("publication_date"),
        "countries": "|".join(sorted(countries)),
        "institutions": "|".join(sorted(insts))[:5000],
    })
    work_rows.append(base)

pd.DataFrame(work_rows).to_csv(OUT_WORKS, index=False, encoding="utf-8")
pd.DataFrame(auth_rows).to_csv(OUT_AUTH, index=False, encoding="utf-8")
pd.DataFrame(concept_rows).to_csv(OUT_CONCEPTS, index=False, encoding="utf-8")
print(f"Wrote {OUT_WORKS} ({len(work_rows)} rows)")
print(f"Wrote {OUT_AUTH} ({len(auth_rows)} rows)")
print(f"Wrote {OUT_CONCEPTS} ({len(concept_rows)} rows)")
