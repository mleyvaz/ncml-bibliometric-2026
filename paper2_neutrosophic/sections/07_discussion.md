# 6. Discussion

## 6.1 What the framework reveals beyond classical analysis

The central operative finding of the paper is the substantive
divergence between the classical article-count ranking and the SVNWA
aggregated ranking of NCML authors (Section 5.6). With a Kendall τ of
0.20 and half of the classical top-10 dropping out of the neutrosophic
top-10, the two rankings are only weakly correlated, and the
qualitative differences between them track interpretable editorial
dimensions (theoretical focus, cross-source citation evidence,
co-authorship centrality). Because the SVNWA operator exploits the
independence of T, I and F — a feature that neither fuzzy nor
intuitionistic-fuzzy aggregation preserves — the re-ordering
constitutes evidence that the neutrosophic formalism yields
information inaccessible to alternative techniques of equal
conceptual parsimony.

The five per-indicator decompositions reported in Section 5 play a
supporting role rather than the principal one. They show that
indeterminacy is measurable and substantial in the source data, but
many of those findings could be reached by reporting multiple
sources side by side, by bootstrapping the Lotka fit, or by applying
a fuzzy membership function directly. What the aggregated ranking
demonstrates is that the *joint treatment* of all three components
across multiple dimensions — the operation that neutrosophy makes
natural and the alternatives make awkward — produces conclusions that
would be missed otherwise. Three concrete examples follow.

First, the *h*-index decomposition (Section 5.1) makes visible the
order-of-magnitude gap between OpenAlex and Google Scholar that the
classical headline number "h = 1" actively hides. The 50 % I-class
membership of the journal is not a defect of measurement but a property
of the bibliographic ecosystem: the journals that cite NCML the most are
themselves under-indexed by Crossref-anchored databases. An honest
editorial report should disclose the indeterminacy interval [h_T, h_TI]
rather than the lower bound alone.

Second, the bootstrap-based Lotka profile (Section 5.2) resolves the
apparent contradiction between α̂ = 2.03 and a failed K-S test. The
neutrosophic profile (T = 0, I = 1, F = 0) reports both facts
simultaneously: the *exponent* matches Lotka classical with high
confidence, while the *shape* deviates with equally high confidence.
Editorial analysts can then point to the source of the deviation
(over-representation of one-shot authors, characteristic of training
journals) instead of being forced to choose between "follows Lotka" and
"does not follow Lotka".

Third, the graded Bradford nucleus membership (Section 5.3) shows that
the journal's citation ecosystem has *three* substantively different
strata, not the canonical three Bradford zones. The strong-nucleus
journals (T > 0.7) are exclusively the two largest neutrosophic outlets
(NSS, NCML). The boundary-nucleus stratum (T = 0.5–0.7) is composed of
Cuban journals from the educational and informatics fields. The
peripheral-but-not-trivial stratum (T = 0.2–0.4) introduces a more
diverse and less neutrosophic-specific set of sources. Each stratum
implies a different editorial action: the strong-nucleus journals
require an auto-citation policy (the companion paper [10] documents a
17 % NSS+NCML self-citation rate); the boundary-nucleus stratum requires
diversification toward indexed venues; the peripheral stratum is the
target of the journal's outreach toward soft-computing and decision-
making mainstream.

## 6.2 Relation to the Woodall et al. (2025) critique

Woodall, Faltin, and Reynolds [9] published in 2025 a substantive
methodological critique of neutrosophic methods in statistical process
control and decision-making. Their three principal points were: (i)
the choice of three components (T, I, F) is rarely justified by the
data structure; (ii) comparisons with fuzzy or Bayesian alternatives
are absent or superficial; (iii) the citation ecosystem of neutrosophic
methods is closed and self-referential.

The framework presented here addresses each point head-on.

On point (i): in the neutrosophic bibliometric framework, the
indeterminacy component is *computed from the data*, not elicited from
experts via linguistic scales. The choice of three components is
warranted by the data structure (multiple sources of evidence with
explicit disagreement) rather than by analyst preference. This is the
strongest possible response to the "decorative neutrosophy" concern: in
the present framework, removing the indeterminacy component would
destroy information that is empirically present.

On point (ii): for each of the five extensions we identified the
classical counterpart. The classical *h*-index, Lotka exponent, Bradford
zones, topic assignment, and edge weight are recoverable from the
neutrosophic profile by collapsing I into either T or F. The
neutrosophic framework is therefore strictly informationally richer than
the classical baseline, not an alternative computation that yields the
same number with extra notation. Comparison with Bayesian alternatives
remains a target of future work; in particular, the neutrosophic Lotka
profile of Section 3.2 admits a direct Bayesian re-interpretation as a
posterior distribution over the model space {classical, alternative},
which we discuss in Section 7.

