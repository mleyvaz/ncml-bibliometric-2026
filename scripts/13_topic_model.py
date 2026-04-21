"""Topic modeling on NCML abstracts.

Pipeline (BERTopic-style, built from components to avoid Python 3.14 / hdbscan
wheel issue):
  1. Load abstracts: Spanish preferred, English fallback.
  2. Multilingual sentence embeddings (paraphrase-multilingual-MiniLM-L12-v2).
  3. UMAP dimensionality reduction -> 5D.
  4. KMeans clustering; k selected by silhouette over a reasonable range.
  5. c-TF-IDF style topic term extraction.

Outputs:
  data/topics_docs.csv          doc-to-topic assignment with metadata
  data/topics_labels.csv        topic id -> top terms
  reports/clean/topics_umap.png 2D UMAP scatter colored by topic
  reports/clean/topics.md       narrative summary
"""
from __future__ import annotations
import sys
import re
import json
import unicodedata
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
EXT = ROOT / "data" / "pdf_extract.csv"
WORKS = ROOT / "data" / "works.csv"
OUT = ROOT / "data"
REP = ROOT / "reports" / "clean"
REP.mkdir(exist_ok=True, parents=True)

# -------- Load + choose text --------
ext = pd.read_csv(EXT)
works = pd.read_csv(WORKS)

def pick_text(row):
    es = str(row.get("resumen") or "").strip()
    en = str(row.get("abstract") or "").strip()
    # Prefer longer of the two (both present when bilingual); fallback to whichever exists
    if len(es) >= 200 and len(en) >= 200:
        return es + "\n\n" + en  # both improve signal
    if len(es) >= 100:
        return es
    if len(en) >= 100:
        return en
    return ""

ext["text"] = ext.apply(pick_text, axis=1)
# Merge with works (year, volume, DOI)
ext["doi_stub"] = ext["doi_stub"].astype(str)
works["doi_stub"] = works["doi"].fillna("").astype(str).str.replace("/", "_").str.replace(":", "_")
df = ext.merge(works[["doi_stub", "doi", "volume", "year", "title_local"]], on="doi_stub", how="left")

docs_df = df[df["text"].str.len() >= 100].copy().reset_index(drop=True)
print(f"Documents with usable abstract: {len(docs_df)} / {len(df)}")

# -------- Embeddings --------
from sentence_transformers import SentenceTransformer
print("Loading multilingual sentence model (first run downloads ~120 MB)...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
print("Encoding...")
emb = model.encode(docs_df["text"].tolist(), batch_size=64, show_progress_bar=True, convert_to_numpy=True)
print(f"Embeddings: {emb.shape}")

# -------- UMAP reduction --------
import umap
umap5 = umap.UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=42)
emb_5d = umap5.fit_transform(emb)
umap2 = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.1, metric="cosine", random_state=42)
emb_2d = umap2.fit_transform(emb)

# -------- Choose k by silhouette --------
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
k_candidates = list(range(10, 26))
scores = []
for k in k_candidates:
    km = KMeans(n_clusters=k, n_init=5, random_state=42).fit(emb_5d)
    s = silhouette_score(emb_5d, km.labels_, sample_size=min(len(emb_5d), 2000), random_state=42)
    scores.append(s)
    print(f"  k={k}  silhouette={s:.3f}")
best_k = k_candidates[int(np.argmax(scores))]
print(f"Best k = {best_k} (silhouette {max(scores):.3f})")

km = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit(emb_5d)
docs_df["topic"] = km.labels_

