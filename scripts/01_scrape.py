"""Scrape NCML Articles.htm -> structured CSV.

Output: data/articles_raw.csv with columns
  volume, year, pages_start, pages_end, pdf_url, title, authors_raw, doi, source_text
"""
from __future__ import annotations
import re
import sys
import csv
from pathlib import Path
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
RAW = ROOT / "data" / "raw.html"
OUT = ROOT / "data" / "articles_raw.csv"
BASE_URL = "https://fs.unm.edu/NCML/"

html = RAW.read_bytes().decode("utf-8", errors="replace")
soup = BeautifulSoup(html, "lxml")

# Each article is inside a <p> (or similar) that contains an anchor to a PDF
# and a single line of text with pattern:
#   "Authors: Title, Neutrosophic Computing and Machine Learning, Vol. N, pages, year. DOI: URL"
# Volume-header anchors have pattern "NCML-<vol>-<year>.pdf" and no authors section.

# Whitespace-ish: normal spaces, nbsp, U+FFFD (replacement chars the page
# actually contains in older volumes because the source HTML has broken encoding
# for accented characters and the original separator byte).
WS = r"[\s\xa0\ufffd]*"
ENTRY_RE = re.compile(
    rf"^(?P<authors>.+?):\s*(?P<title>.+?),{WS}Neutrosophic{WS}Computing{WS}and{WS}Machine{WS}Learning,{WS}"
    rf"Vol\.\s*(?P<vol>\d+),?{WS}(?P<pages>[\d\-\u2013\u2014\s,]*?),?{WS}(?P<year>\d{{4}})\.?"
    rf"(?:{WS}DOI:{WS}(?P<doi>\S+))?",
    re.IGNORECASE | re.DOTALL,
)
# Fallback for entries that omit the journal name before "Vol."
ENTRY_RE_FALLBACK = re.compile(
    rf"^(?P<authors>.+?):\s*(?P<title>.+?),{WS}Vol\.\s*(?P<vol>\d+),?{WS}"
    rf"(?P<pages>[\d\-\u2013\u2014\s,]*?),?{WS}(?P<year>\d{{4}})\.?"
    rf"(?:{WS}DOI:{WS}(?P<doi>\S+))?",
    re.IGNORECASE | re.DOTALL,
)

VOLUME_HEADER_RE = re.compile(r"NCML-(\d+)-(\d{4})\.pdf$", re.IGNORECASE)

rows = []
skipped = 0
volume_headers = []

for a in soup.find_all("a", href=True):
    href = a["href"].strip()
    if not href.lower().endswith(".pdf"):
        continue
    m_vol = VOLUME_HEADER_RE.search(href)
    # Climb to enclosing paragraph-ish block to capture the whole descriptive line
    parent = a
    for _ in range(6):
        if parent.parent is None:
            break
        parent = parent.parent
        if parent.name in ("p", "td", "li", "div"):
            break
    text = parent.get_text(" ", strip=True)
    # Normalize whitespace and entity artifacts
    text = re.sub(r"\s+", " ", text).strip()

    if m_vol:
        volume_headers.append({"volume": int(m_vol.group(1)), "year": int(m_vol.group(2)), "file": href, "text": text})
        continue

    m = ENTRY_RE.search(text) or ENTRY_RE_FALLBACK.search(text)
    if not m:
        skipped += 1
        continue

    pages_raw = (m.group("pages") or "").replace(" ", "")
    pages_start = pages_end = ""
    m_pp = re.match(r"(\d+)[\-\u2013\u2014](\d+)", pages_raw)
    if m_pp:
        pages_start, pages_end = m_pp.group(1), m_pp.group(2)
    elif pages_raw.isdigit():
        pages_start = pages_end = pages_raw

    doi = (m.group("doi") or "").rstrip(".,;")
    # Normalize DOI: strip URL prefix if present
    doi_clean = doi
    for pref in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/"):
        if doi_clean.lower().startswith(pref):
            doi_clean = doi_clean[len(pref):]
            break

    rows.append({
        "volume": int(m.group("vol")),
        "year": int(m.group("year")),
        "pages_start": pages_start,
        "pages_end": pages_end,
        "pdf_url": BASE_URL + href,
        "title": m.group("title").strip(),
        "authors_raw": m.group("authors").strip(),
        "doi": doi_clean,
        "doi_url": doi,
        "source_text": text,
    })

# Dedup by pdf_url (some anchors are duplicated)
seen = set()
unique = []
for r in rows:
    if r["pdf_url"] in seen:
        continue
    seen.add(r["pdf_url"])
    unique.append(r)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(unique[0].keys()))
    writer.writeheader()
    writer.writerows(unique)

print(f"Volumes detected: {len(volume_headers)}")
for v in volume_headers[:10]:
    print(f"  Vol.{v['volume']} ({v['year']})")
print(f"Articles parsed: {len(unique)}  (raw rows before dedup: {len(rows)}; skipped anchors: {skipped})")
print(f"Output: {OUT}")
