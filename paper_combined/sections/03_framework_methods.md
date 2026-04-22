# 2. Theoretical Background

## 2.1 Neutrosophic logic and single-valued neutrosophic numbers

Neutrosophic logic [4, 5] generalises fuzzy logic by introducing a
separate indeterminacy component. A neutrosophic value is a triple
(T, I, F) where T is the degree of truth, I the degree of
indeterminacy, and F the degree of falsity, each in [0, 1]. Unlike
intuitionistic fuzzy logic, the three components are independent: the
constraint 0 ≤ T + I + F ≤ 3 holds, but no equality is imposed. A
*single-valued neutrosophic number* (SVN) is a particular case where
T, I, and F are explicit real numbers in [0, 1] [6]. SVNs admit
standard algebraic operations (addition, multiplication, scalar
multiplication) and several aggregation operators formalised for
multi-criteria decision-making [7, 11].

We adopt the following notational convention. Given a population P of
items and a property Q, the *neutrosophic membership profile* of P with
respect to Q is the triple

  N_Q(P) = ( T_Q, I_Q, F_Q )                                   (1)

where T_Q is the proportion of items for which Q is verified by direct
positive evidence, I_Q is the proportion for which the evidence is
ambiguous, and F_Q is the proportion for which Q is contradicted by
explicit negative evidence.

## 2.2 Why neutrosophy fits bibliometric measurement

Three structural features of bibliographic data make neutrosophic
treatment a natural rather than ornamental choice. First, *multiple
partially-overlapping sources of evidence* (Crossref, Scopus,
OpenAlex, Google Scholar, DataCite, Dimensions) disagree
systematically, and the disagreement reflects genuine differences in
scope rather than measurement noise. Second, *soft assignments
produced by clustering* (UMAP + KMeans, BERTopic) yield probabilistic
memberships that are routinely discarded by winner-take-all
reporting. Third, *asymmetric availability of negative evidence*:
confirming that an article was *not* cited requires exhaustive
coverage that no single database provides. The (T, F, I) triple
naturally captures this asymmetry: F reports the share of items where
every consulted source agrees on absence, while I reports the share
where coverage is insufficient to conclude.

This motivates the central methodological commitment of this paper:
the indeterminacy component is *computed from the data*, not elicited
from experts via linguistic scales. This distinguishes the framework
from the family of neutrosophic AHP-TOPSIS papers where (T, I, F) are
human judgements [7, 17] — and responds directly to the Woodall et
al. (2025) concern that the choice of three components is seldom
justified by the data structure [18].

## 2.3 Classical bibliometric indicators recalled

**The h-index** [19]. Given a set of articles with citation counts
sorted non-increasing, h is the largest integer such that c_h ≥ h. The
journal-level h5-index is h restricted to articles published in the
past five years.

**Lotka's law** [14]. The number of authors n(x) producing exactly x
publications follows n(x) ∝ x^(-α) with classical α ≈ 2. The exponent
is fitted by maximum likelihood [15, eq. 3.1] and goodness-of-fit is
evaluated with the Kolmogorov-Smirnov statistic against 1.36/√N at 5%.

**Bradford's law** [20]. When journals are ranked by descending number
of citations received and the cumulative count is partitioned into
three zones of equal citations, the counts follow a geometric
progression: |Z_2| ≈ k · |Z_1|, |Z_3| ≈ k · |Z_2| for a Bradford
multiplier k typically in [3, 5] for mature fields.

**Topic modeling.** Soft clustering (LDA, BERTopic, KMeans on
embeddings) assigns each document a distribution over topics;
bibliometric studies classically report the *winner*.

**Co-authorship networks.** Authors are nodes; an edge's weight is the
count of shared articles. Centrality, community detection [16], and
modularity are computed on the weighted graph, treating raw counts as
if they conveyed only one kind of information.

# 3. The Neutrosophic Bibliometric Framework and Pipeline

## 3.1 Corpus and data pipeline

The empirical corpus consists of the 762 articles published by NCML in
volumes 1 through 42 (2018 to April 2026). Article-level metadata
(title, authors, volume, year, pages, DOI) were scraped from the
official journal index at `https://fs.unm.edu/NCML/Articles.htm` on
19 April 2026, and enriched through OpenAlex (671 articles, 93.3%),
DataCite (704 articles, 97.9%), and — for the journal-aggregate
measures — Google Scholar Metrics. Full-text PDFs were retrieved for
728 of 762 articles (95.5% coverage; 33 URLs had corrupted encoding
at source). For each PDF we extracted the abstract (Spanish resumen,
91.5% extraction rate; English abstract, 41%), the keyword list
(94%), the email addresses (99%) and the references block (95%).

The 2 225 author-article pairs were disambiguated into 1 363 unique
authors using a union-find algorithm with four hierarchical
equivalence rules in decreasing order of strength: (i) shared ORCID;
(ii) shared OpenAlex author identifier; (iii) shared canonical name
(NFKD-normalised, lowercased, stop-token removed, alphabetised); (iv)
initial-plus-surname key when no ORCID conflict exists. The
disambiguation reduced 1 539 raw signatures by 9.9%. The top 100
clusters were inspected manually; no false merges were detected.

