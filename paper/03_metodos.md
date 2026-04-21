# 3. Metodos

## 3.1 Diseno del estudio

Se ejecuto un analisis bibliometrico descriptivo de los articulos publicados por
*Neutrosophic Computing and Machine Learning* (NCML) entre el Volumen 1 (2018) y
el Volumen 42 (2026, parcial), siguiendo una adaptacion del protocolo PRISMA
para estudios bibliometricos [TBD cita PRISMA 2020]. La naturaleza editorial de
los autores principales (Editors-in-Chief de NCML y NSS) motivo la incorporacion
de un tercer autor externo al ecosistema neutrosofico para el diseno y
ejecucion del analisis, con el fin de mitigar el sesgo de interpretacion. Todo
el codigo fuente y los datos intermedios estan disponibles en el repositorio
asociado [TBD URL OSF/GitHub].

## 3.2 Fuentes de datos

La fuente primaria fue el listado oficial de articulos de NCML en
`https://fs.unm.edu/NCML/Articles.htm`, scrapeado el 19 de abril de 2026. Se
complementaron los metadatos con cuatro fuentes adicionales:

1. **OpenAlex** (api.openalex.org), para identificadores de autor, afiliaciones
   institucionales y paises, recuento de citas, y clasificacion conceptual.
2. **DataCite** (api.datacite.org), para metadatos de registros Zenodo,
   visualizaciones y descargas.
3. **Google Scholar Metrics**, consultado via Scholar (venue search), para
   obtener indices h5-index y h5-mediana de NCML y revistas hermanas del
   ecosistema neutrosofico.
4. **Google Scholar** (scraping muestreado), para estimar citas por articulo en
   una muestra estratificada.

## 3.3 Construccion del corpus

Se descargaron los PDF completos de los 762 articulos indexados en la pagina
oficial (cobertura 95.5%, 33 URL con encoding corrupto desde origen). Para cada
PDF se extrajo texto completo mediante PyMuPDF 1.27 [TBD cita], y se identificaron
por heuristica las secciones siguientes: resumen en espanol, abstract en ingles,
palabras clave, correos electronicos institucionales y bloque de referencias.
Las tasas de extraccion correcta fueron 91.5% para resumen en espanol, 41% para
abstract en ingles (menor cobertura por monolinguismo historico de la revista),
94% para palabras clave y 95% para bloque de referencias.

## 3.4 Enriquecimiento via API

Las 719 DOIs unicas (en formato `10.5281/zenodo.N`) se consultaron en paralelo
contra OpenAlex y DataCite, obteniendo respuesta positiva en el 93.3% y 97.9%
respectivamente. La concurrencia se limito a 8 hilos con `User-Agent`
identificado para ingresar al pool cortes de ambas APIs. Los registros en
bruto se almacenaron en JSONL para reproducibilidad.

## 3.5 Desambiguacion de autores

Las firmas autorales provenientes de OpenAlex, DataCite y el scraping local se
unificaron mediante un algoritmo de union-find [TBD cita Tarjan 1975] con las
siguientes reglas jerarquicas de equivalencia:

1. Mismo ORCID.
2. Mismo identificador interno de OpenAlex (`author_id`).
3. Misma forma canonica del nombre, definida como: eliminar tildes (NFKD),
   minusculizar, descartar particulas (`de`, `del`, `la`, `los`, `y`, `da`,
   `do`, `van`, `von`), y ordenar los tokens restantes alfabeticamente. Esta
   normalizacion iguala variantes como "Leyva Vazquez, Maikel" y "Maikel
   Leyva Vazquez".
4. Igualdad de llave "inicial del nombre + apellidos ordenados" (por ejemplo
   `m|leyva vazquez`), aplicada solo cuando no hay ORCID conflictivo entre
   las firmas.

El proceso redujo 1.539 firmas raw a 1.363 autores unicos (9.9% de
variantes colapsadas). Para cada cluster se escogio como nombre canonico la
variante mas frecuente. Los 100 clusters mas prolificos se inspeccionaron
manualmente para identificar falsos positivos; no se detectaron merges
erroneos en esa muestra.

## 3.6 Productividad autoral (Lotka)

Se ajusto la ley de Lotka discreta `n(x) ∝ x^(-alpha)` por maxima verosimilitud
[TBD cita Newman 2005, ec. 3.1] sobre la variable *articulos por autor*:

```
alpha = 1 + n · [Σ ln(x_i / (x_min - 0.5))]^(-1)
```

donde el conteo minimo `x_min = 1`. La bondad de ajuste se evaluo con el
estadistico Kolmogorov-Smirnov comparando la CDF empirica con la teorica
basada en la funcion zeta de Hurwitz.

## 3.7 Dispersion de fuentes citadas (Bradford)

Los bloques de referencias extraidos se segmentaron en citas individuales
mediante marcadores `[N]` o `N.` numericos. Para cada cita se identifico la
revista-fuente combinando dos mecanismos:

1. **Busqueda directa** contra una lista curada de 11 revistas candidatas
   (NSS, NCML, IJNS, Plithogenic LC, Fuzzy Sets and Systems, Information
   Sciences, Expert Systems with Applications, Applied Soft Computing,
   Symmetry, IEEE Access, Knowledge-Based Systems).
