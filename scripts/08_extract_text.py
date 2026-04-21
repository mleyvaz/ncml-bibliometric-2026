"""Extract text + structured fields from downloaded NCML PDFs.

For each PDF we try to pull:
  - full_text (concatenated pages)
  - resumen (Spanish abstract)
  - abstract (English abstract)
  - keywords (es/en)
  - affiliations_block (numbered footer lines like "1 Universidad ... Ecuador. E-mail:")
  - emails (all @-containing tokens)
  - references_block (text after "Referencias" / "References")

Heuristics are Spanish-NCML specific. We fall back to empty strings when a
section cannot be located.

Output: data/pdf_extract.csv and data/pdf_fulltext/<doi>.txt (one per article).
"""
from __future__ import annotations
import sys
import re
import glob
from pathlib import Path
import fitz  # PyMuPDF
import pandas as pd
from tqdm import tqdm

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
PDF_DIR = ROOT / "data" / "pdfs"
OUT_TXT_DIR = ROOT / "data" / "pdf_fulltext"
OUT_TXT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = ROOT / "data" / "pdf_extract.csv"

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)

# Markers that open each section. Ordered by priority.
RESUMEN_RE = re.compile(r"\bResumen\b\s*[.:]?\s*", re.I)
ABSTRACT_RE = re.compile(r"\bAbstract\b\s*[.:]?\s*", re.I)
# Keywords markers — Spanish and English variants
KW_ES_RE = re.compile(r"Palabras\s*clave\s*[:\-]?\s*", re.I)
KW_EN_RE = re.compile(r"Keywords?\s*[:\-]?\s*", re.I)
# References block
REFS_RE = re.compile(r"\b(Referencias|References|Bibliograf[ií]a)\b\s*\n", re.I)


def cut_section(text: str, start_re: re.Pattern, max_len: int = 4000, end_res: list[re.Pattern] = None) -> str:
    """Cut from first match of start_re up to the first match of any end_res
    (or max_len chars, whichever comes first)."""
    m = start_re.search(text)
    if not m:
        return ""
    start = m.end()
    chunk = text[start : start + max_len]
    end_positions = [max_len]
    for er in end_res or []:
        em = er.search(chunk)
        if em:
            end_positions.append(em.start())
    return chunk[: min(end_positions)].strip()


def extract_pdf(path: Path) -> dict:
    try:
        doc = fitz.open(path)
    except Exception as e:
        return {"ok": False, "error": f"open: {e}"}
    try:
        pages = [p.get_text() for p in doc]
    finally:
        doc.close()
    full = "\n".join(pages)
    # Normalize whitespace a bit
    clean = re.sub(r"[ \t]+", " ", full)
    clean = re.sub(r"-\n", "", clean)  # fix hyphenation at line end

    resumen = cut_section(clean, RESUMEN_RE, max_len=2500,
                          end_res=[ABSTRACT_RE, KW_ES_RE, KW_EN_RE, re.compile(r"\n\n1\.\s*Introducci")])
    abstract = cut_section(clean, ABSTRACT_RE, max_len=2500,
                           end_res=[KW_ES_RE, KW_EN_RE, re.compile(r"\n\n1\.\s*Introduction")])
    kw_es = cut_section(clean, KW_ES_RE, max_len=500,
                        end_res=[ABSTRACT_RE, KW_EN_RE, re.compile(r"\n\n1[\.:]\s")])
    kw_en = cut_section(clean, KW_EN_RE, max_len=500,
                        end_res=[RESUMEN_RE, KW_ES_RE, re.compile(r"\n\n1[\.:]\s")])
    # References: take everything after last REFS match
    refs = ""
    for m in REFS_RE.finditer(clean):
        refs = clean[m.end():].strip()
    # Emails = easy heuristic for affiliations coverage
    emails = sorted(set(EMAIL_RE.findall(clean)))

    return {
        "ok": True,
        "pages": len(pages),
        "chars": len(full),
        "resumen": resumen,
        "abstract": abstract,
        "keywords_es": kw_es,
        "keywords_en": kw_en,
        "references_block": refs[:15000],  # cap
        "n_emails": len(emails),
        "emails": "|".join(emails),
        "fulltext": full,
    }


files = sorted(glob.glob(str(PDF_DIR / "*.pdf")))
print(f"PDFs found: {len(files)}")

rows = []
for path in tqdm(files, desc="Extract"):
    p = Path(path)
    data = extract_pdf(p)
    fn = p.stem  # DOI-derived name
    if data.get("ok"):
        (OUT_TXT_DIR / f"{fn}.txt").write_text(data.pop("fulltext"), encoding="utf-8", errors="replace")
    rows.append({"pdf_file": p.name, "doi_stub": fn, **{k: v for k, v in data.items() if k != "fulltext"}})

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False, encoding="utf-8")

print(f"\nExtracted: {df['ok'].sum()} / {len(df)}")
print(f"Avg abstract len (es): {df['resumen'].fillna('').map(len).mean():.0f} chars")
print(f"Avg abstract len (en): {df['abstract'].fillna('').map(len).mean():.0f} chars")
print(f"With keywords_es: {(df['keywords_es'].fillna('').map(len) > 10).sum()}")
print(f"With references_block: {(df['references_block'].fillna('').map(len) > 50).sum()}")
print(f"With emails: {(df['n_emails'].fillna(0) > 0).sum()}")
print(f"Output: {OUT_CSV}")
