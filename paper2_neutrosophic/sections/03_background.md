# 2. Background

## 2.1 Neutrosophic logic and single-valued neutrosophic numbers

Neutrosophic logic [3, 4] generalises fuzzy logic by introducing a separate
indeterminacy component. A neutrosophic value is a triple (T, I, F) where T
is the degree of truth, I is the degree of indeterminacy, and F is the
degree of falsity, each in the closed interval [0, 1]. Unlike intuitionistic
fuzzy logic, the components are independent: the constraint
0 ≤ T + I + F ≤ 3 holds, but no equality is imposed.

A *single-valued neutrosophic number* (SVN) is a particular case where T, I
and F are explicit real numbers in [0, 1] [5]. SVNs admit standard
algebraic operations including addition, multiplication, scalar
multiplication, and several aggregation operators (weighted arithmetic,
weighted geometric, ordered weighted averaging) that have been formalised
for the multi-criteria decision-making context [6, 11]. For the present
work we use the SVN form throughout.

We adopt the following notational convention. Given a population P of
items and a property Q (e.g., "journal X is in the Bradford nucleus", "the
journal follows Lotka's law", "this article belongs to topic T_k"), the
*neutrosophic membership profile* of P with respect to Q is the triple

  N_Q(P) = ( T_Q, I_Q, F_Q )                                  (1)

where T_Q is the proportion of items for which Q is verified by direct
positive evidence, I_Q is the proportion for which the evidence is
ambiguous, and F_Q is the proportion for which Q is contradicted by
explicit negative evidence. The three sum to one when the evidence
classification is exhaustive; in cases where multiple sources of evidence
exist, the components are computed independently and the sum may exceed or
fall below one, capturing redundancy or coverage gaps respectively.

## 2.2 Classical bibliometric indicators

For each indicator we extend in Section 3 we briefly recall its classical
form.

**The h-index** [12]. Given a set of articles with citation counts
{c_1, c_2, …, c_n} sorted in non-increasing order, the h-index is the
largest integer h such that c_h ≥ h. The journal-level h5-index is the
h-index restricted to articles published in the past five years. Both are
sensitive to the citation source: the same publication universe yields
different values depending on whether one counts in OpenAlex, Scopus, Web
of Science, or Google Scholar [1, 2].

**Lotka's law** [13]. The number of authors n(x) producing exactly x
publications follows a power-law distribution

  n(x) = C · x^(-α)                                            (2)

with classical exponent α ≈ 2. The exponent is fitted by maximum
likelihood [14, eq. 3.1] and the goodness-of-fit is evaluated with the
Kolmogorov–Smirnov statistic D = max_x |F_emp(x) - F_th(x)| against the
critical value 1.36/√N at the 5 % significance level.

**Bradford's law** [15]. When journals are ranked by descending number of
references received and the cumulative count is partitioned into three
zones of equal citations, the number of journals per zone follows a
geometric progression: |Z_2| ≈ k · |Z_1|, |Z_3| ≈ k · |Z_2| for a
constant Bradford multiplier k typically in the range [3, 5] for mature
fields. The zones are conventionally labelled "nucleus", "middle", and
"periphery". Boundary journals are assigned to a single zone by hard
threshold.

**Topic modeling**. Soft-clustering algorithms (LDA, BERTopic, KMeans on
embeddings) assign each document a probability distribution over topics.
Bibliometric studies typically report the *winner-take-all* assignment:
each document is reduced to its most probable topic. This discards
information about documents that fall on the boundary between two or more
topics.

**Co-authorship networks**. Authors are nodes; an edge between two
authors carries a weight equal to the number of articles they co-author.
Centrality, community detection (e.g., Louvain [16]), and modularity are
then computed on this weighted graph. The classical formulation does not
distinguish between an edge of weight 1 (a single shared paper) and an
edge of weight 5 (five shared papers); both contribute to the same
community-detection algorithm with weight proportional to count, but the
qualitative distinction (verified collaboration vs. opportunistic
co-authorship) is lost.

## 2.3 Why neutrosophy is well-suited to bibliometric measurement

Three structural features of bibliometric data make neutrosophic
treatment a natural choice rather than an ornamental one.

1. **Multiple, partially overlapping sources of evidence**. Citation
   counts, author identifiers, and journal coverage are each available
   from several databases (Crossref, Scopus, OpenAlex, Google Scholar,
   DataCite, Dimensions). The sources disagree systematically. The
   disagreement is not noise: it reflects genuine differences in scope
   and indexing policy. Neutrosophy captures the disagreement as I; fuzzy
   logic and probability would either smooth it away or attribute it to
   the analyst's subjective uncertainty.
2. **Soft assignments produced by clustering**. UMAP + KMeans, BERTopic,
   and other modern topic-modeling pipelines produce probabilistic
   assignments. Reporting the winner discards measurable information.
3. **Asymmetric availability of negative evidence**. Confirming that an
   article was cited is straightforward; confirming that it was *not*
   cited requires exhaustive coverage that no single database provides.
   The truth-falsity asymmetry is naturally accommodated by the (T, F, I)
   triple: F reports the share of items where every consulted source
   agrees on absence, while I reports the share where coverage is
   insufficient to conclude.

For these reasons we propose a framework in which the indeterminacy
component is computed *from the data*, not assumed by the analyst. This
distinguishes our work from the family of neutrosophic AHP-TOPSIS papers
in which the (T, I, F) triples are elicited from human experts via
linguistic scales [6, 8, 17]. In our framework, indeterminacy is an
emergent property of the bibliographic data structure.