2. **Cuatro patrones regex heuristicos** para extraer cualquier candidato no
   incluido en la lista curada, principalmente revistas de habla hispana no
   indexadas en Scopus.

Las fuentes se canonicalizaron (minuscula, sin acentos, espacios colapsados) y
se ordenaron por frecuencia descendente. Las zonas de Bradford se definieron
como las tres particiones de la curva acumulada que concentran ~1/3 de las
citas cada una.

## 3.8 Red de coautoria

A partir de la tabla de autorships con identificadores canonicos se construyo
un grafo no dirigido con NetworkX 3.6, donde los nodos son autores, las
aristas indican co-firma y el peso de cada arista es el numero de articulos
coescritos. Las comunidades se detectaron con el algoritmo de Louvain
[TBD cita Blondel et al. 2008] ponderado por peso de aristas. Las metricas
reportadas (densidad, clustering medio, modularidad, componente principal,
diametro) se calcularon sobre el grafo completo; los subgrafos de los autores
con al menos 2 y 4 articulos se usaron para visualizacion.

## 3.9 Modelado de topicos

El corpus textual para modelado de topicos se construyo combinando el resumen
en espanol y el abstract en ingles de cada articulo cuando ambos estaban
disponibles (modo bilingue), o uno solo cuando el otro no fue extraible. Se
descartaron los documentos con texto de menos de 100 caracteres. El pipeline
siguio la arquitectura BERTopic [TBD cita Grootendorst 2022], adaptado para
Python 3.14 debido a incompatibilidades de wheel de HDBSCAN:

1. **Embeddings**: `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensiones).
2. **Reduccion de dimensionalidad**: UMAP a 5 componentes (`n_neighbors=15`,
   `min_dist=0.0`, metrica coseno, `random_state=42`).
3. **Clustering**: KMeans (en lugar de HDBSCAN), con K optimizado mediante
   silhouette score sobre el rango [10, 25]. El valor seleccionado fue K=24
   con silueta 0.43.
4. **Representacion de topicos**: c-TF-IDF sobre unigramas y bigramas,
   stopwords en espanol, ingles y un conjunto especifico de dominio
   (`neutrosofico`, `multicriterio`, `metodo`, etc.) para evitar que
   terminos omnipresentes dominaran las firmas.

Para la evolucion temporal se calculo la matriz `topico x ano` y la
diferencia en share entre los periodos 2018-2020 y 2023-2025, identificando
topicos emergentes y declinantes.

## 3.10 Comparacion de fuentes de citas

La verificacion del impacto citacional se realizo en tres niveles:

1. **Total agregado**: todas las citas OpenAlex a los 762 articulos
   (resultado: 27 citas totales, h-index de revista = 1).
2. **Metrica de revista**: consulta manual del registro de NCML en Google
   Scholar Metrics (resultado: h5-index = 10, h5-mediana = 25 para 2020-2024).
3. **Muestra estratificada** (n = 26): 3 articulos por ano entre 2018-2024 y
   5 de 2025, mas el articulo mas citado de OpenAlex. Para cada titulo se
   ejecuto una consulta controlada en Scholar con User-Agent identificado,
   respetando el limite de tasa mediante pausas aleatorias entre 6 y 14
   segundos. Una instancia fue validada manualmente por discrepancia
   evidente (Vol.10: regex devolvio 204 citas; el valor real verificado en
   la pagina fue 1).

## 3.11 Limitaciones conocidas

Las limitaciones identificadas en los metodos y reportadas explicitamente en
los resultados son:

- **Cobertura de paginas geograficas/institucionales**: OpenAlex retorno
  afiliaciones y paises solo para el 88% de las autorias totales; los mapas
  geograficos estan basados en ese subconjunto (n = 158 autorias).
- **Extraccion heuristica de referencias**: la ausencia de GROBID en el
  pipeline (por razones de despliegue) implica un 46% de referencias sin
  revista-fuente detectable, sesgado hacia citas de libros, tesis, URL y
  revistas hispanas con formato irregular. Los rankings del nucleo son robustos
  pero el conteo de la cola es ruidoso.
- **Scholar citations**: el muestreo n=26 es estadisticamente limitado; las
  cifras agregadas de impacto ~2.500-4.000 citas son extrapolaciones basadas
  en Scholar Metrics y el muestreo, con intervalo de confianza amplio.
- **Encoding del sitio fuente**: la pagina `Articles.htm` contiene
  aproximadamente 400 caracteres U+FFFD (replacement character) en lugar de
  los caracteres originales acentuados. Se reconstruyeron titulos y autores
  mediante comparacion con los PDFs cuando fue posible.

## 3.12 Reproducibilidad

Todo el pipeline esta implementado en Python 3.14 con las siguientes versiones
(selected): `pandas 2.x`, `beautifulsoup4 4.x`, `requests 2.32`, `pymupdf 1.27`,
`sentence-transformers 5.4`, `umap-learn 0.5.12`, `scikit-learn 1.8`,
`networkx 3.6`, `python-louvain 0.16`. Los scripts numerados
(`01_scrape.py` a `18_kpi_dashboard.py`) son idempotentes y pueden re-ejecutarse
en orden para regenerar la totalidad de datos y figuras. Los datos intermedios
(CSV/JSONL) se publican con hash SHA-256 para verificacion de integridad.
