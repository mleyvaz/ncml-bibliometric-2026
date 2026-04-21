"""Download all NCML PDFs listed in works.csv to data/pdfs/.

Parallel downloads with retries; skips files already present.
Outputs data/download_manifest.csv with local_path, size, status per DOI.
"""
from __future__ import annotations
import sys
import time
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
from tqdm import tqdm

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
WORKS = ROOT / "data" / "works.csv"
PDF_DIR = ROOT / "data" / "pdfs"
MANIFEST = ROOT / "data" / "download_manifest.csv"
PDF_DIR.mkdir(parents=True, exist_ok=True)

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    )
}

df = pd.read_csv(WORKS)
# Dedup by pdf_url (several rows can share the same PDF file e.g. volume headers
# or encoding-twin entries) to avoid two threads racing on the same local path.
df = df.drop_duplicates(subset=["pdf_url"]).reset_index(drop=True)
print(f"Targets: {len(df)} unique PDFs")


def safe_name(url: str, doi: str) -> str:
    # Prefer DOI suffix for stable naming; fallback to URL filename hash
    if isinstance(doi, str) and doi:
        return doi.replace("/", "_").replace(":", "_") + ".pdf"
    h = hashlib.sha1(url.encode()).hexdigest()[:12]
    return f"nodoi_{h}.pdf"


def download(url: str, dest: Path) -> tuple[str, int, str]:
    if dest.exists() and dest.stat().st_size > 1000:
        return "exists", dest.stat().st_size, ""
    for attempt in range(3):
        try:
            r = requests.get(url, headers=UA, timeout=60, stream=True)
            if r.status_code != 200:
                return f"http_{r.status_code}", 0, ""
            ct = r.headers.get("content-type", "")
            # Stream to file
            tmp = dest.with_suffix(".part")
            with tmp.open("wb") as f:
                for chunk in r.iter_content(65536):
                    if chunk:
                        f.write(chunk)
            # Validate it's a PDF (first 5 bytes == %PDF-)
            with tmp.open("rb") as f:
                head = f.read(5)
            if head != b"%PDF-":
                tmp.unlink(missing_ok=True)
                return "not_pdf", 0, ct
            try:
                tmp.replace(dest)  # Windows-safe atomic replace
            except OSError:
                time.sleep(0.2)
                tmp.replace(dest)
            return "ok", dest.stat().st_size, ct
        except requests.RequestException as e:
            time.sleep(1.5 * (attempt + 1))
            last = str(e)
    return "error", 0, last[:120]


def worker(row):
    url = row["pdf_url"]
    doi = row["doi"] if isinstance(row["doi"], str) else ""
    dest = PDF_DIR / safe_name(url, doi)
    status, size, info = download(url, dest)
    return {
        "doi": doi,
        "pdf_url": url,
        "local_path": str(dest),
        "status": status,
        "size": size,
        "info": info,
    }


rows = []
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(worker, r) for _, r in df.iterrows()]
    for f in tqdm(as_completed(futs), total=len(futs), desc="PDFs"):
        rows.append(f.result())

manifest = pd.DataFrame(rows)
manifest.to_csv(MANIFEST, index=False, encoding="utf-8")

status_counts = manifest["status"].value_counts().to_dict()
total_size_mb = manifest["size"].sum() / 1e6
print(f"\nStatus: {status_counts}")
print(f"Total size: {total_size_mb:.1f} MB")
print(f"Manifest: {MANIFEST}")
