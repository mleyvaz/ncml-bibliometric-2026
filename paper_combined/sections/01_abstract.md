# Abstract

Neutrosophic Computing and Machine Learning (NCML) is the applied-methods
journal of the neutrosophic publication ecosystem founded by Smarandache,
with 42 volumes published between 2018 and 2026 (partial). No systematic
bibliometric retrospective of the journal has been published, and the recent
methodological critique of Woodall, Faltin and Reynolds (2025) raises three
empirically-testable concerns about the neutrosophic field: methodological
concentration, citational concentration, and limited external validation.
This paper combines a classical bibliometric retrospective of NCML
(Sections 4, 7) with a methodological contribution: the introduction of a
**neutrosophic bibliometric framework** that promotes indeterminacy to a
first-class component of measurement (Sections 3, 5).

We compiled a reproducible corpus of 762 articles through scraping,
enriched with OpenAlex (671/719 DOIs) and DataCite (704/719), disambiguated
1 363 unique authors by union-find (four hierarchical rules), fitted the
classical Lotka and Bradford laws, built the Louvain co-authorship network,
and modeled 24 topics with multilingual embeddings plus UMAP and KMeans on
725 usable abstracts. The neutrosophic framework extends five classical
indicators — *h*-index, Lotka exponent, Bradford zone membership,
document-topic membership, and co-authorship edge weight — into
single-valued neutrosophic triples (T, I, F) whose indeterminacy component
is **computed from the data rather than elicited from experts**. The
central operative test of the framework is a neutrosophic aggregated
ranking of authors using the SVNWA operator.

Classical results confirm a rapidly growing journal with CAGR 42% (2018-2025),
a Lotka exponent α = 2.03 (K-S rejected), a Bradford nucleus of five
journals concentrating 33% of citations (17% self-citation to the
neutrosophic ecosystem), a co-authorship graph of modularity 0.96 with only
a 16% main connected component, a topical identity shift of -21.6 pp in the
education topic between 2018-2020 and 2023-2025, and an order-of-magnitude
discrepancy between citation sources (Google Scholar h5-index = 10 vs
OpenAlex h = 1). The neutrosophic analysis decomposes these findings:
N-*h*-index (T = 0.04, I = 0.50, F = 0.46), N-Lotka (T = 0, I = 1, F = 0),
graded Bradford nucleus membership where only two journals reach T ≥ 0.85,
61% of documents with boundary-topic indeterminacy, and only 1.8% of
co-authorship edges with verified-collaboration T ≥ 0.5. **The SVNWA
aggregated ranking of 146 authors diverges substantially from the
classical article-count ranking (Kendall τ = 0.20, top-10 overlap 5/10)**,
a divergence unreachable by fuzzy, intuitionistic-fuzzy, or probabilistic
aggregation without introducing structure equivalent to the (T, I, F)
triple. The paper closes with a fifteen-recommendation editorial roadmap
organised on a three-year horizon.

**Keywords:** bibliometrics; neutrosophic logic; single-valued neutrosophic
numbers; SVNWA aggregation; Lotka's law; Bradford's law; *h*-index;
co-authorship network; topic modeling; Google Scholar Metrics; open-access
journals; editorial retrospective; Neutrosophic Computing and Machine
Learning.
