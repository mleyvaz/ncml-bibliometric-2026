"""Create compressed ZIP backups of the complete bibliometric project.

Splits output in two files because PDFs make the total ~450 MB:
  NCML_bibliometric_pdfs.zip        — 728 PDFs + download_manifest.csv
  NCML_bibliometric_analysis.zip    — data/, reports/, paper/, scripts/, Excel

Both together = full reproducible snapshot.
"""
from __future__ import annotations
import sys
import zipfile
from pathlib import Path
import hashlib
import datetime

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
PDFS_ZIP = ROOT / "NCML_bibliometric_pdfs.zip"
ANALYSIS_ZIP = ROOT / "NCML_bibliometric_analysis.zip"


def add_dir(zf: zipfile.ZipFile, src_dir: Path, arcroot: str, skip_exts=()):
    for p in src_dir.rglob("*"):
        if not p.is_file():
            continue
        if any(str(p).lower().endswith(e) for e in skip_exts):
            continue
        arcname = f"{arcroot}/{p.relative_to(src_dir).as_posix()}"
        zf.write(p, arcname)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# Manifest with metadata
manifest_lines = [
    f"# NCML Bibliometric Dataset — backup",
    f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}",
    f"Source: https://fs.unm.edu/NCML/Articles.htm",
    f"Corpus: 762 articles, 42 volumes, 2018-2026 (partial)",
    "",
    "## Archives",
    "- NCML_bibliometric_pdfs.zip    — 728 full-text PDFs + manifest",
    "- NCML_bibliometric_analysis.zip — data, figures, reports, paper draft, scripts",
    "",
    "Licenses: CC-BY 4.0 (data), MIT (code).",
    "See paper/00_outline.md for authorship, COI and target journal.",
]
(ROOT / "MANIFEST.md").write_text("\n".join(manifest_lines), encoding="utf-8")


# ---------- PDFs zip ----------
print("Building PDFs zip...")
with zipfile.ZipFile(PDFS_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    add_dir(zf, ROOT / "data" / "pdfs", "pdfs")
    # include manifest of what was downloaded + source URLs
    for fn in ("download_manifest.csv", "raw.html"):
        p = ROOT / "data" / fn
        if p.exists():
            zf.write(p, f"meta/{fn}")
    zf.write(ROOT / "MANIFEST.md", "MANIFEST.md")
print(f"  -> {PDFS_ZIP}  ({PDFS_ZIP.stat().st_size / 1e6:.1f} MB)")

# ---------- Analysis zip ----------
print("Building analysis zip...")
with zipfile.ZipFile(ANALYSIS_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    # Exclude the large pdfs/ subfolder and the per-article .txt fulltext (heavy)
    for p in (ROOT / "data").rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[:2] == ("data", "pdfs"):
            continue
        if rel.parts[:2] == ("data", "pdf_fulltext"):
            continue  # extractable from PDFs; excluded to keep zip small
        zf.write(p, rel.as_posix())

    add_dir(zf, ROOT / "reports", "reports")
    add_dir(zf, ROOT / "paper", "paper")
    add_dir(zf, ROOT / "scripts", "scripts", skip_exts=(".pyc",))

    # Top-level artifacts
    for name in ("NCML_bibliometric_dataset.xlsx", "MANIFEST.md"):
        p = ROOT / name
        if p.exists():
            zf.write(p, name)

print(f"  -> {ANALYSIS_ZIP}  ({ANALYSIS_ZIP.stat().st_size / 1e6:.1f} MB)")

# Hashes
print("\nSHA-256:")
for p in (PDFS_ZIP, ANALYSIS_ZIP):
    h = file_hash(p)
    print(f"  {p.name}: {h}")

# Also write hash file
(ROOT / "backup_hashes.txt").write_text(
    "\n".join(f"{file_hash(p)}  {p.name}" for p in (PDFS_ZIP, ANALYSIS_ZIP)),
    encoding="utf-8",
)
print(f"\nHashes saved to: {ROOT / 'backup_hashes.txt'}")
