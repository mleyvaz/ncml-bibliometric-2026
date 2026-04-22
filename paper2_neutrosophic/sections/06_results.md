# 5. Case-Study Results

This section reports the empirical application of the five neutrosophic
extensions to the NCML 2018–2026 corpus. Each subsection presents the
classical baseline followed by the neutrosophic profile and a short
interpretation. A composite figure with all four numeric panels is
provided in Figure 1.

## 5.1 Neutrosophic h-index

The classical *h*-index of NCML obtained from OpenAlex is **h = 1** with
27 total citations across 762 articles. The same journal reports an
*h5-index* = 10 with *h5-median* = 25 in Google Scholar Metrics for the
period 2020–2024 [10]. The two values disagree by an order of magnitude.

The neutrosophic *h*-index decomposes the disagreement explicitly. On
the stratified sample of n = 26 articles for which both OpenAlex and
Google Scholar counts are available:

- T-class (cited in both sources): 1 article (3.8 %).
- I-class (cited in only one source): 13 articles (50.0 %).
- F-class (no citation in any source): 12 articles (46.2 %).

The journal-level neutrosophic *h*-index profile is therefore

  N_h(NCML) = ( T = 0.04, I = 0.50, F = 0.46 )

with bounds h_T = 1 (lower bound, OpenAlex-only) and h_TI ≤ h5 = 10
(upper bound, Google Scholar Metrics). The midpoint of the interval is
h ≈ 5.5, which is the value an editorial board should use for
benchmarking under explicit acknowledgement of source uncertainty.

The classical headline number "h = 1" is technically correct but
informationally misleading. The neutrosophic profile reveals that **half
of the articles in the sample are in an evidential limbo**: cited in
some place, not cited in another, and the analyst must choose whether
to count them or not. In the corresponding journal-aggregate evidence,
this is the dominant condition rather than the exception.

## 5.2 Neutrosophic Lotka exponent

The maximum-likelihood fit of Lotka's law on the 1 363 disambiguated
authors yields **α̂ = 2.027** with standard error SE = 0.028 — a value
indistinguishable from the classical Lotka exponent of 2. The K-S
goodness-of-fit test, however, produces D = 0.120 against the critical
value 1.36/√1363 = 0.038, decisively rejecting the null hypothesis of
shape adequacy at the 5 % level.

The bootstrap distribution of α̂ over B = 1 000 replicates has mean 2.03
and 95 % percentile interval [2.00, 2.06]. The K-S statistic is above
critical in all 1 000 replicates. The neutrosophic Lotka profile is

  N_Lotka(NCML) = ( T = 0.00, I = 1.00, F = 0.00 )

The interpretation is that NCML's productivity distribution **matches the
classical Lotka exponent perfectly but its shape diverges in every
bootstrap replicate**. The classical headline "follows Lotka with α =
2.03" is true in the parametric sense and false in the shape sense; the
neutrosophic profile resolves the apparent contradiction by reporting
both. The cause of the shape divergence is identifiable from the
companion paper [10]: an excess of one-shot authors (71.9 % of the
population vs. 61.7 % predicted by the classical model). This is
characteristic of journals that function as a training venue for
graduate students.

## 5.3 Neutrosophic Bradford zone membership

The classical Bradford partition assigns 5 journals to the nucleus, 74
to the middle zone, and 2 260 to the periphery, with multipliers k =
14.8 between zones 1 and 2 and k = 30.5 between zones 2 and 3. The
multipliers far exceed the classical range [3, 5], indicating extreme
concentration. The five nucleus journals are *Neutrosophic Sets and
Systems* (1 047 citations), NCML itself (1 000), *Universidad y Sociedad*
(722), *Serie Cientifica de la Universidad de las Ciencias Informaticas*
(608), and *Revista Conrado* (586).

The neutrosophic nucleus membership of the top ten cited journals
(Table 1) shows that this crisp partition obscures meaningful gradation:

| Rank | Journal | T_nuc | I_nuc | F_nuc |
|---|---|---|---|---|
| 1 | Neutrosophic Sets and Systems | 0.88 | 0.17 | 0.00 |
| 2 | Neutrosophic Computing and Machine Learning | 0.85 | 0.20 | 0.00 |
| 3 | Universidad y Sociedad | 0.64 | 0.37 | 0.00 |
| 4 | Serie Cientifica de la U. de las Ciencias Informaticas | 0.52 | 0.40 | 0.08 |
| 5 | Revista Conrado | 0.50 | 0.40 | 0.10 |
| 6 | Conrado (variant) | 0.35 | 0.42 | 0.23 |
| 7 | International Journal of Neutrosophic Science | 0.28 | 0.41 | 0.31 |
| 8 | Revista de Ciencias Medicas de Pinar del Rio | 0.25 | 0.40 | 0.35 |
| 9 | Revista Cubana de Ciencias Informaticas | 0.24 | 0.39 | 0.37 |
| 10 | Revista Cubana de Informatica Medica | 0.22 | 0.39 | 0.39 |

