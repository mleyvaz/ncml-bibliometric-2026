"""Bradford's law analysis on NCML cited references.

Strategy:
  1. Split each article's references_block on [N] markers.
  2. Heuristic extraction of the "journal/source" string from each reference.
  3. Normalize aggressively (lowercase, strip accents, collapse spaces,
     trim common junk) to merge variants.
  4. Rank sources by citation frequency and compute Bradford zones.

Known limitations (documented in output): without GROBID-quality reference
parsing, book chapters, theses and URLs contaminate the journal list. We
focus on the top-decile which is much cleaner than the tail.
"""
from __future__ import annotations
import sys
import re
import json
import unicodedata
from collections import Counter
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
EXTRACT = ROOT / "data" / "pdf_extract.csv"
REP = ROOT / "reports" / "clean"
REP.mkdir(exist_ok=True, parents=True)

df = pd.read_csv(EXTRACT)
print(f"Articles: {len(df)}")

REF_SPLIT = re.compile(r"(?:(?<=\n)|(?<=\s))\[\s*\d+\s*\]\.?\s*", re.MULTILINE)
# Alternative for "1." or "1)" numbering
REF_SPLIT_NUMERIC = re.compile(r"(?:(?<=\n)|\A)\s*\d{1,3}[\.\)]\s+", re.MULTILINE)

# ---- Heuristic journal extraction ----
# After picking references, try patterns in order:
# P1: ", “Title,” JOURNAL[, ]vol..."
# P2: "Title. JOURNAL, vol..."
# P3: ", JOURNAL, vol..."
# P4: " in JOURNAL"
QUOTE = "[\"\u201c\u201d]"
JOURNAL_RES = [
    re.compile(QUOTE + r"([^\"\u201c\u201d]{4,})" + QUOTE + r",?\s*(?P<j>[^,]{4,120}?),\s*vol", re.IGNORECASE),
    re.compile(r"\.\s*(?P<j>[A-Z][^\.]{4,120}?)[,\.]\s*(?:vol|Vol|VOL)\.\s*\d", re.IGNORECASE),
    re.compile(r",\s*(?P<j>[A-Z][A-Za-z&\-\s\u00c0-\u017f]{4,120}?),\s*(?:vol|Vol)\.\s*\d", re.IGNORECASE),
    re.compile(r"\bin\s+(?P<j>[A-Z][A-Za-z&\-\s\u00c0-\u017f]{4,120}?)(?:,|\.)", re.IGNORECASE),
]

KNOWN = [
    ("Neutrosophic Sets and Systems", re.compile(r"neutrosophic\s+sets?\s+and\s+systems?\b", re.I)),
    ("Neutrosophic Computing and Machine Learning", re.compile(r"neutrosophic\s+computing\s+and\s+machine\s+learning", re.I)),
    ("International Journal of Neutrosophic Science", re.compile(r"international\s+journal\s+of\s+neutrosophic\s+science", re.I)),
    ("Plithogenic Logic and Computation", re.compile(r"plithogenic\s+logic\s+and\s+computation", re.I)),
    ("Fuzzy Sets and Systems", re.compile(r"fuzzy\s+sets?\s+and\s+systems?", re.I)),
    ("Information Sciences", re.compile(r"\binformation\s+sciences\b", re.I)),
    ("Expert Systems with Applications", re.compile(r"expert\s+systems\s+with\s+applications", re.I)),
    ("Applied Soft Computing", re.compile(r"applied\s+soft\s+computing", re.I)),
    ("Symmetry", re.compile(r"\bsymmetry\b\s*(?!,|\.)\s*,?\s*vol", re.I)),
    ("IEEE Access", re.compile(r"\bieee\s+access\b", re.I)),
    ("Knowledge-Based Systems", re.compile(r"knowledge\-?based\s+systems", re.I)),
]


def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def canon_source(s: str) -> str:
    s = strip_accents(s).lower()
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(" .,;:-")
    # Drop common rubbish prefixes
    s = re.sub(r"^(ed\.|eds?\.\s*by|in\s+)", "", s)
    return s


def extract_refs(block: str) -> list[str]:
    if not isinstance(block, str) or len(block) < 30:
        return []
    # Prefer [N] style; if none found, fallback to numeric "1." style.
    parts = REF_SPLIT.split(block)
    if len(parts) < 3:
        parts = REF_SPLIT_NUMERIC.split(block)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p and len(p.strip()) > 20]


def detect_journal(ref: str) -> str | None:
    # 1) First, match against known list — strongest signal
    for label, pat in KNOWN:
        if pat.search(ref):
            return label
    # 2) Generic heuristics
    for rx in JOURNAL_RES:
        m = rx.search(ref)
        if m:
            candidate = m.group("j").strip(" .,\"'()")
            # Filter nonsense: avoid all-caps acronyms that are obviously not journals
            if len(candidate) >= 5 and len(candidate) <= 120:
                return candidate
    return None


# Parse all references
all_refs_by_doc = []
n_refs_total = 0
n_refs_with_journal = 0

for _, row in df.iterrows():
    refs = extract_refs(row.get("references_block", ""))
    all_refs_by_doc.append(refs)
    for r in refs:
        n_refs_total += 1
        if detect_journal(r):
            n_refs_with_journal += 1

print(f"Total extracted references: {n_refs_total}")
print(f"Mean refs per article: {n_refs_total / max(1, len(df)):.1f}")
print(f"References with detected journal: {n_refs_with_journal} ({n_refs_with_journal/max(1,n_refs_total):.1%})")