# -------- c-TF-IDF topic terms (sklearn-based) --------
# Build Spanish+English stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def preprocess(t: str) -> str:
    t = strip_accents(t).lower()
    t = re.sub(r"[^a-z\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

docs_df["text_clean"] = docs_df["text"].map(preprocess)

STOP_ES = set("""
el la los las un una unos unas y o u de del al a en con sin por para
es son esta estan este estas estos esa ese eso esta esas esos
que como cual cuales cuyo cuya cuyos cuyas si no ni tambien tampoco
su sus mi mis tu tus nuestro vuestra lo se lo les le
pero aunque porque ya aun mas menos muy poco mucho algun alguna algunos
entre sobre bajo ante hacia hasta desde tras segun mediante durante
ser estar tener haber hacer hay han ha fue era eran sera
articulo autor autores
""".split())
STOP_EN = set("""the a an and or of for with in on at to from by as is are was were be been being
this that these those it its they them their there here we our you your he she his her i me my
not no nor but however while because since whether without within into upon which who whom
also such more most less less than can may might must should would could do does did done doing
study research method results findings paper article abstract introduction conclusion
""".split())
# Domain-specific generic terms to suppress (still too dominant)
STOP_DOMAIN = set("""
neutrosofico neutrosofica neutrosoficas neutrosoficos neutrosofia metodo metodos
multicriterio analisis evaluacion evaluar evaluacion caso estudio sobre trabajo
aplicacion presente investigacion resultado resultados conclusion
resumen abstract keywords palabras clave
neutrosophic fuzzy analysis assessment method model case study paper
""".split())
STOPS = STOP_ES | STOP_EN | STOP_DOMAIN

# Build per-topic concatenated corpus (c-TF-IDF)
docs_per_topic = docs_df.groupby("topic")["text_clean"].apply(lambda s: " ".join(s)).reset_index()

cv = CountVectorizer(ngram_range=(1, 2), min_df=2, stop_words=list(STOPS), token_pattern=r"[a-z]{4,}")
counts = cv.fit_transform(docs_per_topic["text_clean"])
tfidf = TfidfTransformer().fit_transform(counts)
features = np.array(cv.get_feature_names_out())

topic_terms = {}
for i, tid in enumerate(docs_per_topic["topic"].tolist()):
    row = tfidf[i].toarray().ravel()
    top_idx = row.argsort()[-12:][::-1]
    topic_terms[int(tid)] = features[top_idx].tolist()

# Topic size
topic_size = docs_df["topic"].value_counts().sort_index().to_dict()

# Persist outputs
labels_df = pd.DataFrame([
    {"topic": t, "size": topic_size.get(t, 0), "top_terms": ", ".join(topic_terms.get(t, []))}
    for t in sorted(topic_terms)
]).sort_values("size", ascending=False)
labels_df.to_csv(OUT / "topics_labels.csv", index=False, encoding="utf-8")

docs_out = docs_df[["doi", "volume", "year", "title_local", "topic"]].copy()
docs_out["umap_x"] = emb_2d[:, 0]
docs_out["umap_y"] = emb_2d[:, 1]
docs_out.to_csv(OUT / "topics_docs.csv", index=False, encoding="utf-8")

# -------- Plot: 2D UMAP colored by topic --------
plt.figure(figsize=(11, 8))
cmap = plt.get_cmap("tab20", best_k)
for t in range(best_k):
    mask = km.labels_ == t
    if mask.sum() == 0:
        continue
    plt.scatter(emb_2d[mask, 0], emb_2d[mask, 1], s=12, alpha=0.6, color=cmap(t),
                label=f"T{t}: {topic_terms.get(t, [''])[0]}"[:45])
plt.legend(loc="lower left", bbox_to_anchor=(1.01, 0), fontsize=8)
plt.title(f"UMAP + KMeans (k={best_k}) — NCML {len(docs_df)} articulos")
plt.xlabel("UMAP-1"); plt.ylabel("UMAP-2")
plt.tight_layout()
plt.savefig(REP / "topics_umap.png", dpi=150, bbox_inches="tight")
plt.close()

# -------- Summary --------
md = [f"# Topic modeling — NCML ({len(docs_df)} articulos)", "",
      f"- Modelo embeddings: paraphrase-multilingual-MiniLM-L12-v2",
      f"- Reduccion: UMAP 5D (neighbors=15, cosine)",
      f"- Clustering: KMeans k={best_k} (seleccionado por silhouette={max(scores):.3f} sobre k∈[{min(k_candidates)},{max(k_candidates)}])",
      "",
      "## Topicos (ordenados por tamano)", "",
      "| ID | Tamano | Terminos top |", "|---|---|---|"]
for _, r in labels_df.iterrows():
    md.append(f"| T{int(r['topic'])} | {int(r['size'])} | {r['top_terms']} |")
md.append("")
md.append("![UMAP topics](topics_umap.png)")
(REP / "topics.md").write_text("\n".join(md), encoding="utf-8")

print(f"\nTopics: {best_k}")
print(f"Avg cluster size: {len(docs_df)/best_k:.1f}")
print("\nTop 5 topics:")
for _, r in labels_df.head(5).iterrows():
    print(f"  T{int(r['topic'])} ({int(r['size'])} docs): {r['top_terms'][:120]}")
print(f"\nWritten: {REP / 'topics.md'} ; {OUT / 'topics_docs.csv'} ; {OUT / 'topics_labels.csv'}")
