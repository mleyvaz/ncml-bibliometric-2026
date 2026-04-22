# 4. Methods and Data

## 4.1 Corpus

The empirical case study uses the corpus of *Neutrosophic Computing and
Machine Learning* (NCML) compiled in our companion paper [10]. The
corpus comprises 762 articles published in volumes 1 through 42 (2018 to
April 2026), of which 728 PDFs were successfully retrieved (95.5 %
coverage). Article-level metadata (title, authors, volume, year, pages,
DOI) were scraped from the official journal index and enriched through
the OpenAlex (671 articles, 93.3 %) and DataCite (704 articles, 97.9 %)
APIs.

## 4.2 Author disambiguation

The 2 225 author–article pairs were resolved into 1 363 unique authors
using a union-find algorithm with four hierarchical equivalence rules:
(i) shared ORCID; (ii) shared OpenAlex author identifier; (iii) shared
canonical name (NFKD-normalised, lowercased, stop-token removed,
alphabetised); (iv) initial-plus-surname key when no ORCID conflict
exists. The disambiguation reduced 1 539 raw signatures by 9.9 %. The
top 100 clusters were inspected manually; no false merges were detected.

## 4.3 Citation triangulation

For each article, citation counts were obtained from up to three
sources: OpenAlex (full corpus), Google Scholar (a stratified sample of
n = 26, with 3 articles per year between 2018 and 2024 plus the most
cited OpenAlex article and 5 articles from 2025), and DataCite (full
corpus, where DataCite tracks citations among DataCite-registered DOIs
only). Source-disagreement is computed at the article level using the
classification rule of Section 3.1.

## 4.4 Topic modeling

The 725 articles with usable abstracts (≥ 100 characters in either the
Spanish resumen or the English abstract) were embedded with the
multilingual *paraphrase-multilingual-MiniLM-L12-v2* sentence transformer
(384 dimensions) [18]. The embeddings were reduced to five dimensions
with UMAP [19] (n_neighbors = 15, min_dist = 0.0, cosine metric, fixed
random state) and clustered with KMeans. The number of clusters K was
selected by silhouette score over K ∈ [10, 25]; the optimal value was
K = 24 with silhouette = 0.43. Topic terms were obtained by class-based
TF-IDF (c-TF-IDF) [20].

For the present paper, the document-to-topic distances required by
equations (9) and (10) were computed from the two-dimensional UMAP
coordinates exported by the original pipeline. This is a conservative
proxy: distances in the lower-dimensional space are slightly compressed
relative to the five-dimensional clustering space. Future work will use
the full 5D distances for sharper separation.

## 4.5 Co-authorship network

The disambiguated authors and their article-level co-occurrences
generated a graph of 1 363 nodes and 2 174 edges (density 0.0023, mean
degree 3.19). Communities were detected with the Louvain algorithm [16]
weighted by raw co-authorship counts.

## 4.6 Computational environment

All computations were implemented in Python 3.14 on a single laptop
with 16 GB of RAM. The pipeline uses pandas, numpy, scipy, scikit-learn,
sentence-transformers, umap-learn, networkx, python-louvain, and
matplotlib for visualisation. The full source code (22 numbered scripts)
is available at https://github.com/mleyvaz/ncml-bibliometric-2026 under
MIT licence; the dataset is published under CC-BY 4.0. Bootstrap
resampling for the neutrosophic Lotka uses B = 1 000 replicates with
fixed random state 42 for reproducibility.

## 4.7 Implementation of the neutrosophic indicators

The five neutrosophic indicators of Section 3 are implemented in
`scripts/27_neutrosophic_indicators.py`. The script reads the cleaned
data tables produced by the classical pipeline (works.csv,
author_clusters.csv, scholar_sample_clean.csv, bradford_sources.csv,
topics_docs.csv, network_edges.csv) and produces:

- `data/neutrosophic_h_index.json` — N-h-index profile (T, I, F).
- `data/neutrosophic_lotka.json` — bootstrap distribution of α and the
  neutrosophic Lotka profile.
- `data/neutrosophic_bradford_top30.csv` — per-journal nucleus
  membership for the top 30 cited journals.
- `data/neutrosophic_topics_docs.csv` — per-document topic membership
  triple.
- `data/neutrosophic_coauth_edges.csv` — per-edge collaboration
  membership triple.
- `figures/neutrosophic_indicators.png` — composite figure with the four
  panels reported in Section 5.

The script terminates in approximately ten seconds on a modern laptop
and is fully deterministic.
