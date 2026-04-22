# 4. Classical Bibliometric Retrospective of NCML

This section presents the classical bibliometric findings on the NCML
corpus. Each subsection addresses one research question and references
the corresponding figure. Section 5 will subsequently re-analyse the
same corpus through the neutrosophic framework of Section 3.

## 4.1 Editorial growth and community formation (RQ1)

Between 2018 and 2026, NCML published **762 articles** distributed
across **42 volumes**. Annual growth follows a marked exponential
trajectory, with a compound annual growth rate (CAGR) of **42%**
between 2018 and 2025 (Figure 1A). The journal rose from 24 articles
in 2018 to 250 in 2025, a ten-fold multiplier in seven years. The
year 2026 appears as partial because the cutoff is April 2026.

Cumulative community formation grew in parallel (Figure 1B). Unique
authors moved from 50 in 2018 to 1 363 in 2026, a factor of 27×. The
rate of new authors per year was stable at ~50–65 between 2018 and
2021, then sextupled from 2023 onward (124 new authors in 2022, 323
in 2023, 316 in 2024, 349 in 2025), indicating an expansion of the
collaborator pool that accompanied the volume growth.

> **Figure 1.** Editorial growth of NCML. (A) Articles published per
> year with CAGR 2018-2025 = 42%. Hatched bars mark partial year data.
> (B) New authors per year and cumulative unique-author curve.
> (Source: `growth.png`.)

## 4.2 Geographic and institutional distribution

The distribution of authorships (based on the 88% of author rows with
OpenAlex-extracted affiliation) shows extreme regional concentration
(Figure 2A). Of 158 authorships with an identified country, 150
(94.9%) correspond to Iberoamerican countries. Ecuador concentrates
60.1% (95 authorships), Cuba 19.0% (30), and Venezuela 7.0% (11). The
top-3 (Ecuador–Cuba–Venezuela) absorbs 86% of the total. Only 8
authorships originate outside Iberoamerica: Bulgaria (3), United
States (3), India (1), Japan (1).

At the institutional level (Figure 2B), Universidad Regional Autonoma
de los Andes (UNIANDES, Ecuador) leads with 23 authorships, followed
by Universidad Bolivariana del Ecuador (UBE, 20), Universidad de
Guayaquil (17), Universidad Estatal de Bolivar (15), Universidad de
Holguin (12, Cuba), and Politecnica Salesiana (12, Ecuador). The top
five institutions are all Ecuadorian; nine of the top ten are from
Ecuador or Cuba.

> **Figure 2.** Geographic and institutional distribution of NCML
> authorships. (A) Authorships by country (Iberoamerican countries
> highlighted in red). (B) Top 15 institutions. (C) Regional
> concentration (95% Iberoamerican). (Source: `geo.png`.)

## 4.3 Author productivity and Lotka's law (RQ2)

The corpus exhibits the classical signatures of scientific
productivity distributions: a large base of one-time authors and a
thin tail of highly prolific ones. Of 1 363 unique authors, 940
(69%) appear in a single article, and only 51 (3.7%) have five or
more. After disambiguation, the most prolific authors are Carmen
Marina Méndez Cabrita (29 articles), Florentin Smarandache (25), and
Maikel Leyva Vázquez (19).

Maximum-likelihood fitting of n(x) ∝ x^(-α) with x_min = 1 yields

  α̂ = 2.027  (SE = 0.028, n = 1 363)

statistically indistinguishable from the classical α = 2. However,
the Kolmogorov-Smirnov test is not passed (D = 0.120, 5%-critical =
0.038): the data deviate systematically from the theoretical
distribution in two places (Figure 3). First, the empirical share of
one-article authors (71.9%) exceeds the theoretical prediction
(61.7%) by more than ten percentage points. Second, the tail shows
non-smooth jumps in the interval [5, 29] articles.

The interpretation is consistent with the pattern of journals with a
strong training function: a continuous flow of one-shot authors
(graduate students, thesis candidates) overlays a small but highly
productive editorial core. The Pareto curve confirms that 80% of
articles come from the top ~17% of authors.

> **Figure 3.** Lotka's law on NCML. (A) Empirical (points) versus MLE
> fit (red line) in log-log scale. (B) Empirical vs theoretical CDF,
> K-S = 0.12. (Source: `lotka_loglog.png`.)