Two findings emerge that the classical analysis hides. First, the
nucleus is not internally homogeneous: the top two journals (NSS and
NCML, both inside the neutrosophic ecosystem) have T ≥ 0.85 — well
above the boundary — while ranks 3 to 5 (three Cuban journals) sit at
T = 0.50–0.64 with substantial I, indicating they are *boundary
nucleus journals* rather than core members. Second, ranks 6 to 10 have
T ≈ I ≈ F ≈ 0.3, meaning they are not unambiguously inside or outside
the nucleus. An editorial discussion about the journal's citation
ecosystem should therefore distinguish between *strong nucleus* (T >
0.7), *boundary nucleus* (0.4 ≤ T ≤ 0.7), and *peripheral* (T < 0.4)
journals — a tripartite distinction that the crisp Bradford zones
flatten.

## 5.4 Neutrosophic topic membership

The classical topic model identifies 24 topics with silhouette = 0.43
on the 725 documents with usable abstracts. The crisp document–topic
assignment is reported as a hard label per document.

The neutrosophic decomposition of topic membership (Figure 1, panel D)
shows that **only 39 % of documents have T ≥ 0.7** in their assigned
topic. The remaining 61 % distribute as follows: 21 % have moderate T
(0.4 ≤ T < 0.7) and 40 % have T < 0.4 with substantial I, indicating
that they sit on or near a topic boundary. The mean indeterminacy I̅ is
0.13 with standard deviation 0.10; documents with I ≥ 0.3 number 154
(21 %) and represent the topic-boundary cohort.

The editorial interpretation is direct: roughly four out of every ten
articles published in NCML during the period 2018–2026 do not belong
unambiguously to a single topic in the 24-topic model. Topic-based
benchmarking that ignores this fact will systematically misattribute
articles between topics, especially in the legal-medical interface
(topics T0, T9, T17, T20, T22, T23) where the boundaries are
substantively fluid (a paper on legal aspects of medical malpractice
straddles two topics by construction).

## 5.5 Neutrosophic co-authorship edge weights

The classical co-authorship graph has 2 174 edges with a long-tailed
weight distribution: 1 963 edges (90.3 %) have weight w = 1 (single
shared paper); only 211 edges (9.7 %) have w ≥ 2. Modularity computed
on raw weights is 0.96, suggesting a near-perfect community structure.

The neutrosophic edge profile reverses the perspective:

- T_collab ≥ 0.5 (verified collaboration): **40 edges (1.8 %)**.
- I_collab ≥ 0.5 (single collaboration, opportunistic): 1 963 edges
  (90.3 %).
- The remaining edges (171, 7.9 %) have intermediate T-I balance.

A network of *verified* collaborations (T_collab ≥ 0.5) drops the graph
from 1 363 nodes and 2 174 edges to a much smaller subgraph of 35
nodes and 40 edges, dominated by the 4–5 most prolific Ecuadorian
research groups (UNIANDES Riobamba, UBE, UNIANDES Ambato) and the
international group of Smarandache, Leyva, Fujita and a few co-authors.

The classical modularity 0.96 is reduced to 0.81 on the verified
network — still high, but substantially less spectacular. This is
honest: the journal's intellectual integration is measurable on a much
smaller core than the classical graph suggests, and the bulk of the
graph reflects the *publication marketplace* rather than a coherent
community of practice.

## 5.6 Neutrosophic aggregated ranking of authors (operative test)

The five preceding subsections re-expressed classical indicators as
neutrosophic triples and showed that the indeterminacy components
carry non-trivial information. A stronger operative test of the
framework is whether the (T, I, F) triples, once aggregated across
multiple dimensions, **yield a ranking that differs from the classical
ranking and that the differences are interpretable and editorially
actionable**. This subsection reports such a test.

### 5.6.1 Design

We rank the 146 authors with ≥ 3 articles along four neutrosophic
dimensions:

- **D1. N-productivity.** T = sigmoid of article count centred at 8
  articles, I = bell centred at the mid-range (authors with 3–6
  articles), F = residual.
- **D2. N-citational evidence.** Per-article source-triangulation
  class (T = cited in both OpenAlex and Scholar, I = cited in one
  only, F = no citation evidence), averaged across the author's
  publications. For publications outside the Scholar sample, we
  substitute an OpenAlex-only approximation with inflated I.
- **D3. N-co-authorship centrality.** Mean T_collab, I_collab, F_collab
  over the edges touching the author (values from Section 3.5).
- **D4. N-theoretical focus.** Share of the author's articles
  assigned to theory-heavy topics (T7, T16, T2) for T, legal and
  medical applied topics for F, other topics for I.

Aggregation uses the Single-Valued Neutrosophic Weighted Arithmetic
operator SVNWA of Ye [11]:

  SVNWA( (T_j, I_j, F_j); w_j ) =
     ( 1 − ∏_j (1 − T_j)^{w_j}, ∏_j I_j^{w_j}, ∏_j F_j^{w_j} )   (16)

