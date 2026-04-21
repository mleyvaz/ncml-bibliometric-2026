"""Query Google Scholar for a stratified sample of NCML articles.

Rate-limit-friendly: delay, browser UA, stops on CAPTCHA.
"""
from __future__ import annotations
import sys
import re
import time
import random
import urllib.parse as up
from pathlib import Path
import requests
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
IN = ROOT / "data" / "scholar_sample.csv"
OUT = ROOT / "data" / "scholar_sample_results.csv"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")

df = pd.read_csv(IN)
print(f"Sample: {len(df)} articles")

sess = requests.Session()
sess.headers.update({
    "User-Agent": UA,
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml",
})

CAPTCHA_MARKERS = ("unusual traffic", "/sorry/", "not a robot", "captcha")

def clean_title(t: str) -> str:
    # Strip replacement chars and collapse spaces
    t = re.sub(r"[\ufffd]", "", t or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def scholar_cites(title: str) -> tuple[int | None, str]:
    q = clean_title(title)[:250]
    url = "https://scholar.google.com/scholar?" + up.urlencode({"q": q, "hl": "es"})
    r = sess.get(url, timeout=30)
    if r.status_code != 200:
        return None, f"http {r.status_code}"
    body = r.text
    if any(m in body.lower() for m in CAPTCHA_MARKERS):
        return None, "captcha"
    if '<div class="gs_r' not in body:
        return None, "no_result"
    # Take the FIRST "Cited by N" / "Citado por N" in the page — this is the
    # cites-count of the first (most relevant) result.
    m = re.search(r"Citado por\s*(\d+)|Cited by\s*(\d+)", body)
    if m:
        n = int(m.group(1) or m.group(2))
        return n, "ok"
    # A result exists but no cites row visible = 0 cites
    return 0, "ok_no_cite"

results = []
for i, row in df.iterrows():
    title = row["title_local"]
    before = time.time()
    n, status = scholar_cites(title)
    elapsed = time.time() - before
    print(f"  [{i+1}/{len(df)}] Vol.{row['volume']} | OA={int(row['oa_cited_by']) if pd.notna(row['oa_cited_by']) else '-'} | Scholar={n} ({status}) | {elapsed:.1f}s")
    results.append({**row.to_dict(), "scholar_cites": n, "status": status})
    if status == "captcha":
        print("  CAPTCHA encountered — stopping.")
        break
    # Random sleep 6-14s to stay polite
    time.sleep(random.uniform(6, 14))

pd.DataFrame(results).to_csv(OUT, index=False, encoding="utf-8")
print(f"Wrote {OUT}")