The full pipeline is implemented in Python 3.14 with twenty numbered
scripts (01–20 plus helpers); the source code, intermediate data
(CSV/JSONL), figures, and SHA-256 checksums are published at
https://github.com/mleyvaz/ncml-bibliometric-2026 (code under MIT,
data under CC-BY 4.0). The pipeline is idempotent and reproducible
end-to-end in approximately 30 minutes on a modern laptop.

## 3.2 Neutrosophic extensions of classical indicators

The following five extensions apply the (T, I, F) triple to each
classical indicator of Section 2.3. In each case, the classical
indicator is recovered by collapsing the indeterminacy component,
so the framework is strictly informationally richer than the
classical baseline.

### 3.2.1 Neutrosophic *h*-index

For each article a_i with citation counts c_i^{(k)} from K
independent sources, define the per-article evidence indicator
e_i = |{ k : c_i^{(k)} ≥ 1 }| / K. Articles are classified as T-class
(e_i = 1), I-class (0 < e_i < 1), or F-class (e_i = 0). The
*neutrosophic h-index profile* of the journal is the triple
N_h(J) = (h_T, h_I, h_F) where h_T is the h-index over T-class
articles and h_I is the h-index over T-class + I-class articles. The
classical h-index is recovered by the most-comprehensive-source
choice.

### 3.2.2 Neutrosophic Lotka exponent

Let {x_1, …, x_N} be the productivity counts. For b = 1, …, B,
bootstrap-resample with replacement and compute the MLE α̂_b and the
K-S statistic D_b. The neutrosophic Lotka profile is

  T = |{b: α̂_b ∈ [1.9, 2.1] AND D_b ≤ D_crit}| / B             (2)
  I = |{b: α̂_b ∈ [1.9, 2.1] AND D_b > D_crit}| / B
  F = |{b: α̂_b ∉ [1.9, 2.1]}| / B

with D_crit = 1.36/√N. We use B = 1 000 and fixed random state 42.

### 3.2.3 Neutrosophic Bradford zone membership

The crisp Bradford partition is replaced with graded nucleus
membership. For a journal with citation share s_j, let s* be the
share at which the cumulative reaches 1/3 (classical nucleus
boundary) and κ = 0.4 · s* a smoothing constant. Then

  T_nuc(j) = σ( (s_j − s*) / κ )                               (3)
  I_nuc(j) = 0.4 · exp( −(s_j − s*)² / (2 · (1.5κ)²) )         (4)
  F_nuc(j) = max( 0, 1 − T_nuc(j) − I_nuc(j) )                 (5)

where σ is the logistic function. Equation (4) creates an
indeterminacy peak at the boundary.

### 3.2.4 Neutrosophic topic membership

Let d_i be the Euclidean distance from document i to its assigned
cluster centroid, d_i' the distance to the nearest other cluster,
and σ̂ the median of {d_i} over the corpus. Then

  T_topic(i) = exp( −d_i² / (2 σ̂²) )                           (6)
  I_topic(i) = 0.5 · exp( −(d_i' − d_i)² / (2 (0.5 σ̂)²) )     (7)
  F_topic(i) = max( 0, 1 − T_topic(i) − I_topic(i) )           (8)

### 3.2.5 Neutrosophic co-authorship edge weight

For an edge (u, v) with w shared articles,

  T_collab(u, v) = 1 − exp( −(w − 1) / 2 )                     (9)
  I_collab(u, v) = 𝟙{w=1} · 0.5 + 𝟙{w>1} · 0.5 exp(−(w−1)/1.5) (10)
  F_collab(u, v) = max( 0, 1 − T_collab(u, v) − I_collab(u, v)) (11)

T saturates for verified collaboration; I peaks at w = 1
(single-article, possibly opportunistic); F is the residual.

## 3.3 Neutrosophic aggregation (SVNWA)

Aggregation of the per-indicator triples is performed with the
Single-Valued Neutrosophic Weighted Arithmetic operator of Ye [11]:

  SVNWA( (T_j, I_j, F_j); w_j ) =                              (12)
     ( 1 − ∏_j (1 − T_j)^{w_j},  ∏_j I_j^{w_j},  ∏_j F_j^{w_j} )

Score function (Smarandache) maps the aggregate to [0, 1]:

  S(T, I, F) = (2 + T − I − F) / 3                             (13)

## 3.4 Implementation and computational environment

All computations run on a single laptop (16 GB RAM) with Python 3.14,
pandas, numpy, scipy, scikit-learn, sentence-transformers, umap-learn,
networkx, python-louvain, matplotlib, and python-docx. Topic modeling
uses the multilingual embeddings *paraphrase-multilingual-MiniLM-L12-v2*
[22] reduced to 5D by UMAP [23] and clustered with KMeans; the number
of clusters K = 24 was selected by silhouette score (= 0.43) over
K ∈ [10, 25]. Bootstrap resampling for the neutrosophic Lotka (B = 1 000)
uses fixed random state 42. The composite pipeline is documented in
twenty numbered scripts (01–20 and neutrosophic extensions 27–29).