with equal weights w_j = 0.25 across the four dimensions. Authors are
ranked by the score function of Smarandache:

  S(T, I, F) = (2 + T − I − F) / 3                                (17)

which maps the triple to the interval [0, 1]. The classical baseline
is the rank by raw article count.

### 5.6.2 Results

The two rankings differ substantially:

- **Kendall τ = 0.20** (p = 0.001) — weak positive correlation.
- **Spearman ρ = 0.25** (p = 0.003) — same direction, still weak.
- **Top-10 overlap = 5/10** (Jaccard = 0.33) — half of the classical
  top-10 does *not* appear in the neutrosophic top-10.

The authors whose neutrosophic rank is substantially *higher* than
their classical rank share a common profile: small article count
(3–4 publications) but a high share of theoretically-focused papers
(T7, T2, T16) and well-cited by at least one source. Conversely, the
authors whose neutrosophic rank is substantially *lower* than their
classical rank show a different profile: 4–6 publications
predominantly in legal-medical applied topics with low co-authorship
centrality (they publish within a single closed research group) and
no citation evidence in either OpenAlex or Scholar.

Table 2 shows the five largest rises and falls.

| Change | Author | Articles | Rank (classical) | Rank (neutrosophic) |
|---|---|---|---|---|
| ↑ +81 | Lozada Torres, Edwin Fabricio | 3 | 87 | 6 |
| ↑ +78 | Parrales-Bravo, Franklin | 3 | 87 | 9 |
| ↑ +75 | Villalba León, Carlos Luis | 3 | 87 | 17 |
| ↑ +67 | Alvarado, Yelena Abreu | 3 | 87 | 20 |
| ↓ −100 | Romero Fernández, Ariel José | 4 | 52 | 135 |
| ↓ −92  | Cruz Piza, Iyo Alexis | 6 | 20 | 112 |
| ↓ −90  | Troya Terranova, Katherine Tatiana | 5 | 35 | 128 |
| ↓ −90  | Machado Maliza, Mesías Elías | 4 | 52 | 142 |
| ↓ −84  | Chamorro Valencia, Diego Xavier | 5 | 35 | 119 |

The divergence is not a statistical artefact of the bootstrap noise
but a *qualitative re-ordering* of the author base. The editorial
implication is that the classical "authors ranked by article count"
list — which is what NSIA reports in its annual editorial summary —
systematically overvalues authors who publish many papers in a
single topic cluster with no cross-source citation evidence, and
systematically undervalues authors with few but well-positioned
publications.

### 5.6.3 Why this is a genuine neutrosophic finding

Crucially, this re-ordering **cannot be reproduced by any of the
alternative formalisms** without introducing additional structure
equivalent to the (T, I, F) triple:

- *Probabilistic aggregation* of the four dimensions requires a
  likelihood model per dimension, which does not exist for D2, D3 or
  D4 in their natural form.
- *Fuzzy aggregation* collapses I and F into a single non-membership,
  losing the distinction between "no evidence" and "contradictory
  evidence". In D2 this distinction is empirically critical.
- *Intuitionistic fuzzy aggregation* preserves T and F but forces
  T + F ≤ 1, which is violated whenever an author has both
  strong positive evidence in Scholar and strong negative evidence
  in OpenAlex (high-discrepancy case).

Therefore the neutrosophic aggregate exploits precisely the
independence of the three components — the feature that distinguishes
neutrosophy from its predecessors — to produce a measurement that the
predecessors cannot. This is the operative validation that the
framework provides information unreachable by alternative techniques,
not merely an alternative notation.

> **Figure 2.** Rank divergence between the classical article-count
> ranking and the neutrosophic SVNWA ranking over 146 NCML authors
> with ≥ 3 publications. Left panel: scatter of rank positions with
> the identity line as reference; points far from the line indicate
> large divergence. Right panel: top-15 authors by each ranking, side
> by side, showing substantial re-ordering of the journal's visible
> leadership. (Source: `ranking_comparison.png`.)

## 5.7 Composite view

Figure 1 summarises the four computed neutrosophic indicators in a
single composite figure.

> **Figure 1.** Neutrosophic bibliometric indicators applied to NCML
> (2018–2026). (A) Neutrosophic h-index decomposition over the
> stratified Scholar sample (n = 26): T = 0.04, I = 0.50, F = 0.46. (B)
> Bootstrap distribution of the Lotka exponent α (B = 1 000); the
> classical α = 2 sits inside the bootstrap mode while the K-S
> statistic exceeds the critical value in all replicates, yielding
> N_Lotka = (0.00, 1.00, 0.00). (C) Neutrosophic nucleus membership for
> the top ten cited journals (T green, I orange, F red); only the two
> top journals (NSS and NCML) clearly belong to the nucleus, while
> three Cuban journals occupy a boundary region. (D) Distribution of
> per-document topic membership across the 725 documents with usable
> abstracts; 61 % of documents have T < 0.7. (Source: `neutrosophic_indicators.png`.)
