"""Populate the github_repo/ folder with scripts, data, figures and paper."""
from __future__ import annotations
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REPO = ROOT / "github_repo"

# --- Scripts (all .py) ---
scripts_dst = REPO / "scripts"
scripts_dst.mkdir(exist_ok=True)
for p in (ROOT / "scripts").glob("*.py"):
    shutil.copy2(p, scripts_dst / p.name)
print(f"Copied {len(list(scripts_dst.glob('*.py')))} scripts")

# --- Data (exclude heavy files) ---
data_dst = REPO / "data"
data_dst.mkdir(exist_ok=True)

SKIP_PREFIXES = ("raw.html", "openalex_raw", "datacite_raw")
SKIP_DIRS = ("pdfs", "pdf_fulltext")

for p in (ROOT / "data").iterdir():
    if p.is_dir() and p.name in SKIP_DIRS:
        continue
    if p.is_file():
        if any(p.name.startswith(pref) for pref in SKIP_PREFIXES):
            continue
        if p.suffix.lower() == ".jsonl" and p.stat().st_size > 5_000_000:
            continue  # skip huge raw JSONL
        shutil.copy2(p, data_dst / p.name)
print(f"Copied {len(list(data_dst.glob('*')))} data files")

# --- Figures ---
fig_dst = REPO / "figures"
fig_dst.mkdir(exist_ok=True)
for p in (ROOT / "reports" / "clean").glob("*.png"):
    shutil.copy2(p, fig_dst / p.name)
print(f"Copied {len(list(fig_dst.glob('*.png')))} figures")

# --- Paper ---
paper_dst = REPO / "paper"
paper_dst.mkdir(exist_ok=True)
for p in (ROOT / "paper").iterdir():
    if p.is_file() and p.suffix.lower() in (".md", ".bib", ".docx"):
        # Skip intermediate files
        if p.stem in ("final_extract",):
            continue
        shutil.copy2(p, paper_dst / p.name)
print(f"Copied {len(list(paper_dst.glob('*')))} paper files")

# --- docs/ with REPRODUCE + DATASET quick guides ---
docs_dst = REPO / "docs"
docs_dst.mkdir(exist_ok=True)

(docs_dst / "REPRODUCE.md").write_text(
    "# Reproducing the analysis\n\n"
    "1. Clone the repo and install dependencies (see README).\n"
    "2. Ensure network access (scripts 01, 03 fetch from the web).\n"
    "3. Run scripts in numeric order (01 through 22).\n"
    "4. Expect ~30 min end-to-end on a modern laptop.\n\n"
    "## Troubleshooting\n\n"
    "- **UnicodeEncodeError on Windows**: each script uses `sys.stdout.reconfigure`\n"
    "  but if you run via `python -X utf8 script.py` it is even safer.\n"
    "- **hdbscan wheel fails on Python 3.14**: the pipeline uses KMeans instead\n"
    "  (not HDBSCAN). If you want HDBSCAN, downgrade to Python 3.12.\n"
    "- **OpenAlex rate limit**: the default 8 threads stay below the polite\n"
    "  pool; if you get 429s, reduce `max_workers` in `03_fetch_apis.py`.\n"
    "- **Scholar CAPTCHA**: `06_scholar_sample.py` stops on detection; run it\n"
    "  from a residential IP, not a cloud VM.\n",
    encoding="utf-8",
)

(docs_dst / "DATASET.md").write_text(
    "# Dataset guide\n\n"
    "## NCML_bibliometric_dataset.xlsx (19 sheets)\n\n"
    "| Sheet | Rows | Description |\n"
    "|---|---|---|\n"
    "| README | 12 | Metadata of the study |\n"
    "| KPIs | 20 | Consolidated indicators |\n"
    "| Articulos | 762 | Articles with DOI, volume, year, pages, URLs |\n"
    "| Autores | 1,363 | Unique authors (post-disambiguation) |\n"
    "| Autorias | 2,225 | Authorship rows with affiliations and ORCID |\n"
    "| Topicos | 24 | Topics with size and top terms |\n"
    "| Topicos_docs | 725 | Doc-to-topic assignment + UMAP 2D coordinates |\n"
    "| Topicos_ano | 24 | Topic x year share matrix |\n"
    "| Topicos_crec | 24 | Emerging vs declining topics |\n"
    "| Bradford | 2,339 | Journals cited, ranked by frequency |\n"
    "| Lotka_fit | 10 | Fit parameters + K-S diagnostics |\n"
    "| Lotka_dist | 17 | Distribution n(x) vs number of authors |\n"
    "| Comunidades | 81 | Louvain communities |\n"
    "| Paises | 14 | Country distribution |\n"
    "| Instituciones | 45 | Top institutions |\n"
    "| Scholar_muestra | 26 | Scholar vs OpenAlex sample |\n"
    "| Crecimiento | 9 | Articles and authors per year |\n"
    "| Red_stats | 11 | Network metrics |\n"
    "| Red_top_pares | 300 | Top 300 co-authoring pairs |\n\n"
    "Each sheet is also available as a CSV in `data/` for programmatic access.\n",
    encoding="utf-8",
)

(docs_dst / "INSTALL.md").write_text(
    "# Installation\n\n"
    "```bash\n"
    "# Clone\n"
    "git clone https://github.com/mleyvaz/ncml-bibliometric-2026.git\n"
    "cd ncml-bibliometric-2026\n\n"
    "# Virtual environment\n"
    "python -m venv venv\n"
    "source venv/bin/activate    # Linux/Mac\n"
    "venv\\Scripts\\activate      # Windows\n\n"
    "# Install dependencies\n"
    "pip install -r requirements.txt\n"
    "```\n\n"
    "Tested on: Python 3.11, 3.12, 3.14 (Windows 11, Ubuntu 22.04, macOS 14).\n\n"
    "Python 3.14 quirks: `hdbscan` wheels may be missing. The pipeline already\n"
    "uses KMeans by default, so no action needed; if you want HDBSCAN topic\n"
    "modeling, use Python 3.12 and `pip install bertopic`.\n",
    encoding="utf-8",
)
print(f"Wrote docs")

# --- Manifest of the repo ---
manifest_lines = ["# Repository manifest", ""]
for path in sorted(REPO.rglob("*")):
    if path.is_file() and not path.name.startswith("."):
        rel = path.relative_to(REPO)
        manifest_lines.append(f"- `{rel.as_posix()}` ({path.stat().st_size:,} bytes)")
(REPO / "MANIFEST.md").write_text("\n".join(manifest_lines), encoding="utf-8")
print(f"Wrote MANIFEST with {len(manifest_lines) - 2} files")

# --- Size summary ---
total = sum(p.stat().st_size for p in REPO.rglob("*") if p.is_file())
print(f"\nTotal repo size: {total / 1e6:.2f} MB")
