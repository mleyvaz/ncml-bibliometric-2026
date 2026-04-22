# 5. Neutrosophic Analysis of the Same Corpus

Section 4 reported the classical bibliometric retrospective. The crisp
indicators reveal substantive findings but conceal the indeterminacy
that the multi-source nature of contemporary bibliographic data
forces upon them. This section re-analyses the same corpus through
the neutrosophic framework of Section 3 and culminates (Section 5.6)
in the SVNWA aggregated author ranking, which addresses RQ6 and
provides the operative test that distinguishes neutrosophic
aggregation from alternative uncertainty formalisms.

## 5.1 Neutrosophic *h*-index

Applying Equation (1) of Section 3.2.1 to the stratified sample of
n = 26 articles for which both OpenAlex and Google Scholar counts
exist:

- **T-class** (cited in both sources): 1 article (3.8%).
- **I-class** (cited in only one source): 13 articles (50.0%).
- **F-class** (no citation in any source): 12 articles (46.2%).

The journal-level neutrosophic h-index profile is

  N_h(NCML) = ( T = 0.04, I = 0.50, F = 0.46 )

with bounds h_T = 1 (lower, OpenAlex-only) and h_TI ≤ h5 = 10
(upper, Google Scholar Metrics). The midpoint ≈ 5.5 is the value an
editorial board should use for benchmarking under explicit
acknowledgement of source uncertainty.

The classical headline "h = 1" is technically correct but
informationally misleading. The neutrosophic profile reveals that
**half of the sampled articles sit in evidential limbo**: cited in
one database, absent in the other, leaving the analyst to choose
whether to count them or not.

## 5.2 Neutrosophic Lotka exponent

Bootstrap resampling over B = 1 000 replicates produces α̂ with mean
2.03 and 95% percentile interval [2.00, 2.06]. The K-S statistic
exceeds the 5%-critical value 0.038 in *every* replicate. Applying
Equation (2):

  N_Lotka(NCML) = ( T = 0.00, I = 1.00, F = 0.00 )

The interpretation is that NCML's productivity distribution **matches
the classical Lotka exponent perfectly but its shape diverges in
every bootstrap replicate**. The classical "follows Lotka with
α = 2.03" is true in the parametric sense and false in the shape
sense; the neutrosophic profile resolves the apparent contradiction
by reporting both. The cause of the shape divergence is identified
in Section 4.3: an excess of one-shot authors (71.9% vs 61.7%
predicted), characteristic of a training venue.

## 5.3 Neutrosophic Bradford zone membership

The classical Bradford partition (Section 4.4) assigns 5 journals to
the nucleus with hard boundaries. Applying Equations (3)-(5) to the
top-ten cited journals:

| Rank | Journal | T_nuc | I_nuc | F_nuc |
|---|---|---|---|---|
| 1 | Neutrosophic Sets and Systems | 0.88 | 0.17 | 0.00 |
| 2 | Neutrosophic Computing and Machine Learning | 0.85 | 0.20 | 0.00 |
| 3 | Universidad y Sociedad | 0.64 | 0.37 | 0.00 |
| 4 | Serie Cientifica U. Ciencias Informaticas | 0.52 | 0.40 | 0.08 |
| 5 | Revista Conrado | 0.50 | 0.40 | 0.10 |
| 6 | Conrado (variant) | 0.35 | 0.42 | 0.23 |
| 7 | International Journal of Neutrosophic Science | 0.28 | 0.41 | 0.31 |
| 8 | Revista de Ciencias Medicas de Pinar del Rio | 0.25 | 0.40 | 0.35 |
| 9 | Revista Cubana de Ciencias Informaticas | 0.24 | 0.39 | 0.37 |
| 10 | Revista Cubana de Informatica Medica | 0.22 | 0.39 | 0.39 |