## 4.4 Dispersion of cited sources and Bradford's law (RQ3)

The 21 943 references extracted from bibliography blocks (mean 31.1
per article) allowed identification of the source journal in 11 877
citations (54.1%), distributed over **2 339 unique sources**. The
rest correspond mostly to books, theses, reports, and URLs, which
fall outside the Bradford framework.

Partitioning into three equal-citation zones (Figure 4A) produces
extreme concentration:

- **Zone 1 (nucleus):** 5 journals concentrate 3 963 citations (33.4%).
- **Zone 2 (middle):** 74 journals concentrate 3 970 citations (33.4%).
- **Zone 3 (periphery):** 2 260 journals concentrate 3 944 citations (33.2%).

The empirical Bradford multiplier is k = [14.8, 30.5], far from the
constant value predicted by classical law (k ≈ 3–5). This indicates
an extremely heterogeneous dispersion: the nucleus is 3 to 5 times
more concentrated than typical.

The five nucleus journals (Figure 4B) are:

| Rank | Journal | Citations |
|---|---|---|
| 1 | Neutrosophic Sets and Systems | 1 047 |
| 2 | Neutrosophic Computing and Machine Learning (self-citation) | 1 000 |
| 3 | Universidad y Sociedad (Cuba) | 722 |
| 4 | Serie Cientifica de la Universidad de las Ciencias Informaticas (Cuba) | 608 |
| 5 | Revista Conrado (Cuba) | 586 |

NSS and NCML jointly represent **17.2% of the detected journal
citations**, confirming that the neutrosophic ecosystem is
markedly self-referential. Among the top 15 most-cited journals, 8 are
Iberoamerican journals not indexed in Scopus, and only 2 belong to
mainstream international circuits (IEEE Transactions on Fuzzy
Systems, Fuzzy Sets and Systems) with 105 combined citations (<1%
of the total).

> **Figure 4.** Bradford's law on NCML. (A) Cumulative-citations curve
> vs journal rank (log scale) with zones 1 and 2 marked. (B) Top 20
> cited journals; the heaviest are the neutrosophic ecosystem and
> Cuban journals of education and computer science. (Source:
> `bradford.png`.)

## 4.5 Thematic agenda and its evolution (RQ4)

Topic modeling on 725 documents with usable abstracts yielded **24
distinct topics** (Figure 5), with silhouette score 0.43 (optimal
K ∈ [10, 25]). The 2D UMAP projection shows a macrocluster structure
with clearly separated domains:

- **Law and justice** (237 aggregated articles, 33% of the corpus):
  T0 (law in Ecuador), T17 (labour and migration law), T9 (violence
  and victims), T23 (criminal law), T15 (indigenous peoples), T5
  (administrative law), T6 (animal rights).
- **Health and medicine** (237, 33%): T22 (dentistry), T12
  (infectious disease), T20 (depression and older adults), T3 (trauma
  and clinical neurology), T10 (clinical microbiology), T13
  (pregnancy and maternal health), T11 (diabetes, obesity,
  hypertension), T1 (nursing care).
- **Education** (76, 13%): T14 (learning and students), T19
  (pedagogy and teacher training).
- **Neutrosophic theory and methods** (98, 14%): T7 (theoretical
  developments by Smarandache), T16 (software and SVNS), T2 (fsQCA
  and machine learning).
- **Others** (62, 9%): T4 (digital and municipal sustainability), T21
  (water and pollution), T18 (vehicles and energy), T8 (emotions in
  nursing).

Temporal evolution of topic share between 2018-2020 and 2023-2025
reveals a **drastic identity shift in the journal** (Figure 6). The
most-rising topics are all applied law or medicine: T0 Law/Ecuador
(+6.8 percentage points), T22 Dentistry (+6.7 pp), T17
Labour/migration (+6.7 pp), T12 Disease/virus (+5.2 pp), T23 Criminal
law (+5.1 pp). The most-falling topics are methodological and
educational:

- T14 Education/students: **-21.6 pp** (from 28% of the corpus in
  2018-2020 to 6% in 2023-2025).
- T16 AI/software/SVNS: -16.3 pp.
- T7 Smarandache/pure theory: -9.0 pp.
- T2 fsQCA/Machine Learning: -7.6 pp.
- T19 Pedagogy: -5.1 pp.

