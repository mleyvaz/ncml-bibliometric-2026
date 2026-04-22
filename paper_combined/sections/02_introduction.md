# 1. Introduction

Bibliometric analyses of scientific journals fulfil a triple function in
the editorial community: they document the historical evolution of a
publication, they expose its collaborative structure, and they surface
both strengths and systemic biases for the adjustment of editorial
policy [2, 3]. When the signatories are the editors themselves, the
exercise acquires the additional character of an internal audit, with
the advantage of privileged access to data and the disadvantage of a
manifest conflict of interest.

Emerging scientific journals in Spanish-speaking countries face a double
challenge: demonstrating real impact in an ecosystem whose citation
sources are not fully indexed by the commercial bibliographic databases
(Scopus, Web of Science), and professionalising their editorial
processes to access those databases. The asymmetries between sources —
documented by Harzing and van der Wal [12] in the case of Google Scholar
versus Web of Science, and extended by Martin-Martin et al. [13] to the
Scholar-OpenAlex-Scopus contrast — are particularly severe for
Iberoamerican social-science journals and for journals publishing
through open-access repositories such as Zenodo or SciELO.

Classical bibliometric methods treat as crisp quantities that are
fundamentally uncertain. Citation counts collapse when sources disagree
by an order of magnitude; the Lotka exponent is reported as a point
estimate even when the Kolmogorov-Smirnov (K-S) test rejects the shape
hypothesis; Bradford zones partition journals into hard categories
despite obvious boundary cases; document-topic assignments are reduced
to winner-take-all labels even when soft clustering produces graded
probabilities; and co-authorship edges weight a single-paper
collaboration identically to a sustained five-paper partnership. This
indeterminacy is not measurement noise — it is a genuine property of
contemporary bibliographic data, and it is exactly the kind of
phenomenon that neutrosophic logic was designed to treat [4].

## 1.1 The neutrosophic ecosystem

Neutrosophy, formalised by Smarandache in 1998 as a trivalent extension
of fuzzy set theory [4, 5], has generated a specific editorial ecosystem
articulated around the Neutrosophic Science International Association
(NSIA). The doyen of the ecosystem is *Neutrosophic Sets and Systems*
(NSS), founded in 2013 and indexed in Scopus in 2021, with a Google
Scholar h5-index of 57 at the end of 2024. The *International Journal
of Neutrosophic Science* (IJNS, 2019; h5-index 31) followed, and as an
outlet for applications and computational methods, *Neutrosophic
Computing and Machine Learning* (NCML) began publication in 2018 and
to April 2026 accumulates 42 volumes.

NCML was conceived as the applied companion to NSS, emphasising case
studies, multi-criteria decision-making methods, and software
applications. During its early years it published 24-35 articles
annually with strong Latin-American representation (principally Cuba
and Ecuador). From 2022 onward the journal experienced an editorial
expansion that brought production above 250 articles per year in 2025.
To the authors' knowledge, no systematic bibliometric retrospective of
NCML has been published.

## 1.2 Recent methodological critique: Woodall et al. (2025)

In April 2025, Woodall, Faltin, and Reynolds published in *Quality
Engineering* a substantive critique of the inferential uses of
neutrosophic sets in statistical process control and multi-criteria
decision-making [18]. Their central concerns can be synthesised in
three points: (i) most reported applications use standard AHP-TOPSIS
configurations with neutrosophic numbers without justifying why
indeterminacy should be modeled with three components; (ii)
comparisons with classical fuzzy or Bayesian approaches are absent or
superficial; (iii) the internal citation circle of the neutrosophic
ecosystem limits external validation of the methods.

The critique provides a useful frame for a bibliometric study that
documents empirically the three signals Woodall and co-authors denounce
as indicative of a self-referential field: methodological
concentration, citational concentration, and geographical concentration.
The present study adopts this frame explicitly as a working hypothesis,
without assuming *a priori* that the three patterns hold, and allowing
the data to sustain, qualify, or refute them.

## 1.3 Objectives and research questions

The study has three articulated objectives:

1. **Descriptive**: document the editorial trajectory of NCML between
   2018 and 2026, including annual volume, thematic agenda, geography
   of authorships, and co-authorship structure.
2. **Analytical**: fit classical bibliometric laws (Lotka, Bradford)
   and contrast the results against theoretical reference values and
   the comparative literature on Spanish-language social-science
   journals.
3. **Methodological**: propose a neutrosophic extension of five
   classical bibliometric indicators and demonstrate, via an aggregated
   author ranking using SVNWA, that the framework yields conclusions
   unreachable by alternative formalisms of comparable conceptual
   parsimony.

From these objectives we derive six research questions.

- **RQ1.** How did the editorial volume, geographic composition, and
  institutional composition of NCML evolve across its 42 volumes?
- **RQ2.** How is the productivity of the 1 363 unique authors of the
  corpus distributed, and what invisible-college structure emerges in
  the co-authorship network?
- **RQ3.** What dispersion pattern do the journals cited by NCML follow
  and what is the self-citation rate within the neutrosophic ecosystem?
- **RQ4.** How many topics cluster NCML's production and how did each
  topic's share evolve between 2018-2020 and 2023-2025?
- **RQ5.** How much do the signals of citational impact differ across
  bibliometric sources and what lessons follow for the journal's
  indexing strategy?
- **RQ6.** Does a neutrosophic aggregate of the per-indicator (T, I, F)
  profiles produce author-level or source-level rankings that differ
  from their classical crisp counterparts, and is the difference
  editorially interpretable?

## 1.4 Contribution and structure

The primary contribution is to equip the neutrosophic ecosystem with a
first empirical baseline on NCML, built with a reproducible pipeline
and explicitly-documented limitations. As a secondary contribution, the
paper introduces a neutrosophic framework for bibliometric analysis
that generalises to any journal with multi-source citation evidence,
and validates the framework empirically on the NCML corpus. The code,
intermediate datasets, figures, and SHA-256 checksums are released at
https://github.com/mleyvaz/ncml-bibliometric-2026 under MIT (code) and
CC-BY 4.0 (data) licences.

The paper is organised as follows. Section 2 reviews the theoretical
background on neutrosophic logic and classical bibliometric indicators.
Section 3 presents the framework and the data pipeline. Section 4
reports the classical bibliometric retrospective of NCML. Section 5
reports the neutrosophic analysis of the same corpus, culminating in
the SVNWA aggregated author ranking that operationally distinguishes
neutrosophy from alternative formalisms. Section 6 discusses
implications and engages the Woodall et al. (2025) critique. Section 7
summarises fifteen editorial recommendations. Section 8 concludes.
