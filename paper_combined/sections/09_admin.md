# Author Contributions

Conceptualization: M.L.V. and F.S. Methodology: M.L.V. and Y.G.V.
Software: M.L.V. (scraping pipeline, API enrichment, classical and
neutrosophic indicator computation, bootstrap, topic modeling, network
analysis, SVNWA aggregation, visualisation in Python). Validation:
Y.G.V. (independent review of code and manual verification of the
Scholar sample) and F.S. (validation of the neutrosophic-theoretical
framework). Formal analysis: M.L.V. and Y.G.V. Data curation: M.L.V.
Writing — original draft: M.L.V. Writing — review and editing: M.L.V.,
Y.G.V., F.S. Visualization: M.L.V. Supervision: F.S. Project
administration: M.L.V. All authors read and approved the final version
of the manuscript. Roles follow the NISO CRediT Contributor Roles
Taxonomy.

# Funding

This research received no external funding, either public or private.
Infrastructure, storage, and authorial time were provided by the
authors.

# Conflict of Interest

Maikel Leyva Vazquez is Editor-in-Chief of *Neutrosophic Computing and
Machine Learning* (NCML) and Florentin Smarandache is Editor-in-Chief
of *Neutrosophic Sets and Systems* (NSS). Yismandry Gonzalez Vargas
(Asociacion Latinoamericana de Ciencias Neutrosoficas, ALCN) holds no
editorial role at either journal. The authors declare this potential
conflict of interest and request the NCML Editorial Board to conduct
peer review exclusively with reviewers external to the NSIA
ecosystem. The authors will not participate in the editorial decision
on this manuscript.

# Acknowledgements

The authors thank the NSIA Publishing community and the Latin-American
Association of Neutrosophic Sciences (ALCN) for facilitating access to
the historical NCML corpus, and the developers of OpenAlex, DataCite,
BERTopic, UMAP, NetworkX, python-louvain, PyMuPDF, and sentence-
transformers, whose open-source tools made this study possible. Any
errors or omissions in the interpretation of the data are the sole
responsibility of the authors.

# Data and Code Availability

The complete pipeline (scraping, PDF download, text extraction,
disambiguation, Lotka and Bradford fits, co-authorship network,
topic modeling, and neutrosophic extensions) is available as open
source at https://github.com/mleyvaz/ncml-bibliometric-2026 under MIT
(code) and CC-BY 4.0 (data) licences. The repository contains twenty-
nine numbered reproducible scripts, the NCML_bibliometric_dataset.xlsx
consolidation (19 sheets covering all analytical tables), the ZIP
backups with the 728 downloaded PDFs and intermediate data, and
the figures in PNG format at 160-170 dpi. Researchers interested in
verifying, replicating, or extending the analysis can clone the
repository and run the scripts in numerical order (01 through 29).
Intermediate datasets are published with SHA-256 integrity hashes.
