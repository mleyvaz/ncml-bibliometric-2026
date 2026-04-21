"""Build analysis-ready tables from raw scraped data + OpenAlex + DataCite.

Outputs:
  data/works.csv         — one row per article
  data/authors.csv       — one row per (article, author)
  data/concepts.csv      — one row per (article, concept) from OpenAlex
"""
from __future__ import annotations
import sys
import json
import re
from pathlib import Path
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
CLEAN = ROOT / "data" / "articles_clean.csv"
OA = ROOT / "data" / "openalex_raw.jsonl"
DC = ROOT / "data" / "datacite_raw.jsonl"
OUT_W = ROOT / "data" / "works.csv"
OUT_A = ROOT / "data" / "authors.csv"
OUT_C = ROOT / "data" / "concepts.csv"


def load_jsonl(p: Path) -> dict:
    out = {}
    if not p.exists():
        return out
    for line in p.open(encoding="utf-8"):
        rec = json.loads(line)
        out[rec["_doi"]] = rec["data"]
    return out


df = pd.read_csv(CLEAN)
oa = load_jsonl(OA)
dc = load_jsonl(DC)
print(f"Articles: {len(df)}  OpenAlex: {len(oa)}  DataCite: {len(dc)}")


def split_authors_local(s: str):
    if not isinstance(s, str):
        return []
    # Split on comma / " and "; strip
    parts = re.split(r",\s*|\s+y\s+|\s+and\s+", s)
    return [p.strip() for p in parts if p.strip()]


# ------- Build works table -------
work_rows = []
for _, r in df.iterrows():
    doi = r["doi"] if isinstance(r["doi"], str) else ""
    oa_w = oa.get(doi, {})
    dc_w = (dc.get(doi, {}).get("data", {}) or {}).get("attributes", {}) if dc.get(doi) else {}
    authorships = oa_w.get("authorships", []) or []
    countries = set()
    insts = set()
    for au in authorships:
        for c in au.get("countries", []) or []:
            countries.add(c)
        for inst in au.get("institutions", []) or []:
            if inst.get("display_name"):
                insts.add(inst["display_name"])
            if inst.get("country_code"):
                countries.add(inst["country_code"])
    work_rows.append({
        "doi": doi,
        "volume": r["volume"],
        "year": r["year"],
        "pages_start": r["pages_start"],
        "pages_end": r["pages_end"],
        "pdf_url": r["pdf_url"],
        "title_local": r["title"],
        "authors_local": r["authors_raw"],
        "n_authors_local": len(split_authors_local(r["authors_raw"])),
        # OpenAlex
        "oa_id": oa_w.get("id", ""),
        "oa_title": oa_w.get("title", ""),
        "oa_cited_by": oa_w.get("cited_by_count", ""),
        "oa_n_authors": len(authorships),
        "oa_type": oa_w.get("type", ""),
        "oa_is_oa": (oa_w.get("open_access") or {}).get("is_oa", ""),
        "oa_countries": "|".join(sorted(countries)),
        "oa_institutions": "|".join(sorted(insts))[:4000],
        "oa_concepts_top": "|".join(
            c.get("display_name", "") for c in (oa_w.get("concepts") or [])[:5]
        ),
        # DataCite
        "dc_views": dc_w.get("viewCount", ""),
        "dc_downloads": dc_w.get("downloadCount", ""),
        "dc_citations": dc_w.get("citationCount", ""),
        "dc_publisher": dc_w.get("publisher", ""),
        "dc_pubyear": dc_w.get("publicationYear", ""),
    })

works = pd.DataFrame(work_rows)
works.to_csv(OUT_W, index=False, encoding="utf-8")
print(f"works.csv: {len(works)} rows")

# ------- Build authors table -------
auth_rows = []
for _, r in df.iterrows():
    doi = r["doi"] if isinstance(r["doi"], str) else ""
    vol, yr = r["volume"], r["year"]
    oa_w = oa.get(doi, {})
    dc_w = (dc.get(doi, {}).get("data", {}) or {}).get("attributes", {}) if dc.get(doi) else {}
    authorships = oa_w.get("authorships", []) or []
    dc_creators = dc_w.get("creators") or []
    # Prefer OpenAlex if we have detailed data, else DataCite, else local split
    if authorships:
        for au in authorships:
            a = au.get("author", {}) or {}
            auth_rows.append({
                "doi": doi, "volume": vol, "year": yr,
                "source": "openalex",
                "position": au.get("author_position"),
                "name": a.get("display_name"),
                "orcid": (a.get("orcid") or "").replace("https://orcid.org/", ""),
                "oa_author_id": a.get("id", ""),
                "institutions": "|".join(i.get("display_name", "") for i in (au.get("institutions") or [])),
                "countries": "|".join(au.get("countries") or []),
            })
    elif dc_creators:
        for i, c in enumerate(dc_creators):
            # orcid lookup
            orcid = ""
            for nid in c.get("nameIdentifiers") or []:
                if nid.get("nameIdentifierScheme", "").upper() == "ORCID":
                    orcid = nid.get("nameIdentifier", "").replace("https://orcid.org/", "")
            auth_rows.append({
                "doi": doi, "volume": vol, "year": yr,
                "source": "datacite",
                "position": "first" if i == 0 else ("last" if i == len(dc_creators) - 1 else "middle"),
                "name": c.get("name") or c.get("givenName", "") + " " + c.get("familyName", ""),
                "orcid": orcid, "oa_author_id": "",
                "institutions": "|".join(a.get("name", "") for a in (c.get("affiliation") or []) if isinstance(a, dict)),
                "countries": "",
            })
    else:
        # Fallback: local split
        names = split_authors_local(r["authors_raw"])
        for i, n in enumerate(names):
            auth_rows.append({
                "doi": doi, "volume": vol, "year": yr,
                "source": "local",
                "position": "first" if i == 0 else ("last" if i == len(names) - 1 else "middle"),
                "name": n, "orcid": "", "oa_author_id": "",
                "institutions": "", "countries": "",
            })

authors = pd.DataFrame(auth_rows)
# Normalize name: strip + collapse spaces + title case only if all upper
authors["name_norm"] = (
    authors["name"].fillna("").astype(str)
    .str.replace(r"\s+", " ", regex=True).str.strip()
)
authors.to_csv(OUT_A, index=False, encoding="utf-8")
print(f"authors.csv: {len(authors)} rows ({authors['source'].value_counts().to_dict()})")

# ------- Build concepts table (OpenAlex only) -------
concept_rows = []
for doi, w in oa.items():
    for c in (w.get("concepts") or []):
        concept_rows.append({
            "doi": doi,
            "concept": c.get("display_name"),
            "level": c.get("level"),
            "score": c.get("score"),
        })
concepts = pd.DataFrame(concept_rows)
concepts.to_csv(OUT_C, index=False, encoding="utf-8")
print(f"concepts.csv: {len(concepts)} rows")