On point (iii): the present paper is itself an exercise in opening the
neutrosophic ecosystem to external scrutiny. The framework is
methodological rather than applied, the case study is published with
all data and code under permissive licences, and the discussion of
limitations is explicit (Section 6.4). The companion paper [10]
documents the auto-referentiality empirically and proposes editorial
remediation. The two papers together represent a self-critical posture
that the Woodall critique would, in our reading, encourage rather than
condemn.

## 6.3 Editorial implications for NCML

The five neutrosophic indicators applied to NCML produce four concrete
editorial implications.

1. **Report bounded h-indices.** The journal's h5-index = 10 in Google
   Scholar and h = 1 in OpenAlex should be reported jointly, with the
   evidence-membership triple (0.04, 0.50, 0.46) made explicit in
   editorial communications. Reporting either bound alone is
   informationally incomplete.

2. **Acknowledge the productivity-distribution shape divergence.** The
   bootstrap-based Lotka profile (T = 0, I = 1, F = 0) confirms the
   classical exponent and confirms the K-S failure. The journal should
   communicate that it follows Lotka in *parameters* but not in *shape*,
   reflecting its training-venue function.

3. **Distinguish strong, boundary, and peripheral citation sources.**
   The graded Bradford nucleus membership recommends an auto-citation
   policy applied to T > 0.7 sources, a diversification policy for T =
   0.5–0.7 sources, and an outreach policy for T < 0.4 sources.
   Compressing all five nucleus journals into a single category misses
   the distinction.

4. **Identify the verified-collaboration core.** The reduced-graph
   subnetwork of T_collab ≥ 0.5 edges (40 edges, 35 nodes) is the
   journal's actual community of practice. Editorial actions intended
   to consolidate the journal's identity should target this network,
   not the long tail of single-paper co-authorships.

## 6.4 Limitations

Three limitations qualify the conclusions.

First, the neutrosophic *h*-index is computed on a stratified sample of
n = 26 articles for which both OpenAlex and Scholar counts are
available. Generalising the (T, I, F) proportions to the journal
population requires either an exhaustive Scholar scrape (impractical
without paid tools and at high risk of rate-limiting) or a larger
stratified sample. The current estimates of T = 0.04 and I = 0.50
should be read as point estimates with substantial sampling
uncertainty; bootstrap or Bayesian intervals on the proportions
themselves would be a useful refinement.

Second, the neutrosophic topic membership in Section 3.4 was computed
from two-dimensional UMAP coordinates rather than from the
five-dimensional clustering space. This compresses the distances
slightly and may inflate the indeterminacy estimate. Computing the
distances in the 5D space requires re-running the clustering pipeline
and is a target for the next revision.

Third, the framework is restricted to a single journal. Cross-journal
comparison would require applying the same pipeline to NSS, IJNS, and
related venues. The companion paper [10] points to such comparison as
the principal extension. The neutrosophic framework facilitates the
comparison precisely because it makes the cross-source disagreement
explicit, and we expect that NSS and IJNS will exhibit different
T/I/F profiles: NSS, being indexed in Scopus since 2021, should show
much higher T_h with correspondingly lower I_h.

## 6.5 Comparison with alternative formalisms

The choice of single-valued neutrosophic numbers over alternative
uncertainty formalisms (probability, fuzzy sets, intuitionistic fuzzy
sets) merits brief justification.

*Probability* is suited when the data-generation process can be
modelled with a likelihood. The bootstrap Lotka profile of Section 5.2
is in fact a probabilistic computation, and the neutrosophic profile
inherits its statistical foundation. However, for the *h*-index and
Bradford membership, no single likelihood model captures the
multiplicity of independent sources; the neutrosophic triple naturally
accommodates this without forcing a Bayesian commitment to a prior.

*Fuzzy sets* model graded membership but lack a separate falsity
component. The Bradford profile of Table 1 illustrates the value of an
explicit F: a journal with T = 0.2 and F = 0.5 is qualitatively
different from one with T = 0.2 and F = 0.0, even though both have
identical T. Fuzzy sets cannot make this distinction.

*Intuitionistic fuzzy sets* introduce a non-membership degree but
maintain the constraint T + F ≤ 1 with hesitancy as a derived quantity.
Neutrosophy relaxes this constraint, allowing T + I + F ≤ 3 and
treating I as an independent measurement. For bibliometric data this
relaxation matches the empirical situation: an article can be cited in
multiple sources (high T) and contested or under-cited in others (high
F, possibly with high I) — a configuration that intuitionistic fuzzy
sets cannot represent.

In sum, the neutrosophic formalism is not the only choice; it is the
most natural choice given the structure of the data and the desire to
report indeterminacy explicitly rather than collapse it.