Two findings emerge that the classical analysis hides. First, the
nucleus is *not* internally homogeneous: the top two journals (NSS
and NCML, both inside the neutrosophic ecosystem) have T ≥ 0.85,
while ranks 3-5 (three Cuban journals) sit at T = 0.50-0.64 with
substantial I, indicating *boundary-nucleus* status rather than
strong membership. Second, ranks 6-10 have T ≈ I ≈ F ≈ 0.3,
meaning they are neither unambiguously inside nor outside the
nucleus.

## 5.4 Neutrosophic topic membership

Applying Equations (6)-(8) to the 725 documents yields: only **39%
of documents have T ≥ 0.7 in their assigned topic**. The remaining
61% distribute as follows: 21% have moderate T (0.4 ≤ T < 0.7) and
40% have T < 0.4 with substantial I, indicating they sit on or near
a topic boundary. Mean I is 0.13 with standard deviation 0.10;
documents with I ≥ 0.3 number 154 (21%) and represent the
topic-boundary cohort.

The editorial interpretation is direct: roughly four out of every
ten NCML articles published 2018-2026 do not belong unambiguously
to a single topic in the 24-topic model. Topic-based benchmarking
that ignores this fact will systematically misattribute articles in
the legal-medical interface (topics T0, T9, T17, T20, T22, T23)
where the boundaries are substantively fluid (a paper on legal
aspects of medical malpractice straddles two topics by construction).

## 5.5 Neutrosophic co-authorship edge weights

Applying Equations (9)-(11) to the 2 174 edges of the network:

- T_collab ≥ 0.5 (verified collaboration): **40 edges (1.8%)**.
- I_collab ≥ 0.5 (single-article collaboration): 1 963 edges (90.3%).
- Intermediate T-I balance: 171 edges (7.9%).

A network of *verified* collaborations (T_collab ≥ 0.5) drops the
graph from 1 363 nodes and 2 174 edges to a subgraph of 35 nodes and
40 edges, dominated by four to five prolific Ecuadorian research
groups (UNIANDES Riobamba, UBE, UNIANDES Ambato) and the
international group Smarandache-Leyva-Fujita. The classical
modularity 0.96 reduces to 0.81 on the verified network — still
high, but substantially less spectacular. This is honest: the
journal's intellectual integration is measurable on a much smaller
core than the classical graph suggests, and the bulk of the graph
reflects the *publication marketplace* rather than a coherent
community of practice.

## 5.6 Neutrosophic aggregated author ranking (RQ6) — the operative test

The preceding subsections re-expressed each classical indicator as a
neutrosophic triple and demonstrated that the indeterminacy carries
non-trivial information. A stronger operative test of the framework
is whether the (T, I, F) triples, once aggregated across dimensions
through SVNWA, **yield a ranking that differs from the classical
ranking and whose differences are editorially interpretable**. If
fuzzy, intuitionistic-fuzzy, or probabilistic aggregation could
produce the same ranking, then the neutrosophic formalism would
carry no additional information; if they cannot, the neutrosophic
framework is operatively distinct.

### 5.6.1 Design

We rank the 146 authors with ≥ 3 articles along four neutrosophic
dimensions:

- **D1. N-productivity.** T = sigmoid centred at 8 articles, I = bell
  peaking at the mid-range (3-6 articles), F = residual.
- **D2. N-citational evidence.** Per-article source-triangulation class
  (T = cited in both OpenAlex and Scholar, I = cited in one only,
  F = no evidence), averaged across the author's publications. For
  unsampled articles, OpenAlex-only counts yield higher I.
- **D3. N-co-authorship centrality.** Mean T_collab, I_collab,
  F_collab over the edges incident to the author.
- **D4. N-theoretical focus.** Share of the author's publications in
  theoretical topics (T7, T16, T2) = T; share in applied legal-medical
  topics = F; share in other topics = I.

Aggregation: SVNWA of Equation (12) with equal weights 0.25.
Score: Smarandache's S(T, I, F) = (2 + T − I − F) / 3 of Equation (13).
Classical baseline: rank by article count.

### 5.6.2 Results

The two rankings differ substantially:

