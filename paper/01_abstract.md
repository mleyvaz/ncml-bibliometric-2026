# Abstract

**Antecedentes.** *Neutrosophic Computing and Machine Learning* (NCML) es la
revista aplicada del ecosistema neutrosofico fundado por Smarandache, con 42
volumenes publicados entre 2018 y 2026 (parcial). No existe una retrospectiva
bibliometrica sistematica de la revista, y la critica reciente de Woodall et
al. (2025) plantea preocupaciones empiricamente evaluables sobre la
concentracion metodologica, citacional y geografica del campo.

**Metodos.** Se construyo un corpus reproducible de 762 articulos mediante
scraping del listado oficial, descarga y extraccion de texto completo con
PyMuPDF, y enriquecimiento via OpenAlex (671/719 DOIs) y DataCite (704/719).
Los autores se desambiguaron por union-find con cuatro reglas jerarquicas
(ORCID, OpenAlex ID, forma canonica, iniciales). Se ajustaron las leyes de
Lotka (MLE) y Bradford (particion en tres zonas), se construyo la red de
coautoria (NetworkX + Louvain) y se modelaron topicos con embeddings
multilingues + UMAP + KMeans sobre 725 resumenes. El impacto citacional se
triangulo entre OpenAlex, Google Scholar Metrics y un muestreo Scholar
estratificado (n=26).

**Resultados.** La revista crecio con CAGR del 42% (2018-2025), de 24 a 250
articulos anuales. Los 1.363 autores unicos siguen una distribucion Lotka
`alpha = 2.03` (clasica) con exceso del 10% de autores one-shot y Pareto del
80% de articulos concentrados en el 17% de autores. La dispersion Bradford
muestra un nucleo de solo cinco revistas que absorben el 33% de las citas
(multiplicador empirico 14.8-30.5, vs 3-5 clasico), con auto-citacion al
ecosistema NSS+NCML del 17.2%. La red de coautoria es extremadamente
fragmentada (modularidad 0.96, componente principal 16%, 81 comunidades
disjuntas). El modelado de topicos identifica 24 clusters tematicos y evidencia
un cambio drastico de identidad: el topico educacion cayo -21.6 puntos
porcentuales entre 2018-2020 y 2023-2025, sustituido por derecho aplicado y
medicina clinica en contextos ecuatorianos. El impacto citacional discrepa en
orden de magnitud entre fuentes: Google Scholar Metrics reporta h5-index=10 y
h5-mediana=25, mientras OpenAlex reporta h=1 (factor 10x). La revista no esta
indexada en Scopus.

**Conclusiones.** NCML presenta una trayectoria de revista aplicada
iberoamericana de alto crecimiento con dependencia estructural de un ecosistema
editorial cerrado. Los tres cuestionamientos de Woodall et al. (2025) se
verifican parcialmente. Se recomiendan cinco acciones editoriales: solicitar
ISSN propio, implementar landing pages con metadatos `citation_*` para
visibilidad Scholar-DOAJ, diversificar geograficamente el Editorial Board,
reservar espacios editoriales para teoria, y monitorear el ratio de
auto-citacion del ecosistema.

**Palabras clave:** bibliometria; revistas emergentes; neutrosofia; Google
Scholar Metrics; OpenAlex; ley de Lotka; ley de Bradford; modelado de
topicos; red de coautoria; retrospectiva editorial.
