# 1. Introduction

Bibliometric analysis quantifies the structure and dynamics of scholarly
publication using indicators such as the *h*-index, citation counts, the
Lotka and Bradford laws, co-authorship networks, and topic models. These
indicators have become central to research evaluation, journal benchmarking,
and editorial decision-making. Yet despite their explanatory power, the
classical indicators share a common epistemic limitation: they are computed
as crisp quantities even when the underlying data carry substantial
uncertainty.

Three concrete sources of indeterminacy illustrate the gap. First, *citation
counts* differ across databases. The same article may be reported as having
zero citations in OpenAlex and seventy-one in Google Scholar [1, 2]. Reporting
either one as the truth misrepresents the evidence; reporting the mean
discards the disagreement. Second, *parametric fits to power-law
distributions* such as Lotka’s law are typically reported as point estimates
with a standard error, yet the goodness-of-fit test (Kolmogorov–Smirnov, K-S)
frequently rejects the model even when the exponent matches the classical
prediction. Whether the journal "follows Lotka" is then a matter of degree,
not of yes-or-no. Third, *Bradford zone assignment* partitions a long list of
cited journals into three discrete buckets by cumulative citation share,
imposing crisp boundaries on what is fundamentally a continuous gradient.
Journals near the boundaries acquire a coin-flip identity that is preserved
neither by the data nor by the analyst's intent.

Neutrosophic logic, introduced by Smarandache in 1998 [3, 4], provides a
formal apparatus for reasoning under three independent components: truth (T),
indeterminacy (I), and falsity (F), each ranging in [0, 1]. Single-valued
neutrosophic numbers (SVN), introduced by Wang et al. (2010) [5], have become
the standard operational form for applied work. The neutrosophic framework
generalises probability, fuzzy logic and intuitionistic fuzzy logic by
treating indeterminacy as a separate, non-derivable dimension. The framework
has produced a substantial corpus of applied work in multi-criteria
decision-making, statistical process control, and several social-science
domains [6, 7].

Surprisingly, the application of neutrosophy to *bibliometric measurement
itself* remains largely unexplored. Existing bibliometric studies that
employ neutrosophic methods do so on top of the bibliographic data, applying
neutrosophic AHP-TOPSIS to rank journals or authors [8]. The indicators
themselves — citation counts, Lotka exponents, Bradford zones, topic
assignments, network weights — continue to be computed in the classical way,
even when their inputs carry obvious indeterminacy. This is a missed
opportunity. Critics of neutrosophic methods, notably Woodall, Faltin, and
Reynolds [9], have observed that many neutrosophic applications are
"decorative" in the sense that the choice of three components is not
justified by the data structure. We argue here that bibliometric measurement
is exactly the opposite: the data structure (multiple sources, partial
agreement, soft cluster assignments) calls for an indeterminacy-aware
formalism, and neutrosophy provides one.

## 1.1 Contribution

The contribution of this paper is threefold:

1. We define a **neutrosophic framework for bibliometric analysis** that
   extends five classical indicators — *h*-index, Lotka exponent, Bradford
   zone membership, document–topic membership, and co-authorship edge weight
   — into single-valued neutrosophic triples (T, I, F).
2. We provide an **operational implementation** of each extension as a
   reproducible algorithm with explicit aggregation rules. The
   implementation is published as open-source code at
   https://github.com/mleyvaz/ncml-bibliometric-2026.
3. We **validate the framework empirically** on a case study of
   *Neutrosophic Computing and Machine Learning* (NCML), comprising 762
   articles published between 2018 and 2026. The case study demonstrates
   that the neutrosophic indicators reveal information that the classical
   indicators conceal, and that this additional information is
   editorially actionable.

The paper is organised as follows. Section 2 reviews the relevant background
on neutrosophic logic, single-valued neutrosophic numbers, and the classical
bibliometric indicators we extend. Section 3 presents the formal framework
and the five neutrosophic extensions. Section 4 describes the data and
computational pipeline. Section 5 reports the case-study results. Section 6
discusses implications and addresses the methodological critique of Woodall
et al. (2025) [9]. Section 7 concludes and outlines future work.

## 1.2 Scope and limitations

The framework presented here is *complementary* to classical bibliometric
analysis, not a replacement. Each neutrosophic indicator can be reduced to
its classical counterpart by collapsing the indeterminacy component. The
purpose of the framework is to make the indeterminacy *visible* and *
quantifiable*, so that bibliometric reports can distinguish between robust
findings (low I) and fragile ones (high I).

The case study is restricted to a single journal (NCML). The conclusions
about NCML's bibliometric profile have been reported elsewhere using
classical methods [10] and are not the principal contribution here. The
principal contribution is the framework itself, demonstrated on a corpus
where the editorial team has direct knowledge of the data-generation
process.