- **Kendall τ = 0.20** (p = 0.001) — weak positive correlation.
- **Spearman ρ = 0.25** (p = 0.003) — same direction, still weak.
- **Top-10 overlap = 5/10** (Jaccard = 0.33) — half of the classical
  top-10 does *not* appear in the neutrosophic top-10.

Authors whose neutrosophic rank is substantially *higher* than their
classical rank share a common profile: small article count (3-4
publications) but high share of theoretically-focused papers (T7, T2,
T16) and well-cited in at least one source. Conversely, authors
whose neutrosophic rank is substantially *lower* show a different
profile: 4-6 publications concentrated in legal-medical applied
topics with low co-authorship centrality (they publish within a
single closed research group) and no citation evidence in either
OpenAlex or Scholar.

Table 2 shows the five largest rises and falls.

| Change | Author | Articles | Rank (classical) | Rank (neutrosophic) |
|---|---|---|---|---|
| ↑ +81 | Lozada Torres, Edwin Fabricio | 3 | 87 | 6 |
| ↑ +78 | Parrales-Bravo, Franklin | 3 | 87 | 9 |
| ↑ +75 | Villalba León, Carlos Luis | 3 | 87 | 17 |
| ↑ +67 | Alvarado, Yelena Abreu | 3 | 87 | 20 |
| ↓ −100 | Romero Fernández, Ariel José | 4 | 52 | 135 |
| ↓ −92 | Cruz Piza, Iyo Alexis | 6 | 20 | 112 |
| ↓ −90 | Troya Terranova, Katherine Tatiana | 5 | 35 | 128 |
| ↓ −90 | Machado Maliza, Mesías Elías | 4 | 52 | 142 |
| ↓ −84 | Chamorro Valencia, Diego Xavier | 5 | 35 | 119 |

### 5.6.3 Why this is a genuinely neutrosophic finding

The re-ordering **cannot be reproduced by alternative uncertainty
formalisms** without introducing additional structure equivalent to
the (T, I, F) triple:

- *Probabilistic aggregation* of the four dimensions requires a
  likelihood model per dimension, which does not exist naturally for
  D2, D3, or D4.
- *Fuzzy aggregation* collapses I and F into a single non-membership,
  losing the distinction between "no evidence" and "contradictory
  evidence". In D2 this distinction is empirically critical.
- *Intuitionistic fuzzy aggregation* preserves T and F but forces
  T + F ≤ 1, which is violated whenever an author has strong positive
  evidence in Scholar *and* strong negative evidence in OpenAlex — the
  high-discrepancy case that Section 5.1 identified as dominant in
  this corpus.

The SVNWA aggregate exploits precisely the independence of the three
components — the feature that distinguishes neutrosophy from its
predecessors — to produce a measurement that the predecessors
cannot. This is the operative validation that the framework yields
information unreachable by alternative techniques of comparable
conceptual parsimony, not merely an alternative notation.

> **Figure 8.** Rank divergence between the classical article-count
> ranking and the neutrosophic SVNWA ranking over 146 NCML authors
> with ≥ 3 publications. (A) Scatter of rank positions with identity
> line; points far from the line indicate large divergence. (B)
> Top-15 authors by each ranking, side by side, showing substantial
> re-ordering of the journal's visible leadership. (Source:
> `ranking_comparison.png`.)

## 5.7 Composite view

Figure 9 summarises the four per-indicator neutrosophic decompositions
in a single composite figure for comparison with the classical
results of Section 4.

> **Figure 9.** Composite view of neutrosophic bibliometric
> indicators on NCML. (A) N-*h*-index decomposition on the Scholar
> sample (T = 0.04, I = 0.50, F = 0.46). (B) Bootstrap distribution
> of α with Lotka-classical reference and 95% CI band. (C)
> Neutrosophic nucleus membership for top-10 cited journals (T, I, F
> side by side). (D) Distribution of per-document topic membership
> T. (Source: `neutrosophic_indicators.png`.)