# Aggregate journal counts (canonicalized)
source_counter = Counter()
for refs in all_refs_by_doc:
    for r in refs:
        src = detect_journal(r)
        if src:
            source_counter[canon_source(src)] += 1

print(f"Unique sources detected: {len(source_counter)}")

# Save full list
src_df = (pd.DataFrame(source_counter.most_common(), columns=["source", "cites"])
          .assign(rank=lambda d: range(1, len(d) + 1)))
src_df.to_csv(REP / "bradford_sources.csv", index=False, encoding="utf-8")

# --------- Bradford zones ---------
# Canonical: sort sources by freq desc; cumulative citation-count curve;
# split into 3 zones of ~equal cumulative citations.
cum = src_df["cites"].cumsum().to_numpy()
total = cum[-1] if len(cum) else 0
third = total / 3 if total else 0

def zone_end(thr):
    if total == 0:
        return 0
    return int((cum >= thr).argmax() + 1) if any(cum >= thr) else len(cum)

z1 = zone_end(third)
z2 = zone_end(2 * third)
z3 = len(src_df)

# Expected Bradford multiplier = k where zone counts go ~ n0, n0*k, n0*k^2
# Empirical ks
def safe_div(a, b):
    return a / b if b else float("inf")

k1 = safe_div(z2 - z1, max(1, z1))
k2 = safe_div(z3 - z2, max(1, z2 - z1))

zones = {
    "zone1_nucleus": int(z1),
    "zone2_middle": int(z2 - z1),
    "zone3_periphery": int(z3 - z2),
    "zone1_cites": int(cum[z1 - 1]) if z1 > 0 else 0,
    "zone2_cites": int(cum[z2 - 1] - cum[z1 - 1]) if z2 > z1 else 0,
    "zone3_cites": int(cum[-1] - cum[z2 - 1]) if len(cum) and z2 > 0 else 0,
    "bradford_k_empirical": [round(k1, 2), round(k2, 2)],
    "total_citations": int(total),
    "total_unique_sources": int(len(src_df)),
}

# --------- Plot ---------
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

# Left: Bradford curve (log rank vs cumulative cites)
ranks = src_df["rank"].to_numpy()
ax[0].plot(ranks, cum, "b-")
ax[0].axvline(z1, color="g", ls="--", label=f"Zona 1 ({z1} revistas)")
ax[0].axvline(z2, color="orange", ls="--", label=f"Zona 2 ({z2-z1} revistas)")
ax[0].set_xscale("log")
ax[0].set_xlabel("Rango de revista (log)")
ax[0].set_ylabel("Citas acumuladas")
ax[0].set_title(f"Ley de Bradford — NCML (n={total} citas, {len(src_df)} fuentes)")
ax[0].legend()
ax[0].grid(True, which="both", alpha=0.3)

# Right: top 20 sources
top20 = src_df.head(20).iloc[::-1]
ax[1].barh(range(len(top20)), top20["cites"])
ax[1].set_yticks(range(len(top20)))
ax[1].set_yticklabels([s[:55] for s in top20["source"]], fontsize=8)
ax[1].set_xlabel("Citas")
ax[1].set_title("Top 20 fuentes citadas")
ax[1].grid(True, axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig(REP / "bradford.png", dpi=150)
plt.close()

(REP / "bradford_zones.json").write_text(json.dumps(zones, indent=2))

# Summary markdown
md = [
    "# Ley de Bradford — NCML",
    "",
    f"**Referencias totales extraidas:** {n_refs_total}",
    f"**Con revista detectada:** {n_refs_with_journal} ({n_refs_with_journal/max(1,n_refs_total):.1%})",
    f"**Fuentes unicas detectadas:** {len(src_df)}",
    "",
    "Nota metodologica: extraccion heuristica (regex) sobre texto plano. ",
    "Las referencias a libros, tesis, paginas web y actas no se consideran ",
    "revistas y quedan fuera. Cobertura limitada vs GROBID; trabajo pendiente.",
    "",
    "## Zonas de Bradford (particion por tercios de citas)",
    "",
    f"- **Zona 1 (nucleo):** {zones['zone1_nucleus']} revistas concentran {zones['zone1_cites']} citas (~1/3)",
    f"- **Zona 2 (media):** {zones['zone2_middle']} revistas concentran {zones['zone2_cites']} citas",
    f"- **Zona 3 (periferia):** {zones['zone3_periphery']} revistas concentran {zones['zone3_cites']} citas",
    "",
    f"Multiplicador Bradford empirico entre zonas: **{zones['bradford_k_empirical']}**",
    f"(Bradford clasica predice un unico k constante; valores muy distintos indican desviacion).",
    "",
    "## Top 10 fuentes citadas",
    "",
    "| Rank | Fuente | Citas |",
    "|---|---|---|",
]
for _, r in src_df.head(10).iterrows():
    md.append(f"| {int(r['rank'])} | {r['source'][:80]} | {int(r['cites'])} |")
md.append("")
md.append("![Bradford curva + top 20](bradford.png)")
(REP / "bradford.md").write_text("\n".join(md), encoding="utf-8")

print("\n=== Top 15 ===")
for _, r in src_df.head(15).iterrows():
    print(f"  {int(r['rank']):>3}. {r['source'][:70]:<70}  {int(r['cites'])} cites")

print(f"\nOutput: {REP / 'bradford.md'}, {REP / 'bradford_sources.csv'}")
