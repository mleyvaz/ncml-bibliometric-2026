# 6. Discussion

## 6.1 What the combined analysis reveals

The classical retrospective (Section 4) and the neutrosophic analysis
(Section 5) complement each other in a non-trivial way. The classical
indicators produce the familiar headline numbers that the editorial
community is trained to read: CAGR 42%, α = 2.03, nucleus of 5
journals, modularity 0.96, h = 1 vs h5 = 10. The neutrosophic
indicators re-express each of these as a (T, I, F) triple that makes
explicit the uncertainty the classical numbers conceal. Neither
analysis is complete without the other: a purely classical report
overstates the journal's measurable impact by collapsing source
disagreement into a single number, while a purely neutrosophic report
dilutes actionable headline numbers into triples that are harder to
communicate outside the specialist audience.

The *operative* validation of the neutrosophic framework — the SVNWA
aggregated author ranking of Section 5.6 — shows that the (T, I, F)
structure can produce conclusions that the alternatives cannot. With
a Kendall τ of 0.20 and half of the classical top-10 dropping out of
the neutrosophic top-10, the two rankings are only weakly correlated,
and the qualitative differences between them track interpretable
editorial dimensions (theoretical focus, cross-source citation
evidence, co-authorship centrality). Because the SVNWA operator
exploits the independence of T, I and F — the feature that neither
fuzzy nor intuitionistic-fuzzy aggregation preserves — the
re-ordering constitutes evidence that the neutrosophic formalism
yields information inaccessible to alternative techniques of equal
conceptual parsimony.

## 6.2 Engagement with Woodall et al. (2025)

Woodall, Faltin, and Reynolds [18] raised three points about the
applied use of neutrosophic methods: (i) the choice of three
components is rarely justified by data structure; (ii) comparisons
with fuzzy or Bayesian alternatives are absent or superficial; (iii)
the citation ecosystem is closed and self-referential. The present
combined paper addresses each point head-on.

On point (i): the framework derives the indeterminacy component
*from the data*, not from expert elicitation. Equation (2)
(neutrosophic Lotka) is a bootstrap computation; Equation (3)
(neutrosophic Bradford) is a continuous relaxation of a hard
threshold; Equations (6)-(7) (neutrosophic topic membership) are
distance-based; Equations (9)-(10) (neutrosophic co-authorship) are
count-based. None of them require a linguistic scale. The choice of
three components is warranted because the data exhibit the
asymmetric T/F/I structure (multiple sources with partial coverage)
that neutrosophy naturally captures.

On point (ii): for each of the five extensions we explicitly
identified the classical counterpart, demonstrated that the classical
indicator is recovered by collapsing I, and discussed in Section 5.6.3
why fuzzy and intuitionistic-fuzzy alternatives fail to preserve the
SVNWA ranking. A formal Bayesian dual of the framework is left for
future work (Section 7), but the bootstrap Lotka profile of Equation
(2) already admits a direct Bayesian re-interpretation as a
posterior distribution over a model space.

On point (iii): the classical retrospective of Section 4.4
documents empirically that 17.2% of NCML's journal citations go to
NSS and NCML themselves, that 94.9% of authorships are
Iberoamerican, and that the topic model identifies no fewer than
four distinct legal-medical applied clusters whose methodological
apparatus is essentially AHP-TOPSIS neutrosofico. These are
confirmations, not refutations, of the Woodall concerns. The
editorial roadmap of Section 7 proposes concrete mitigations.

## 6.3 Editorial implications for NCML

The combined analysis leads to four editorial implications that
reshape how NCML should communicate its own impact and structure
its own growth.

1. **Report bounded h-indices.** The journal's h5-index = 10 in
   Google Scholar Metrics and h = 1 in OpenAlex should be reported
   jointly, with the evidence-membership triple
   (T = 0.04, I = 0.50, F = 0.46) made explicit. Single-number
   reporting (either bound alone) is informationally incomplete.

