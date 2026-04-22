# 7. Conclusions and Future Work

## 7.1 Conclusions

We have presented a neutrosophic framework for bibliometric analysis
that extends five classical indicators — *h*-index, Lotka exponent,
Bradford zone membership, document–topic membership, and co-authorship
edge weight — into single-valued neutrosophic triples (T, I, F). The
framework computes the indeterminacy component directly from the data,
avoiding the criticism that neutrosophic methods are decorative
overlays on top of crisp computations. Each extension reduces to its
classical counterpart by collapsing the indeterminacy component, so the
framework is strictly informationally richer than the classical
baseline rather than an alternative requiring methodological commitment.

The empirical case study on *Neutrosophic Computing and Machine
Learning* (NCML, 762 articles, 2018–2026) demonstrated five substantive
findings:

- The neutrosophic *h*-index reveals that 50 % of articles in the
  evaluated sample sit in an evidential limbo where the citation
  evidence depends on the source consulted, a fact that classical
  reporting hides.
- The bootstrap Lotka profile resolves the apparent contradiction
  between a classical exponent and a failed shape test, attributing the
  divergence to the journal's training-venue function.
- The graded Bradford nucleus membership distinguishes strong-nucleus
  journals (T > 0.7) from boundary-nucleus and peripheral journals,
  enabling differentiated editorial policy.
- The neutrosophic co-authorship profile reduces the journal's
  intellectual integration metric (modularity) from the spectacular
  classical value of 0.96 to a more honest 0.81 once single-paper
  collaborations are recognised as opportunistic rather than
  consolidated.
- **The SVNWA aggregated ranking of 146 authors diverges substantially
  from the classical article-count ranking** (Kendall τ = 0.20, top-10
  overlap 5/10), a divergence that cannot be reproduced by alternative
  uncertainty formalisms without introducing structure equivalent to
  the (T, I, F) triple. This is the operative validation that the
  framework yields information unreachable by classical, probabilistic,
  fuzzy, or intuitionistic-fuzzy techniques; it also re-orders the
  journal's visible leadership in editorially interpretable ways.

## 7.2 Future work

Five lines of extension are immediate.

1. **Cross-journal comparison.** Applying the framework to
   *Neutrosophic Sets and Systems* (NSS) and the *International Journal
   of Neutrosophic Science* (IJNS) would yield a comparative
   neutrosophic profile of the entire neutrosophic publication
   ecosystem. We anticipate that NSS, being Scopus-indexed since 2021,
   will exhibit substantially higher T_h and lower I_h than NCML.

2. **Bayesian dual.** Each neutrosophic triple admits a Bayesian
   re-interpretation in which T, I, F correspond to posterior
   probabilities over an evidential partition. Formalising this dual
   would address the comparison-with-Bayesian-alternatives concern in
   Woodall et al. [9] and produce a unified inferential framework.

3. **Plithogenic generalisation.** Plithogenic logic [21] generalises
   neutrosophy by allowing each attribute to take multiple values, each
   with its own degree. The bibliometric framework can be extended into
   plithogenic form to capture, for example, the multi-source
   citation evidence as a degree distribution over sources rather than
   as a single triple per source-pair.

4. **Larger Scholar samples.** The neutrosophic *h*-index was computed
   on a 26-article sample. Scaling to the full corpus requires either a
   paid Scholar API access (e.g., SerpAPI) or a distributed scraping
   pipeline. The framework itself is unchanged; only the empirical
   precision of T, I, F at the journal level improves.

5. **Adoption by other journals.** The framework is journal-agnostic.
   Editorial boards of any open-access journal with multiple citation
   sources of partial overlap (typical of all journals indexed in
   OpenAlex but not in Scopus, or vice versa) can apply the same
   pipeline. We invite replication and welcome reports of cases where
   the indeterminacy component is small (suggesting source-redundant
   coverage) or large (suggesting that single-source reporting is
   misleading).

## 7.3 Closing remark

The neutrosophic framework presented here is a methodological
contribution to bibliometric measurement, not a panegyric of
neutrosophic logic. Its value rests on a single empirical claim: in
contemporary bibliographic data, the indeterminacy of citation evidence,
of model fit, of zone membership, of topic assignment, and of
collaboration intensity is *measurable* and *substantial*. Reporting
this indeterminacy explicitly is more informative than concealing it
behind a single number. Whether the formalism used to report the
indeterminacy is neutrosophic, fuzzy, intuitionistic-fuzzy, or
probabilistic is, for the editorial purposes that motivated this paper,
a secondary matter. The neutrosophic formalism happens to fit the data
structure naturally; we leave to other researchers the task of
demonstrating that an alternative formalism fits better.