> **Figure 5.** 2D UMAP map of the 24 identified topics, coloured by
> cluster (KMeans). (Source: `topics_umap.png`.)
>
> **Figure 6.** Temporal evolution of the thematic agenda. (A) Topic-
> year heatmap with percentages by column. (B) Horizontal bar chart
> showing change in share (percentage points) between 2018-2020 and
> 2023-2025; emerging topics in blue, declining in red. (Source:
> `topics_heatmap.png` and `topics_trend.png`.)

## 4.6 Co-authorship network and invisible colleges

The full co-authorship graph contains **1 363 nodes** and **2 174
edges**, with density 0.0023 and mean degree 3.19. The structure is
extremely fragmented: 264 connected components are identified, and
the main component groups only **15.8% of authors** (216 nodes). This
is unusual for a journal with such editorial volume and contrasts
sharply with the networks of established journals such as NSS.

Louvain community detection on the full graph yields **modularity =
0.96** with 81 communities, indicating a near-perfectly disjoint group
structure. The largest communities correspond to Ecuadorian university
groups:

| Community | Members | Articles | Principal authors |
|---|---|---|---|
| C33 | 39 | 160 | Méndez Cabrita, Isea Arguelles, Crespo Berti |
| C14 | 31 | 121 | Fiallos Bonilla, Bucaram Caicedo, Urrutia Guevara |
| C12 | 23 | 74 | López Torres, García Novillo, Salame Ortiz |
| C34 | 15 | 63 | Quevedo Arnaiz, Benavides Salazar, García Arias |
| **C29** | **9** | **61** | **Smarandache, Leyva Vázquez** |

Community C29 (the international theoretical core Smarandache-Leyva)
is the smallest of the top five but has the highest productivity per
member (6.8 articles/author vs 4.1 in C33). It is also the only
community with significant non-Iberoamerican representation. The mean
clustering coefficient of the full graph (0.756) indicates that the
few triangles are highly concentrated: teams are internally closed
cliques with few outward connections. The diameter of the main
component is 11 with mean path length 5.2.

> **Figure 7.** NCML co-authorship network. (A) Main connected
> component (n = 216, 16% of all authors); colours by Louvain
> community. (B) Productive core (authors with ≥ 4 articles connected,
> n = 72). (C) Full filtered network (≥ 2 articles, n = 368),
> visualising fragmentation as a constellation of disjoint clusters.
> (Source: `coauth_main.png`, `coauth_core.png`, `coauth_full.png`.)

## 4.7 Citational impact: discrepancy between sources (RQ5)

The citational impact of NCML shows a **discrepancy of an order of
magnitude between bibliometric sources**. OpenAlex reports a total of
27 citations over the 762 publications (ratio 0.04 cites/article) and
a journal h-index of 1. Only 8 articles (1.0%) exceed one citation
according to this source. In contrast, Google Scholar Metrics reports
for NCML (2020-2024 window):

- **h5-index = 10** (10 articles published 2020-2024 with ≥ 10
  citations each).
- **h5-median = 25** (median of citations of those 10 articles).

These metrics are consistent with those of sister journals in the
ecosystem: NSS (h5 = 57, h5-median 76) and IJNS (h5 = 31, h5-median 51).

The stratified sample (n = 26) confirms the discrepancy (Table 1). In
the sample, 53.8% of articles have at least one Scholar citation vs
only 3.8% in OpenAlex, with 116 total Scholar citations vs 20
OpenAlex (factor 5.8× on the same sample). An article from Vol.11
(2020), "Método para medir la formación de competencias pedagógicas
mediante números neutrosóficos", reports 71 Scholar citations and 0
OpenAlex citations, illustrating the extreme case.

| Source | Total citations | ≥ 1 citation | h / h5 |
|---|---|---|---|
| OpenAlex (n=762) | 27 | 8 (1.0%) | h = 1 |
| Scholar sample (n=26) | 116 | 14 (53.8%) | — |
| Scholar Metrics 2020-2024 | — | — | h5 = 10 |

NCML **is not indexed in Scopus** (verified against the official
Elsevier source list and SCImago). Hence CiteScore, SJR, and SNIP do
not apply. This absence, combined with the strong dependence on
Scholar citations and the ecosystem self-referentiality (Section 4.4),
explains the asymmetry: OpenAlex partially indexes Zenodo but not NSS
and IJNS in depth, while Scholar captures all three.