2. **Acknowledge productivity-distribution shape divergence.** The
   neutrosophic Lotka profile (T = 0, I = 1, F = 0) confirms the
   classical exponent and confirms the K-S failure. The journal
   should communicate that it follows Lotka in *parameters* but not
   in *shape*, reflecting its training-venue function.

3. **Distinguish strong, boundary, and peripheral citation sources.**
   Graded Bradford nucleus membership recommends an auto-citation
   policy for T > 0.7 sources (NSS, NCML itself), diversification for
   T = 0.5-0.7 (the three Cuban journals), and outreach for T < 0.4
   (international fuzzy / soft computing venues).

4. **Rank authors by neutrosophic aggregate.** The SVNWA ranking of
   Section 5.6 identifies the authors whose contribution to NCML is
   not captured by raw article count. Editorial recognition (guest
   editorships, invited reviews, thematic issues) should follow the
   aggregate, not the count. Conversely, prolific authors whose
   neutrosophic score drops sharply have contributed volume without
   external citation evidence or theoretical focus, and editorial
   decisions about these authors should reflect that.

## 6.4 Limitations

Five limitations qualify the conclusions.

- **Sampled Scholar citations.** The neutrosophic *h*-index is
  computed on a stratified sample of n = 26 articles for which
  Scholar counts are manually verified. Generalising the (T, I, F)
  proportions to the full population requires either an exhaustive
  Scholar scrape (impractical without paid tools) or a larger
  stratified sample. Bootstrap intervals on the (T, I, F)
  proportions themselves would be a useful refinement.
- **Heuristic reference extraction.** The Bradford analysis of
  Section 4.4 uses regex-based parsing of reference blocks, which
  misses 46% of references (mostly books, theses, URLs, and
  irregularly-formatted Iberoamerican journals). GROBID-quality
  parsing would sharpen the Bradford nucleus at the tail; the top-10
  rankings are robust.
- **Two-dimensional topic distances.** The neutrosophic topic
  membership uses 2D UMAP coordinates as a proxy for the 5D
  clustering space. This compresses distances slightly and may
  inflate the indeterminacy estimate.
- **Single-journal scope.** The retrospective is confined to NCML;
  comparison with NSS and IJNS applying the same pipeline is a
  direct and valuable extension.
- **Editorial conflict of interest.** Two of the three authors are
  Editors-in-Chief of NCML and NSS. The third author, from ALCN, is
  not editorial but is institutionally linked to the neutrosophic
  community. Mitigation has been attempted through explicit
  disclosure and a request for fully external peer review (see
  cover letter accompanying this manuscript). Readers should form
  their own judgement about residual bias.

## 6.5 Comparison with alternative formalisms

The choice of SVN over alternative uncertainty formalisms merits
brief discussion.

*Probability* is suited when the data-generation process can be
modeled with a likelihood. The bootstrap Lotka profile is a
probabilistic computation, and the neutrosophic profile inherits its
statistical foundation. But for the h-index decomposition, Bradford
membership, topic membership, and edge weight, no single likelihood
model captures the multiplicity of independent sources; the
neutrosophic triple naturally accommodates this without forcing a
Bayesian commitment to a prior.

*Fuzzy sets* model graded membership but lack a separate falsity
component. Table 2 in Section 5.6 illustrates the value of an
explicit F: authors with small T and substantial F are qualitatively
different from those with the same T and F = 0, and the SVNWA
ranking captures this distinction. Fuzzy aggregation does not.

*Intuitionistic fuzzy sets* introduce a non-membership degree but
maintain T + F ≤ 1. For bibliometric data where an author can
simultaneously show high positive evidence in one source and high
negative evidence in another, the constraint T + F ≤ 1 is
empirically violated. Neutrosophy relaxes the constraint (T + I + F
≤ 3) and treats I as an independent measurement, matching the
empirical situation.

In sum, the neutrosophic formalism is not the only option; for the
data structure at hand it is the most natural option that makes
indeterminacy visible without artificial compression.
