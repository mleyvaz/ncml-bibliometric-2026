# Abstract

Classical bibliometrics treats fundamentally uncertain quantities as crisp.
Citation counts collapse when sources disagree by an order of magnitude; the
Lotka exponent is reported as a point estimate even when the
Kolmogorov–Smirnov test rejects the model; Bradford zones partition journals
into hard categories despite obvious boundary cases; document–topic
assignments are reported as winner-take-all even when soft-clustering
algorithms produce graded probabilities; and co-authorship edges weight a
one-paper collaboration identically to a sustained five-paper partnership.
This paper proposes a neutrosophic framework that promotes indeterminacy to
a first-class component of bibliometric measurement. We define
neutrosophic extensions of five classical indicators — the *h*-index, the
Lotka exponent, Bradford zone membership, document–topic membership, and
co-authorship edge weights — using the single-valued neutrosophic triple
(T, I, F). For each indicator we provide a formal definition, a computation
rule that derives the indeterminacy component *from the data rather than
from expert elicitation*, and a worked example. We then present the central
operative test of the framework: we aggregate the five triples across four
dimensions (productivity, citational evidence, co-authorship centrality,
theoretical focus) using the SVNWA operator of Ye (2014) and rank 146
authors of the case-study journal. The neutrosophic ranking diverges
substantially from the classical rank-by-article-count (Kendall τ = 0.20,
top-10 overlap 5/10), re-ordering the journal's visible leadership in ways
that are qualitatively interpretable: prolific authors concentrated in
legal-medical case studies with no cross-source citation evidence fall
sharply, while lower-count but theoretically-focused authors with verified
citations rise to the top. We show that this re-ordering cannot be
reproduced by fuzzy, intuitionistic-fuzzy or probabilistic aggregation
without introducing additional structure equivalent to the (T, I, F)
triple, thus providing operative validation that the framework yields
information unreachable by alternative techniques. The framework is
applied to the 762-article corpus of *Neutrosophic Computing and Machine
Learning* (NCML, 2018–2026). The five indicators jointly reveal: (i) a
neutrosophic *h*-index decomposition T = 0.04, I = 0.50, F = 0.46; (ii) a
bootstrap Lotka profile T = 0, I = 1, F = 0 that reconciles a classical
exponent with a failed shape test; (iii) a graded Bradford nucleus in
which only two journals (NSS, NCML itself) achieve T ≥ 0.85; (iv) 61 % of
documents falling on topic boundaries (T < 0.7); and (v) only 1.8 % of
co-authorship edges rising to T ≥ 0.5 in verified collaboration. The
framework is reproducible, language-agnostic, and applicable to any
bibliographic corpus where multiple sources of evidence must be combined.

**Keywords:** neutrosophic bibliometrics; single-valued neutrosophic
numbers; SVNWA aggregation; Lotka's law; Bradford's law; *h*-index;
author ranking; topic modeling; co-authorship network; uncertainty in
citation counts; Neutrosophic Computing and Machine Learning.
