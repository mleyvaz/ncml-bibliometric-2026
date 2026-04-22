# 8. Conclusion

This paper presented the first systematic bibliometric retrospective
of *Neutrosophic Computing and Machine Learning* (NCML) over its 42
published volumes (2018 to April 2026), combined with a methodological
contribution: a neutrosophic framework that extends five classical
bibliometric indicators into single-valued neutrosophic triples
(T, I, F) whose indeterminacy component is computed from the data
rather than elicited from experts. The operative validation of the
framework — the SVNWA aggregated ranking of 146 authors — demonstrates
that the (T, I, F) structure produces conclusions unreachable by
alternative formalisms (fuzzy, intuitionistic fuzzy, probabilistic) of
comparable conceptual parsimony.

Six findings structure the paper's conclusion.

1. **Editorial growth of 42% CAGR** (2018-2025) accompanied by a
   27-fold expansion of the unique-author community, with the
   acceleration concentrated in 2022-2025 and driven mainly by
   Ecuadorian university groups.

2. **Classical Lotka exponent (α = 2.03) with failed K-S test** — a
   configuration that the neutrosophic profile (T = 0, I = 1, F = 0)
   resolves honestly, attributing the divergence to the journal's
   training-venue function and the dominance of one-shot authors.

3. **Extreme Bradford concentration** (5 journals = 33% of citations,
   k = 14.8-30.5) that graded neutrosophic membership refines into
   three strata: strong nucleus (T > 0.7: NSS, NCML), boundary nucleus
   (T = 0.5-0.7: three Cuban journals), peripheral (T < 0.4:
   mainstream fuzzy / soft computing venues).

4. **Drastic thematic identity shift**: the education topic (T14) fell
   -21.6 percentage points between 2018-2020 and 2023-2025, replaced
   by applied legal and medical topics concentrated in Ecuadorian
   contexts.

5. **Order-of-magnitude citational discrepancy** between Google
   Scholar (h5 = 10) and OpenAlex (h = 1), decomposed by the
   neutrosophic *h*-index profile (T = 0.04, I = 0.50, F = 0.46) into
   a small verified core and a large source-disagreement band.

6. **SVNWA-aggregated author ranking diverges substantially from
   article-count ranking** (Kendall τ = 0.20, top-10 overlap 5/10) in
   a pattern that re-orders the journal's visible leadership by
   editorially interpretable dimensions (theoretical focus,
   cross-source evidence, co-authorship centrality). This divergence
   cannot be reproduced by alternative formalisms without introducing
   structure equivalent to the (T, I, F) triple.

The paper engaged the recent methodological critique of Woodall et
al. (2025) [18] directly: two of the three empirical concerns
(methodological concentration, citational concentration) are
confirmed by the classical retrospective; the third (external
validation) is partially confirmed and fully addressable by the
fifteen-recommendation editorial roadmap of Section 7. The appropriate
response is not defensive but reflexive: absorb the critique as an
agenda and execute the mitigations.

Five lines of future work follow naturally. First, a **comparative
application** of the pipeline to NSS and IJNS would yield a
comparative neutrosophic profile of the entire ecosystem. Second,
**GROBID-quality reference extraction** would sharpen the Bradford
tail and enable citation-network analysis. Third, a **Bayesian dual**
of the neutrosophic profile would address the Woodall concern about
comparison with probabilistic alternatives and produce a unified
inferential framework. Fourth, a **plithogenic generalisation** [21]
would accommodate multi-valued attributes (e.g., multi-source citation
evidence as a degree distribution over sources). Fifth, **editorial
adoption** by journals outside the neutrosophic ecosystem would test
the framework's generality; we invite replication.

A final methodological remark. The framework we presented is not a
panegyric of neutrosophic logic; its value rests on a single empirical
claim — that the indeterminacy of citation evidence, model fit, zone
membership, topic assignment, and collaboration intensity is
measurable and substantial in contemporary bibliographic data, and
that reporting it explicitly is more informative than concealing it
behind a single number. Whether the formalism used to report the
indeterminacy is neutrosophic, fuzzy, intuitionistic-fuzzy, or
probabilistic is secondary. The neutrosophic formalism happens to fit
the data structure naturally and to enable the SVNWA aggregation that
distinguishes it operatively; we leave to future researchers the task
of demonstrating that an alternative formalism can do the same work
with equal parsimony.

The code, datasets, and figures of this study are released as an
open repository at https://github.com/mleyvaz/ncml-bibliometric-2026
under MIT (code) and CC-BY 4.0 (data) licences.
