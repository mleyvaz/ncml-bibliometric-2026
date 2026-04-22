# 3. The Neutrosophic Bibliometric Framework

We now present the five neutrosophic extensions of classical indicators.
For each one we provide the formal definition, the computation rule, and
the interpretation of the resulting (T, I, F) triple.

## 3.1 Neutrosophic h-index

The classical h-index assumes a single citation source. The
*neutrosophic h-index* triangulates K independent sources S_1, …, S_K and
classifies each article a_i according to the agreement among its citation
counts c_i^{(k)}. Define the per-article evidence indicator:

  e_i = | { k : c_i^{(k)} >= 1 } | / K                       (3)

Three classes follow:

- *Verified positive* (T-class): e_i = 1, all sources report a citation.
- *Indeterminate* (I-class): 0 < e_i < 1, sources disagree.
- *Verified negative* (F-class): e_i = 0, no source reports a citation.

The *neutrosophic h-index profile* of the journal is the triple

  N_h(J) = ( h_T, h_I, h_F )                                  (4)

where h_T is the h-index restricted to T-class articles, h_I is the
h-index obtained by including I-class articles in addition to T-class
ones, and h_F = 0 by construction. Equivalently, the upper bound of the
journal's h-index is given by the union of all sources, and the lower
bound by the intersection. The neutrosophic h-index reports both,
together with the journal-level *evidence membership* (T, I, F)
proportions.

Operationally, when only one comprehensive source is available
(e.g., Google Scholar Metrics provides h5 directly), we anchor the
upper-bound on that source and the lower-bound on the most conservative
indexed source.

## 3.2 Neutrosophic Lotka exponent

The classical Lotka fit produces a point estimate α̂ and a K-S test of
shape adequacy. We replace this binary outcome with a neutrosophic
profile based on the *bootstrap distribution* of the exponent.

Let {x_1, …, x_N} be the productivity counts (articles per author). For
b = 1, …, B, draw a bootstrap sample of size N with replacement and
compute the maximum-likelihood exponent α̂_b and the K-S statistic D_b.
The neutrosophic profile of the journal with respect to "follows
classical Lotka" is

  N_Lotka(J) = ( T, I, F )                                    (5)

with:

- T = (1/B) · Σ_b 𝟙{ α̂_b ∈ [1.9, 2.1] AND D_b ≤ D_crit }
- I = (1/B) · Σ_b 𝟙{ α̂_b ∈ [1.9, 2.1] AND D_b > D_crit }
- F = (1/B) · Σ_b 𝟙{ α̂_b ∉ [1.9, 2.1] }

where D_crit = 1.36/√N is the K-S critical value at the 5 % level. T
captures the proportion of bootstrap replicates that confirm Lotka's law
in both exponent and shape; I captures replicates whose exponent matches
classical Lotka but whose shape diverges (typically because of an excess
of one-shot authors); F captures replicates that fall outside the
classical exponent range.

The number of replicates B = 1000 is sufficient for stable membership
estimates. Larger B reduces sampling variance in T, I, F to negligible
levels but does not change qualitative conclusions.

## 3.3 Neutrosophic Bradford zone membership

Classical Bradford partitions journals into three crisp zones by
cumulative citation share. For boundary journals this is artificial. We
define the *neutrosophic nucleus membership* of a journal j with citation
share s_j ∈ [0, 1] as

  T_nuc(j) = σ( (s_j - s*) / κ )                              (6)
  I_nuc(j) = 0.4 · exp( -(s_j - s*)² / (2 · (1.5 κ)²) )       (7)
  F_nuc(j) = max( 0, 1 - T_nuc(j) - I_nuc(j) )                (8)

where σ is the logistic function, s* is the citation share at which the
cumulative reaches one third of the total (the classical nucleus
boundary), and κ is a smoothing constant set to 0.4 · s*. Equation (6)
yields high T for journals well above the boundary and low T for
journals well below. Equation (7) introduces an indeterminacy peak
centred on the boundary, modelling the fuzziness of zone assignment for
journals near the threshold. Equation (8) ensures that F is non-negative
and that the triple is internally consistent.

The same approach applies to membership in zone 2 (middle) and zone 3
(periphery) by repeating the procedure with the corresponding boundary.
Reporting only the nucleus membership is sufficient for most editorial
purposes, since zone-1 journals are the ones whose dependence is
strategically relevant.

## 3.4 Neutrosophic topic membership

Modern topic-modeling pipelines produce probabilistic document–topic
assignments. We map the soft assignment to a neutrosophic profile. Let
d_i be the Euclidean distance from document i to the centroid of its
assigned cluster, and d_i' the distance to the nearest other cluster.
Let σ̂ be the median of {d_i} over the corpus. The membership of
document i in its assigned topic is

  T_topic(i) = exp( -d_i² / (2 σ̂²) )                          (9)
  I_topic(i) = 0.5 · exp( -(d_i' - d_i)² / (2 (0.5 σ̂)²) )    (10)
  F_topic(i) = max( 0, 1 - T_topic(i) - I_topic(i) )          (11)

T captures the closeness of the document to its assigned centroid (high
T = clearly inside the cluster). I captures the proximity of the second
nearest cluster (high I = boundary between two topics). F is the
residual.

The same scheme applies to LDA, BERTopic, or any other clustering
pipeline once a per-document distance to assigned and second-nearest
centroids is available. For BERTopic specifically, the topic-probability
distribution returned by the model can be used directly: T = max
probability, I = second-highest probability, F = 1 − T − I.

## 3.5 Neutrosophic co-authorship edge weights

Classical co-authorship networks weight each edge by the count of shared
articles. We propose

  T_collab(u, v) = 1 - exp( -(w_{u,v} - 1) / 2 )             (12)
  I_collab(u, v) = 𝟙{w_{u,v}=1} · 0.5  +
                   𝟙{w_{u,v}>1} · 0.5 · exp( -(w_{u,v}-1)/1.5 )   (13)
  F_collab(u, v) = max( 0, 1 - T_collab(u, v) - I_collab(u, v) )   (14)

where w_{u,v} is the number of articles co-authored by u and v. T
saturates as w grows (verified collaboration), I peaks at w = 1
(single-article collaboration, which may be opportunistic) and decays
afterwards. F is the residual.

Network-level metrics (modularity, clustering coefficient, degree
centrality) can then be computed using T_collab as the edge weight, with
the I_collab and F_collab triples available for sensitivity analysis. A
collaboration network that survives strong T-thresholding (e.g.,
T > 0.5) reveals the *intellectual core* of the journal as opposed to
the *publication marketplace* shown by the classical raw-count graph.

## 3.6 Aggregation

The five indicators are independent. They can be reported jointly as a
*neutrosophic bibliometric vector*

  N(J) = ( N_h, N_Lotka, N_Bradford-Z1, N_topics, N_coauth )  (15)

with each component a (T, I, F) triple. For an editorial audience we
recommend reporting all five with their indeterminacy components rather
than a single scalar score. Aggregating into a single number requires a
weighting scheme (e.g., neutrosophic AHP) and is left for case-specific
applications.
