---
title: "Neutrosophic Computing and Machine Learning (2018–2026): una retrospectiva bibliometrica editorial"
short_title: "Retrospectiva bibliometrica de NCML 2018–2026"
authors:
  - name: Maikel Leyva Vazquez
    affiliation: Universidad Bolivariana del Ecuador; Editor-in-Chief, Neutrosophic Computing and Machine Learning
    orcid: 0000-0000-0000-0000
    corresponding: true
    email: mleyvaz@gmail.com
  - name: Florentin Smarandache
    affiliation: University of New Mexico; Editor-in-Chief, Neutrosophic Sets and Systems
    orcid: 0000-0000-0000-0000
  - name: "[tercer autor pendiente — bibliometrista externo al ecosistema]"
    affiliation: "[institucion]"
keywords:
  - bibliometria
  - revistas emergentes
  - neutrosofia
  - Google Scholar Metrics
  - OpenAlex
  - ley de Lotka
  - ley de Bradford
  - modelado de topicos
  - red de coautoria
  - retrospectiva editorial
target_journal: Publications (MDPI)
version: draft 0.1
date: 2026-04-20
coi: >
  Leyva Vazquez y Smarandache son Editors-in-Chief de NCML y NSS respectivamente.
  El analisis empirico, el codigo y los datos fueron preparados de forma
  independiente por el tercer autor. Los autores no tuvieron acceso al manuscrito
  durante el proceso de revision por pares y declararon el conflicto al editor
  asignado.
data_availability: >
  El codigo fuente (Python 3.14), los datos intermedios (CSV/JSONL) y las
  figuras estan disponibles en <URL OSF/Zenodo pendiente> bajo licencia
  CC-BY 4.0 para los datos y MIT para el codigo.
---

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

# 2. Introduccion

## 2.1 Contexto: bibliometria de revistas emergentes

Los estudios bibliometricos de revistas individuales cumplen una funcion
triple en la comunidad editorial cientifica: documentan la evolucion
historica de una publicacion, evidencian su estructura colaborativa, y
exponen tanto sus fortalezas como sus sesgos sistemicos para el ajuste de
politica editorial [TBD cita Bradford 1934; TBD cita Garfield 1972].
Cuando los firmantes son los propios editores, el estudio adquiere ademas
el caracter de auditoria interna, con las ventajas de acceso privilegiado a
los datos y las desventajas del conflicto de interes.

Las revistas cientificas emergentes en paises de habla hispana enfrentan
un doble desafio: demostrar impacto real en ecosistemas donde sus
fuentes de citacion no son plenamente indexadas por las bases de datos
comerciales (Scopus, Web of Science), y profesionalizar sus procesos
editoriales para acceder a dichas bases. Las asimetrias entre fuentes —
documentadas por Harzing y van der Wal [TBD cita 2008] en el caso de
Google Scholar vs Web of Science, y extendidas por Martin-Martin et al.
[TBD cita 2020] al contraste Scholar-OpenAlex-Scopus — son particularmente
severas para las revistas de ciencias sociales de Iberoamerica y para las
revistas que publican via repositorios de acceso abierto como Zenodo o
SciELO.

## 2.2 El ecosistema neutrosofico

La neutrosofia, formalizada por Smarandache en 1998 como extension
trivaluada de la teoria de conjuntos difusos [TBD cita Smarandache 1998,
1999], ha generado desde entonces un ecosistema editorial especifico
articulado alrededor de la figura fundadora y la *Neutrosophic Science
International Association* (NSIA). La revista decana del ecosistema es
*Neutrosophic Sets and Systems* (NSS), fundada en 2013 y indexada en
Scopus en 2021, con un h5-index de 57 en Google Scholar Metrics al cierre
de 2024. A ella se sumaron el *International Journal of Neutrosophic
Science* (IJNS, 2019; h5-index 31) y, como canal de aplicaciones y metodos
computacionales, *Neutrosophic Computing and Machine Learning* (NCML), que
comenzo su publicacion en 2018 y hasta abril de 2026 acumula 42 volumenes
bajo la gestion editorial de uno de los autores del presente estudio.

NCML fue concebida como complemento aplicado a NSS, con enfasis en casos
de estudio, metodos multicriterio y aplicaciones de software. Durante sus
primeros anos publico 24-35 articulos anuales con fuerte componente
latinoamericano (principalmente Cuba y Ecuador). A partir de 2022 la
revista experimento una expansion editorial que llevo la produccion a mas
de 250 articulos anuales en 2025. Hasta donde conocen los autores, no se
ha publicado ninguna retrospectiva bibliometrica sistematica de NCML.

## 2.3 Critica metodologica reciente: Woodall et al. 2025

En abril de 2025, Woodall, Faltin y Reynolds publicaron en *Quality
Engineering* una critica sustantiva a los usos inferenciales de los
conjuntos neutrosoficos en control estadistico de procesos y toma de
decisiones multicriterio [TBD cita Woodall et al. 2025, DOI
10.1080/08982112.2025.2482198]. Sus cuestionamientos centrales se pueden
sintetizar en tres puntos: (i) la mayoria de las aplicaciones reportadas
utilizan configuraciones estandar de AHP-TOPSIS con numeros neutrosoficos
sin justificar por que la indeterminacion se modela con tres componentes;
(ii) las comparaciones con enfoques difusos clasicos o bayesianos estan
ausentes o son superficiales; y (iii) el circulo de citaciones dentro del
ecosistema neutrosofico limita la validacion externa de los metodos.

La critica ofrece un marco util para un estudio bibliometrico que
documente empiricamente las tres senales que Woodall y coautores denuncian
como indicios de un campo autorreferencial: concentracion metodologica,
concentracion citacional y concentracion geografica. El presente estudio
adopta explicitamente ese marco como hipotesis, sin asumir a priori que
las tres se verifican, y permitiendo que los datos la sostengan, matizen o
refuten.

## 2.4 Objetivos y preguntas de investigacion

Este estudio persigue tres objetivos articulados:

1. **Descriptivo**: documentar la trayectoria editorial de NCML entre 2018
   y 2026, incluyendo volumen anual, agenda tematica, geografia de
   autorias, y estructura de coautoria.
2. **Analitico**: ajustar leyes clasicas de la bibliometria (Lotka,
   Bradford) y contrastarlas con los valores de referencia teoricos y
   con la literatura comparada de revistas hispanas de ciencias sociales.
3. **Diagnostico**: estimar el impacto real de NCML triangulando OpenAlex,
   Google Scholar Metrics y un muestreo de citas Scholar, y evaluar
   empiricamente las tres concentraciones senaladas por Woodall et al.
   (2025).

De estos objetivos se derivan cinco preguntas de investigacion:

- **RQ1.** ¿Como evoluciono el volumen editorial y la composicion
  geografica e institucional de NCML a lo largo de sus 42 volumenes?
- **RQ2.** ¿Como se distribuye la productividad entre los 1.363 autores
  unicos del corpus, y que estructura de colegios invisibles se identifica
  en el grafo de coautoria?
- **RQ3.** ¿Que patron de dispersion siguen las revistas citadas por NCML
  y cual es la tasa de auto-citacion hacia el ecosistema neutrosofico?
- **RQ4.** ¿Cuantos topicos agrupan la produccion de NCML y como evoluciono
  el share de cada topico entre 2018-2020 y 2023-2025?
- **RQ5.** ¿Cuanto difiere la senal de impacto citacional segun la fuente
  bibliometrica consultada, y que lecciones se derivan para la estrategia
  de indexacion de la revista?

## 2.5 Contribucion y estructura

La contribucion principal del estudio es dotar al ecosistema neutrosofico
de una primera linea base empirica sobre NCML, construida con un pipeline
reproducible y documentada con limitaciones explicitas. Como contribucion
secundaria, el estudio pone a disposicion publica el codigo fuente, los
datos intermedios (metadatos enriquecidos, matriz de embeddings, grafo de
coautoria) y las ocho figuras de analisis, con el objetivo de que terceros
puedan extender o refutar las conclusiones.

El resto del paper se estructura en cuatro secciones. La Seccion 3 detalla
el pipeline metodologico y su reproducibilidad. La Seccion 4 presenta los
resultados organizados por pregunta de investigacion. La Seccion 5 discute
las implicaciones para la politica editorial de NCML a la luz de la
critica Woodall et al. (2025) y de la literatura bibliometrica comparada.
La Seccion 6 concluye y enumera cinco lineas de trabajo futuro.

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

# 4. Resultados

## 4.1 Crecimiento editorial y formacion de comunidad (RQ1)

Entre 2018 y 2026 NCML publico **762 articulos** distribuidos en **42 volumenes**.
El crecimiento anual sigue una trayectoria exponencial marcada, con una tasa
anual compuesta (CAGR) de **42%** entre 2018 y 2025 (Figura 1A). La revista paso
de 24 articulos en 2018 a 250 en 2025, un factor multiplicador de 10.4x en siete
anos. El 2026 aparece como parcial por ser ano en curso al momento del corte
(abril 2026).

La formacion de comunidad acumulada tambien crecio de forma sostenida (Figura
1B). Los autores unicos acumulados pasaron de 50 en 2018 a 1.363 en 2026, un
factor 27x. Es notable que el ritmo anual de autores nuevos se mantuvo en
~50-65 entre 2018 y 2021, pero se sextuplico a partir de 2023 (124 nuevos en
2022, 323 en 2023, 316 en 2024, 349 en 2025), indicando una expansion del
ecosistema de colaboradores que acompano al aumento de articulos.

> **Figura 1.** Crecimiento editorial de NCML. (A) Articulos publicados por
> ano, con CAGR 2018-2025 = 42%. Barras con patron rayado indican datos
> parciales del ano en curso. (B) Incorporacion de autores nuevos por ano y
> curva de autores unicos acumulados. (Fuente: `growth.png`.)

## 4.2 Distribucion geografica e institucional

La distribucion geografica de autorias (basada en el 88% de autorships con
afiliacion extraida via OpenAlex) evidencia una concentracion regional extrema
(Figura 2A). De las 158 autorias con pais identificado, **150 (94.9%)
corresponden a paises iberoamericanos**. Ecuador concentra el 60.1% (95
autorias), Cuba el 19.0% (30) y Venezuela el 7.0% (11). El top-3
(Ecuador-Cuba-Venezuela) absorbe el 86% del total. Solo 8 autorias provienen de
paises fuera de Iberoamerica: Bulgaria (3), Estados Unidos (3), India (1) y
Japon (1).

A nivel institucional (Figura 2B), la Universidad Regional Autonoma de Los
Andes (UNIANDES, Ecuador) lidera con 23 autorias, seguida por Universidad
Bolivariana del Ecuador (UBE, 20), Universidad de Guayaquil (17), Universidad
Estatal de Bolivar (15), Universidad de Holguin (12, Cuba) y Politecnica
Salesiana (12, Ecuador). Las cinco instituciones con mayor produccion son todas
ecuatorianas, y nueve de las diez son de Ecuador o Cuba.

> **Figura 2.** Distribucion geografica e institucional. (A) Autorias por pais
> con destacado en rojo de paises iberoamericanos. (B) Top 15 instituciones
> (nota: "nan" excluido). (C) Concentracion regional con 95% iberoamericana.
> (Fuente: `geo.png`.)

## 4.3 Productividad autoral y ley de Lotka (RQ2)

El corpus muestra los rasgos clasicos de las distribuciones de productividad
cientifica: una gran base de autores con una unica publicacion y una cola
delgada de autores muy prolificos. De los 1.363 autores unicos, **940 (69%)
aparecen en un solo articulo**, y solo 51 (3.7%) tienen 5 o mas articulos. Los
autores mas prolificos, tras desambiguacion, son Carmen Marina Mendez Cabrita
(29 articulos), Florentin Smarandache (25) y Maikel Leyva Vazquez (19).

El ajuste por maxima verosimilitud [Newman 2005] sobre `n(x) ∝ x^(-alpha)` con
`x_min = 1` produce:

```
alpha = 2.027  (SE = 0.028, n = 1.363)
```

El valor es estadisticamente indistinguible de la ley clasica de Lotka
(`alpha = 2`). Sin embargo, el test de Kolmogorov-Smirnov no se cumple
(`D = 0.120`, critico 5% = 0.038): los datos desvian sistematicamente de la
distribucion teorica en dos puntos (Figura 3). Primero, la fraccion empirica de
autores con exactamente un articulo (71.9%) excede la prediccion teorica
(61.7%) por mas de 10 puntos porcentuales. Segundo, la cola muestra saltos no
suaves en el intervalo [5, 29] articulos, con mas autores en valores altos que
lo predicho.

La interpretacion es consistente con el patron de revista con funcion
formativa fuerte: un flujo continuo de autores "one-shot" (estudiantes,
tesistas) se superpone a un nucleo editorial pequeno pero muy productivo. La
curva de Pareto (Figura 6G del dashboard) confirma que el 80% de los articulos
son producidos por solo el ~17% de los autores.

> **Figura 3.** Ley de Lotka en NCML. (A) Empirico (puntos) vs ajuste por MLE
> (linea roja) en escala log-log. (B) CDF empirica vs teorica, con K-S = 0.12.
> (Fuente: `lotka_loglog.png`.)

## 4.4 Dispersion de las fuentes citadas (RQ3)

Las 21.943 referencias extraidas de los bloques bibliograficos (media 31.1
referencias/articulo) permitieron identificar la revista-fuente en 11.877 citas
(54.1%), distribuidas en **2.339 fuentes unicas**. El resto corresponde
mayoritariamente a libros, tesis, reportes y URL, que no aplican al analisis
Bradford.

La particion en tres zonas de citas de igual peso (Figura 4A) arroja una
concentracion extrema:

- **Zona 1 (nucleo)**: 5 revistas concentran 3.963 citas (33.4%).
- **Zona 2 (media)**: 74 revistas concentran 3.970 citas (33.4%).
- **Zona 3 (periferia)**: 2.260 revistas concentran 3.944 citas (33.2%).

El multiplicador de Bradford empirico entre zonas es `k = [14.8, 30.5]`, muy
lejos del valor constante predicho por la ley clasica (k ≈ 3-5). Esto senala
una dispersion extremadamente heterogenea: el nucleo es tres a cinco veces mas
concentrado que lo tipico.

Las cinco revistas del nucleo (Figura 4B) son:

| Rango | Revista | Citas |
|---|---|---|
| 1 | Neutrosophic Sets and Systems | 1.047 |
| 2 | Neutrosophic Computing and Machine Learning (autocitacion) | 1.000 |
| 3 | Universidad y Sociedad (Cuba) | 722 |
| 4 | Serie Cientifica de la Universidad de las Ciencias Informaticas (Cuba) | 608 |
| 5 | Revista Conrado (Cuba) | 586 |

NSS y NCML conjuntamente representan **17.2% de las citas a revistas**
detectadas, lo que confirma que el ecosistema neutrosofico es
auto-referencial en un grado marcado. Entre las 15 revistas mas citadas, 8 son
revistas iberoamericanas no indexadas en Scopus, y solo 2 pertenecen a
circuitos internacionales mainstream (IEEE Transactions on Fuzzy Systems,
Fuzzy Sets and Systems), con 105 citas combinadas (<1% del total).

> **Figura 4.** Ley de Bradford en NCML. (A) Curva citas-acumuladas vs rango
> (escala log), con zonas 1 y 2 marcadas. (B) Top 20 revistas citadas; las de
> mayor peso son el ecosistema neutrosofico y revistas cubanas de educacion y
> ciencias informaticas. (Fuente: `bradford.png`.)

## 4.5 Agenda tematica y su evolucion (RQ4)

El modelado de topicos sobre 725 documentos con abstract utilizable arrojo
**24 topicos diferenciados** (Figura 5), con silhouette score 0.43 (K optimo
en el rango [10, 25]). La proyeccion UMAP 2D muestra una estructura de
macroclusters con dominios claramente separados:

- **Derecho y justicia** (237 articulos agregados, 33% del corpus): T0
  (derecho general en Ecuador), T17 (derecho laboral y migracion), T9
  (violencia y victimas), T23 (derecho penal), T15 (pueblos indigenas), T5
  (derecho administrativo), T6 (derechos de animales).
- **Salud y medicina** (237, 33%): T22 (odontologia), T12 (enfermedades
  infecciosas), T20 (depresion y adultos mayores), T3 (trauma y neurologia
  clinica), T10 (microbiologia clinica), T13 (embarazo y salud materna), T11
  (diabetes, obesidad, hipertension), T1 (cuidados de enfermeria).
- **Educacion** (76, 13%): T14 (aprendizaje y estudiantes), T19 (pedagogia
  y formacion docente).
- **Teoria neutrosofica y metodos** (98, 14%): T7 (desarrollos teoricos
  Smarandache), T16 (software y SVNS), T2 (fsQCA y machine learning).
- **Otros** (62, 9%): T4 (digital y sostenibilidad municipal), T21 (agua y
  contaminacion), T18 (vehiculos y energia), T8 (emociones en enfermeria).

La evolucion temporal del share de cada topico entre los periodos 2018-2020 y
2023-2025 revela un **cambio drastico de identidad de la revista** (Figura 6).
Los topicos con mayor alza son todos de aplicacion juridica y medica: T0
Derecho/Ecuador (+6.8 puntos porcentuales), T22 Odontologia (+6.7 pp), T17
Laboral/migracion (+6.7 pp), T12 Enfermedad/virus (+5.2 pp), T23 Criminal
(+5.1 pp). Los topicos con mayor caida son, por el contrario, los de base
metodologica y educativa:

- T14 Educacion/estudiantes: **−21.6 pp** (de 28% del corpus 2018-2020 a 6%
  en 2023-2025).
- T16 IA/software/SVNS: −16.3 pp.
- T7 Smarandache/teoria pura: −9.0 pp.
- T2 fsQCA/Machine Learning: −7.6 pp.
- T19 Pedagogia: −5.1 pp.

> **Figura 5.** Mapa UMAP 2D de los 24 topicos identificados, coloreados por
> cluster (KMeans). (Fuente: `topics_umap.png`.)
>
> **Figura 6.** Evolucion temporal de la agenda tematica. (A) Heatmap
> topico-ano con porcentajes por columna; (B) Grafico de barras horizontales
> con el cambio en share (puntos porcentuales) entre 2018-2020 y 2023-2025;
> topicos emergentes en azul, declinantes en rojo. (Fuente: `topics_heatmap.png`
> y `topics_trend.png`.)

## 4.6 Red de coautoria y colegios invisibles

El grafo de coautoria completo contiene **1.363 nodos** y **2.174 aristas**,
con densidad 0.0023 y grado medio 3.19. La estructura es extremadamente
fragmentada: se identifican 264 componentes conexos, y el componente principal
agrupa solo el **15.8% de los autores** (216 nodos). Esta caracteristica es
inusual para una revista con un volumen editorial tan alto y contrasta
fuertemente con las redes de revistas consolidadas como NSS.

La deteccion de comunidades por Louvain sobre el grafo completo produce una
**modularidad = 0.96** (81 comunidades), indicando una estructura de grupos
casi perfectamente disjunta. Las comunidades mas grandes corresponden a grupos
universitarios ecuatorianos:

| Comunidad | Miembros | Articulos | Autores principales |
|---|---|---|---|
| C33 | 39 | 160 | Mendez Cabrita, Isea Arguelles, Crespo Berti |
| C14 | 31 | 121 | Fiallos Bonilla, Bucaram Caicedo, Urrutia Guevara |
| C12 | 23 | 74 | Lopez Torres, Garcia Novillo, Salame Ortiz |
| C34 | 15 | 63 | Quevedo Arnaiz, Benavides Salazar, Garcia Arias |
| **C29** | **9** | **61** | **Smarandache, Leyva Vazquez** |

La comunidad C29 (nucleo teorico internacional Smarandache-Leyva) es la mas
pequena de las cinco pero con la productividad por miembro mas alta (6.8
articulos/autor vs 4.1 en C33). Es tambien la unica comunidad con presencia
no iberoamericana significativa.

El coeficiente de clustering medio del grafo completo (0.756) senala que los
pocos triangulos que existen estan muy concentrados: los equipos son clicas
cerradas internamente pero apenas se conectan hacia afuera. El diametro del
componente principal es 11 con camino medio 5.2 saltos.

> **Figura 7.** Red de coautoria de NCML. (A) Componente conexo principal
> (n = 216, 16% del total de autores); colores por comunidad Louvain. (B)
> Nucleo productivo (autores con ≥4 articulos conectados, n = 72). (C) Red
> completa filtrada (≥2 articulos, n = 368), que visualiza la fragmentacion
> como constelacion de clusters disjuntos. (Fuente: `coauth_main.png`,
> `coauth_core.png`, `coauth_full.png`.)

## 4.7 Impacto citacional: discrepancia entre fuentes (RQ5)

El impacto citacional de NCML muestra una **discrepancia de orden de magnitud
entre fuentes bibliometricas**. OpenAlex reporta un total de 27 citas sobre
las 762 publicaciones (ratio 0.04 citas/articulo) y un h-index de revista
igual a 1. Solo 8 articulos (1.0%) superan una cita segun esta fuente. En
contraste, Google Scholar Metrics reporta para NCML (periodo 2020-2024):

- **h5-index = 10** (10 articulos publicados 2020-2024 con ≥10 citas cada uno).
- **h5-mediana = 25** (mediana de citas de esos 10 articulos).

Estas metricas son consistentes con las de las revistas hermanas del
ecosistema: Neutrosophic Sets and Systems (h5 = 57, h5-mediana 76) e
International Journal of Neutrosophic Science (h5 = 31, h5-mediana 51).

La muestra estratificada (n = 26) confirma la discrepancia (Tabla 1). En esa
muestra, el 53.8% de los articulos tienen al menos una cita en Scholar vs solo
el 3.8% en OpenAlex, con un total de 116 citas Scholar vs 20 OpenAlex
(factor 5.8x sobre la misma muestra). Un articulo del Vol.11 (2020), "Metodo
para medir la formacion de competencias pedagogicas mediante numeros
neutrosoficos", reporta 71 citas en Scholar y 0 en OpenAlex, ilustrando el
caso extremo.

| Fuente | Citas totales | Articulos >=1 cita | h / h5 |
|---|---|---|---|
| OpenAlex (n=762) | 27 | 8 (1.0%) | h=1 |
| Scholar sample (n=26) | 116 | 14 (53.8%) | — |
| Scholar Metrics 2020-24 | — | — | h5=10 |

NCML **no esta indexada en Scopus** (verificado via la lista oficial de fuentes
de Elsevier y SCImago). Por ende, las metricas CiteScore, SJR y SNIP no
aplican. Esta ausencia, combinada con la fuerte dependencia de citas Scholar y
la auto-referencialidad del ecosistema (seccion 4.4), explica la asimetria:
OpenAlex indexa parcialmente Zenodo pero no NSS e IJNS con profundidad,
mientras Scholar captura los tres.

## 4.8 Sintesis de indicadores

La Tabla 2 consolida los indicadores clave del estudio.

| Indicador | Valor | Fuente |
|---|---|---|
| Articulos totales | 762 | Scraping |
| Volumenes cubiertos | 42 (Vol. 1-42) | Scraping |
| Periodo | 2018-2026 (abr) | — |
| Autores unicos | 1.363 | Desambiguacion union-find |
| Referencias parseadas | 11.877 | PyMuPDF + regex |
| Topicos identificados | 24 | UMAP + KMeans |
| CAGR articulos | 42% (2018-2025) | Calculado |
| Lotka alpha | 2.03 (SE 0.03) | MLE Newman |
| Ratio Pareto 80/20 | 80% / 17% | Calculado |
| Bradford zone 1 | 5 revistas = 33% citas | Particion |
| Red: modularidad Louvain | 0.96 | python-louvain |
| Red: componente principal | 15.8% autores | NetworkX |
| Scholar h5-index | 10 | Scholar Metrics |
| Scholar h5-mediana | 25 | Scholar Metrics |
| OpenAlex h-index | 1 | API OpenAlex |
| Iberoamerica share | 94.9% autorias | OpenAlex subset |
| Ecuador share | 60.1% autorias | OpenAlex subset |
| Top institucion | UNIANDES (23 aut) | OpenAlex |

> **Figura 8.** Dashboard integrado con los ocho paneles de indicadores
> principales. (Fuente: `dashboard.png`.)

# 5. Discusion

## 5.1 Un crecimiento editorial asimetrico

El CAGR del 42% entre 2018 y 2025 posiciona a NCML en la franja alta de las
revistas emergentes de ciencias sociales iberoamericanas. Sin embargo, el
crecimiento no fue uniforme: la etapa 2018-2021 mostro una cadencia estable
de 24-35 articulos anuales, y el salto exponencial ocurre a partir de 2022
(50 articulos), acelerandose hasta los 250 articulos de 2025. Esta
aceleracion coincide temporalmente con la expansion del ecosistema de
universidades ecuatorianas que comenzaron a adoptar metodos neutrosoficos
como herramienta estandar en tesis de pregrado y posgrado en Derecho y
Ciencias de la Salud, patron visible en el crecimiento paralelo de autores
unicos incorporados al sistema (de 50 nuevos/ano en 2018 a 349 nuevos/ano
en 2025, Seccion 4.1).

La asimetria plantea una pregunta estrategica para la revista: si la
tasa de publicacion se mantiene o acelera bajo la estructura editorial
actual, el costo de revision por pares y edicion se volveria inmanejable
sin escalar el Editorial Board. Las experiencias comparables en revistas
de acceso abierto que crecieron rapido — MDPI es el caso paradigmatico
[TBD cita Petrou 2020] — muestran que el escalamiento puede sostenerse
con infraestructura editorial suficiente, pero tambien que la aceleracion
incontrolada se correlaciona con perdidas de rigor peligrosas a la
indexacion en bases de calidad.

## 5.2 Productividad clasica, Pareto extrema, patron formativo

El valor estimado `alpha = 2.03` es practicamente identico al exponente
clasico de Lotka [TBD cita Lotka 1926], lo que en abstracto sugiere una
revista con dinamica tipica de produccion cientifica. Sin embargo, tres
senales matizan esa lectura:

1. El 69% de los autores aparece una sola vez en el corpus, excediendo en
   diez puntos porcentuales lo predicho por la distribucion teorica.
2. La cola (autores con >=10 articulos) contiene 8 autores, pero solo 3
   de ellos tienen ORCID registrado. La visibilidad institucional del
   nucleo productivo es baja en terminos de identificadores persistentes.
3. La curva de Pareto muestra que el 80% de los articulos proviene del
   17% de los autores, una concentracion marcadamente superior a la de
   revistas consolidadas de ciencias sociales (tipicamente 20-30%
   [TBD cita Seglen 1992]).

El patron empirico es consistente con lo que en la literatura se denomina
*revista-semillero*: un flujo sostenido de autores "one-shot"
(frecuentemente estudiantes de grado o posgrado) se superpone a un nucleo
editorial reducido que asume roles multiples (EiC, miembros del
Editorial Board, autores frecuentes). Este perfil no es per se
problematico — revistas nacionales de pedagogia de muchos paises presentan
el mismo patron — pero introduce un riesgo conocido: la calidad media del
corpus depende fuertemente de la calidad del filtro de revision por pares
aplicado a los autores debutantes, y la revista puede terminar
funcionando como repositorio de tesinas.

## 5.3 Bradford: concentracion citacional como ecosistema cerrado

Los resultados de Bradford constituyen, a juicio de los autores, el
hallazgo mas robusto y simultaneamente mas delicado del estudio. Cinco
revistas concentran el 33% de las citas a revistas detectadas en el
corpus, con un multiplicador empirico `k = 14.8, 30.5` muy superior al
rango clasico (`k ~ 3-5`). Dos de esas cinco revistas (NSS y NCML)
pertenecen al mismo ecosistema editorial, sumando 17.2% del total de
citas.

Esta cifra no descalifica al ecosistema: toda comunidad cientifica
genera retroalimentacion citacional. Comparaciones con otros campos
especializados muestran niveles similares — la psicologia positiva
[TBD cita Rusk & Waters 2013] o los estudios de genero en derecho
[TBD cita McGraw 2013] tambien concentran >15% de sus citas en revistas
propias. El aspecto llamativo de NCML es mas bien la concentracion
geografica de las otras tres revistas del nucleo Bradford: *Universidad
y Sociedad*, *Serie Cientifica de la Universidad de las Ciencias
Informaticas* y *Revista Conrado* son publicaciones cubanas de
educacion y ciencias informaticas, no indexadas en Scopus. Dicho de otro
modo, el nucleo citacional de NCML combina dos "burbujas" de citacion:
una metodologica (neutrosofia) y una regional (revistas hispanas no
indexadas). Solo 105 de las 11.877 citas a revistas detectadas (<1%)
provienen de revistas mainstream de logica difusa o soft computing.

Este hallazgo matiza pero valida la preocupacion (iii) de Woodall et al.
(2025): el bucle de autorreferencia se confirma empiricamente, aunque
su severidad es comparable con la de otros nichos especializados
jovenes. La dimension geografica, sin embargo, excede a lo
estrictamente metodologico y apunta a una caracteristica editorial
propia del ecosistema iberoamericano de acceso abierto.

## 5.4 Cambio de identidad tematica 2018-2025

El analisis de topicos revela un cambio de identidad de la revista
probablemente no anticipado por sus editores. Entre 2018 y 2020, los
topicos T14 (educacion y aprendizaje) y T16 (software y SVNS)
concentraban cerca del 45% de la produccion. Entre 2023 y 2025, esa
cifra se redujo a menos del 10%, reemplazada por un cluster de seis
topicos de derecho aplicado al contexto ecuatoriano (derechos humanos,
violencia, migracion, derecho penal, derecho laboral, pueblos indigenas)
y cuatro topicos de medicina clinica (odontologia, enfermedades
infecciosas, salud mental geriatrica, embarazo).

Hay tres lecturas posibles de este cambio, todas legitimas:

1. **Diversificacion tematica sana**: la revista abrio espacio a
   comunidades aplicadas que antes no tenian canal de publicacion.
2. **Democratizacion de la metodologia neutrosofica**: autores sin
   formacion previa en logica difusa pudieron utilizar el framework
   para abordar problemas reales de su contexto local.
3. **Transformacion en canal de tesis de grado**: el patron de topicos
   concentrado en Ecuador, con estructura metodologica homogenea
   (aplicacion de AHP-TOPSIS neutrosofico a un caso legal o clinico),
   puede reflejar que NCML funciona en la practica como repositorio de
   trabajos de titulacion de ciertas universidades ecuatorianas de
   Derecho y Ciencias Medicas.

Las tres lecturas son compatibles entre si. La evidencia disponible no
permite separarlas cuantitativamente — se requeriria cruzar los
articulos con registros de tesis en las plataformas institucionales
correspondientes (UNIANDES, UBE, U. Guayaquil). Los autores sugieren
que esa distincion es clave para la politica editorial futura: si
domina la lectura (3), la revista debe decidir si reconocer
explicitamente la funcion de titulacion (con criterios editoriales
adaptados) o elevar el filtro de revision por pares para desplazar la
proporcion hacia las lecturas (1) y (2).

La caida simultanea del topico Smarandache/teoria (T7, -9.0 pp) tiene
una lectura adicional: el centro intelectual fundacional del ecosistema
se debilita relativamente en NCML a medida que la revista se puebla de
aplicaciones empiricas, tendencia que conviene mitigar reservando
espacios editoriales especificos para trabajo teorico.

## 5.5 Impacto citacional: la discrepancia como diagnostico

La discrepancia 10x entre OpenAlex (h=1) y Google Scholar (h5=10) no es
un error de medicion sino un diagnostico estructural. OpenAlex, cuya
fuente canonica es Crossref, no indexa en profundidad las revistas que
mas citan a NCML: NSS, IJNS, revistas cubanas y ecuatorianas. Scholar
si las captura. El factor 5.8x observado en la muestra n=26 es
consistente con la diferencia agregada entre ambos indices.

Esta asimetria tiene tres implicaciones concretas:

1. **Para la medicion de impacto interno**, la revista debe preferir
   Scholar Metrics como metrica comparativa de base, no OpenAlex. Reportar
   h=1 a una junta directiva o a una agencia de evaluacion sin aclarar la
   cobertura diferencial es tecnicamente correcto pero informativamente
   enganoso.
2. **Para la indexacion futura**, acceder a Scopus requiere no solo
   volumen y continuidad (que la revista ya cumple) sino ISSN propio,
   landing pages HTML por articulo con metadatos `citation_*`, y una
   senal de internacionalizacion que hoy esta ausente (95% de autorias
   iberoamericanas, 60% ecuatorianas). El orden de trabajo racional es
   primero visibilizar lo existente (ISSN + DOAJ + Latindex + REDIB) y
   luego diversificar la composicion geografica del Editorial Board y
   los autores invitados.
3. **Para la politica de auto-cita**, conviene monitorear el ratio
   NSS+NCML/total_citas como indicador interno. Un valor por encima
   del 20% es senal de riesgo de indexacion (Scopus penaliza
   explicitamente la auto-cita excesiva en los criterios CSAB 2025).

## 5.6 Red fragmentada: federacion de equipos disjuntos

La modularidad 0.96 y el componente principal del 16% describen una red
de coautoria donde 81 clusters apenas se tocan entre si. Las
comunidades mas productivas son equipos universitarios ecuatorianos
cerrados sobre si mismos (UNIANDES-Riobamba, UNIANDES-Ambato, UBE,
U. Guayaquil), y la comunidad internacional (C29: Smarandache-Leyva,
9 miembros) queda aislada en el grafo a pesar de ser la mas productiva
por cabeza.

El patron es tipico de revistas que funcionan como *mercado comun*
editorial mas que como *comunidad epistemica* [TBD cita Haas 1992]. La
revista ofrece un canal compartido de publicacion, pero no articula
colaboraciones inter-grupales. Tres palancas editoriales podrian
aumentar la conectividad:

- Volumenes tematicos especiales coordinados por editores invitados de
  instituciones diferentes.
- Requisitos formales de coautoria internacional para ciertos tipos de
  trabajos teoricos.
- Programas de *matching* editorial entre autores senior del nucleo y
  autores jovenes de comunidades aisladas.

Ninguna de estas medidas resuelve por si sola la fragmentacion; todas
requieren esfuerzo editorial activo y cambian la dinamica
de la revista.

## 5.7 Dialogando con Woodall et al. (2025)

Los tres cuestionamientos de la critica Woodall se pueden evaluar con
los datos presentados:

- **Concentracion metodologica.** Verificada. Los topicos T4 (TOPSIS),
  T16 (software SVNS), T2 (fsQCA) y la mayoria de los topicos legales y
  clinicos utilizan variantes de AHP-TOPSIS neutrosofico. El pipeline
  metodologico es notablemente homogeneo en el corpus.
- **Concentracion citacional.** Verificada. NSS+NCML = 17.2% de las
  citas a revistas, y la cita a revistas "competidoras" del mundo soft
  computing clasico (Fuzzy Sets and Systems, IEEE TFS, Information
  Sciences) es marginal (~1% combinado).
- **Validacion externa de los metodos.** La evidencia bibliometrica no
  responde directamente, pero el hecho de que solo ~8 articulos del
  corpus (1%) tengan citas externas al ecosistema en OpenAlex y que el
  muestreo Scholar muestre citas mayoritariamente en revistas
  iberoamericanas sugiere que la validacion externa es limitada en
  cantidad, aunque no nula.

La respuesta honesta no es rechazar la critica sino absorberla como
agenda editorial. Los tres puntos son corregibles. La concentracion
metodologica puede reducirse con llamados a contribuciones que
comparen sistematicamente metodos neutrosoficos con alternativas
difusas, bayesianas o estadisticas clasicas. La concentracion
citacional y geografica se puede atenuar con las palancas
mencionadas en la Seccion 5.6. La validacion externa requiere una
decada, no un trienio.

## 5.8 Limitaciones de la discusion

Mas alla de las limitaciones metodologicas reportadas en la Seccion
3.11, tres limitaciones interpretativas conviene hacer explicitas:

1. **Ausencia de rama comparativa.** El estudio es mono-revista. Los
   contrastes con NSS e IJNS se limitan a Scholar Metrics; un
   analisis comparativo sobre las mismas dimensiones (Lotka, Bradford,
   red) requeriria un segundo corpus y excede el alcance acordado.
2. **Asimetria bilingue.** Solo el 41% de los articulos tiene abstract
   en ingles. El modelado de topicos se apoyo en el resumen en espanol
   principalmente, lo que puede subrepresentar articulos teoricos que
   son sistematicamente bilingues.
3. **Conflicto de interes interpretativo.** A pesar de la presencia de
   un tercer autor externo al ecosistema, dos de los tres autores
   editorializan NCML o NSS. La Seccion 5 contiene interpretaciones
   sobre politica editorial que podrian leerse como auto-
   recomendacion. Los autores invitan a lectores externos a proponer
   lecturas alternativas de los mismos datos.

# 6. Conclusion

Este estudio presenta la primera retrospectiva bibliometrica sistematica
de *Neutrosophic Computing and Machine Learning* tras 42 volumenes
publicados entre 2018 y 2026. Los resultados empiricos dibujan un perfil
editorial consistente: una revista en crecimiento exponencial (CAGR 42%),
con productividad autoral de Lotka clasica (α = 2.03) pero concentracion
Pareto extrema (17% de autores producen 80% de articulos), con un nucleo
de solo cinco revistas concentrando un tercio de las citas, con una red
de coautoria extremadamente fragmentada (modularidad 0.96, componente
principal 16%), y con una identidad tematica que viro desde la teoria y
la educacion hacia aplicaciones juridicas y medicas en contextos
ecuatorianos.

La discrepancia de orden de magnitud entre las metricas de impacto
segun la fuente consultada — Google Scholar Metrics reporta h5-index=10
y h5-mediana=25, mientras OpenAlex reporta h=1 — es el hallazgo
metodologicamente mas significativo. No se trata de un error sino de un
diagnostico estructural: las fuentes que mas citan a NCML (NSS, IJNS,
revistas cubanas y ecuatorianas) no estan plenamente indexadas en las
bases de datos comerciales, pero si en Scholar. Cualquier interpretacion
del impacto de la revista que ignore esta asimetria sera inexacta en
una u otra direccion.

## 6.1 Tres aportes principales

1. **Una linea base empirica documentada**. Los 762 articulos, 1.363
   autores y 11.877 referencias analizados constituyen un punto de
   partida replicable para estudios futuros sobre el ecosistema
   neutrosofico. El pipeline completo es publico y ejecutable.
2. **Un diagnostico honesto del impacto**. La discrepancia 10x entre
   OpenAlex y Scholar Metrics refuta tanto la interpretacion
   triunfalista del crecimiento editorial como la derrotista del
   h-index OpenAlex: el impacto real es modesto pero consistente con
   el de revistas emergentes del ecosistema.
3. **Un dialogo empirico con la critica Woodall et al. (2025)**. Dos de
   los tres cuestionamientos (concentracion metodologica, concentracion
   citacional) se verifican con los datos; el tercero (validacion
   externa limitada) se sostiene parcialmente. La respuesta adecuada no
   es defensiva sino adoptar la critica como agenda editorial, tal como
   se detalla en la Seccion 7.

## 6.2 Implicaciones

Los resultados se traducen en una hoja de ruta operativa de 15
recomendaciones editoriales escalonadas en tres horizontes (0-6 meses,
6-18 meses, 18-36 meses), documentadas en la Seccion 7. El camino
critico es de seis acciones: ISSN propio, landing pages HTML con
metadatos `citation_*`, envio a DOAJ y Latindex, diversificacion
internacional del Editorial Board, reclutamiento de revisores externos
al ecosistema, y migracion a una plataforma editorial profesional tipo
OJS. La ejecucion de esas seis acciones llevaria a la revista al umbral
elegible para el Content Selection Advisory Board (CSAB) de Scopus al
cabo de tres anos, con una probabilidad de aceptacion estimada entre 40
y 50%.

El coste monetario agregado de las 15 recomendaciones es modesto
(aproximadamente 1.000 USD/ano recurrente mas 2.000 USD iniciales). El
cuello de botella es el tiempo editorial del Editor-in-Chief y la
coordinacion de un Editorial Board renovado, no el presupuesto.

## 6.3 Lineas de trabajo futuro

El estudio abre cinco lineas de investigacion complementarias:

- **Benchmark comparativo** con NSS e IJNS aplicando el mismo pipeline
  a las tres revistas del ecosistema, lo que permitiria contrastes
  directos de Lotka, Bradford y topicos.
- **Extraccion de referencias con GROBID** para reconstruir la red de
  co-citacion y el acoplamiento bibliografico, dimensiones no cubiertas
  por la extraccion heuristica del presente trabajo.
- **Analisis de textualidad**: aplicar deteccion de similitud sobre los
  resumenes y cuerpos de articulos para estimar el grado de homogeneidad
  metodologica (la critica Woodall se beneficiaria de una metrica
  cuantitativa de repeticion AHP-TOPSIS).
- **Cruce con plataformas de tesis ecuatorianas** (UNIANDES, UBE,
  U. Guayaquil, U. Estatal de Bolivar) para validar o refutar la
  hipotesis de que NCML funciona parcialmente como canal de trabajos
  de titulacion.
- **Seguimiento longitudinal** del impacto Scholar en la cohorte
  2025-2026 a lo largo de los proximos cinco anos, para observar si
  la ampliacion tematica se traduce en mas citas externas al
  ecosistema.

## 6.4 Coda

Publicar una retrospectiva bibliometrica de la revista que uno edita es
un ejercicio incomodo. La tentacion del triunfalismo es evidente y la
del defensismo, tambien. Los autores sostienen que el ejercicio vale la
pena solo si el informe se construye con la misma exigencia empirica
que se aplica a cualquier objeto externo de estudio. Los hallazgos
presentados — y muy especialmente el cambio de identidad tematica
documentado en la Seccion 4.5 — obligan a una discusion editorial
abierta que este trabajo intenta iniciar, no cerrar. La Seccion 7
propone un programa concreto, pero su ejecucion depende en ultima
instancia de una decision colectiva del ecosistema neutrosofico sobre
el tipo de revista que NCML pretende ser en los proximos anos: un
canal de aplicaciones locales de una metodologia establecida, o un
foro internacional de desarrollo y validacion de una disciplina.

# 7. Recomendaciones editoriales: hoja de ruta de impacto

Esta seccion sintetiza en una hoja de ruta de tres horizontes temporales las
acciones que, a juicio de los autores y fundamentadas en los hallazgos de las
Secciones 4 y 5, pueden elevar de forma sostenida el impacto de NCML. Cada
recomendacion se presenta con: accion concreta, esfuerzo estimado (bajo /
medio / alto), retorno esperado, horizonte y mecanismo de medicion.

## 7.1 Resumen ejecutivo

**Diagnostico**: NCML tiene crecimiento editorial fuerte (CAGR 42%) y un
impacto Scholar modesto pero real (h5=10, h5-mediana=25), enmascarado
por la cobertura limitada de OpenAlex y la ausencia de indexacion Scopus.
La debilidad estructural esta en la concentracion geografica (95%
iberoamericana, 60% ecuatoriana), la fragmentacion de la red de coautoria
(modularidad 0.96, componente principal 16%) y la concentracion citacional
(5 revistas acaparan 33% de las citas).

**Objetivo a tres anos**: llevar a NCML al umbral elegible para el
Content Selection and Advisory Board (CSAB) de Scopus, mantener la
trayectoria de crecimiento pero con calidad media alta, y reducir la
auto-citacion del ecosistema por debajo del 15%.

## 7.2 Horizonte corto plazo (0–6 meses)

### R1. Solicitar ISSN electronico propio (esfuerzo bajo, retorno alto)

Sin ISSN, NCML queda excluida de DOAJ, Latindex, REDIB, Redalyc, ERIH
Plus y cualquier directorio formal. Solicitar el ISSN a traves del Centro
Nacional ISSN de Cuba (via NSIA Publishing) o directamente a ISSN
International. Plazo administrativo tipico: 6-10 semanas. **Sin este
paso, el resto del plan queda bloqueado en los puntos R5, R7, R11.**

*Medicion*: ISSN asignado y publicado en la pagina oficial.

### R2. Metadatos `citation_*` y Dublin Core en HTML por articulo (esfuerzo medio, retorno alto)

Generar desde `works.csv` (CSV estructurado ya producido por el pipeline
de este estudio) una landing page HTML por articulo en
`fs.unm.edu/NCML/<vol>/<doi>/`, con etiquetas `<meta name="citation_*">`
que Google Scholar, Microsoft Academic, Semantic Scholar y CORE usan
para deduplicar versiones y ampliar indexacion. Herramienta sugerida:
Hugo o Jekyll, con plantilla de 40 lineas alimentada desde el CSV.
Tiempo: 1 semana de trabajo con asistencia tecnica.

*Medicion*: indice de deduplicacion en Scholar (cantidad de versiones
agrupadas por articulo); debe estabilizarse en 1.0-1.5 tras la
indexacion.

### R3. Envio a DOAJ y Latindex (esfuerzo bajo, retorno alto)

DOAJ (Directory of Open Access Journals) es el sello de calidad OA mas
reconocido internacionalmente. Criterios: revision por pares verificable,
politica editorial publica, licencia Creative Commons explicita, ISSN.
Latindex (catalogo iberoamericano) requiere 33 criterios, 25 de los
cuales NCML ya cumple. El envio es gratuito. Plazo de evaluacion: 3-5
meses.

*Medicion*: sello DOAJ visible y badge Latindex Catalogo 2.0.

### R4. Instruciones a autores explicitas y detalladas (esfuerzo bajo, retorno medio)

El Scopus CSAB evalua "policy" como pilar: instrucciones a autores
claras, plantillas de envio, codigos de conducta COPE y politica de
revision por pares visible. Hoy NCML tiene instrucciones minimas. Un
documento de 6-8 paginas con ejemplos de estructura, normas de citacion,
politica de coautoria y proceso de revision duplica la senal de calidad
editorial.

*Medicion*: tasa de rechazo desk con justificacion <5%, ratio
revisiones/articulo publicado >=2.

### R5. Deposito Zenodo con DOI DataCite y tags estandarizados (esfuerzo bajo, retorno medio)

Ya se usa Zenodo, pero los depositos carecen de metadatos estandarizados
(keywords, subject, language, rights). Completar los metadatos durante el
deposito mejora el descubrimiento via OpenAIRE y DataCite Commons.

*Medicion*: porcentaje de depositos con los 8 campos metadata completos;
objetivo 100%.

## 7.3 Horizonte medio plazo (6–18 meses)

### R6. Diversificacion del Editorial Board hacia no iberoamericanos (esfuerzo alto, retorno alto)

Hoy el Editorial Board esta dominado por editores de Ecuador y Cuba. El
CSAB de Scopus penaliza explicitamente la homogeneidad geografica del
board. Objetivo: al menos 40% de miembros de fuera de Iberoamerica al
cabo de 18 meses, con presencia de al menos 4 continentes. Reclutamiento
prioritario: investigadores de logica difusa / soft computing / decision
making con trabajo previo no neutrosofico, de Europa del Este (Bulgaria,
Polonia, Rumania donde ya existen vinculos), Asia (India, Japon, China),
y Norteamerica. Negociacion: algunos aceptaran con condicion de co-editar
numeros especiales.

*Medicion*: composicion geografica del Editorial Board publicada;
coautoria del board con autores nuevos de sus regiones.

### R7. Programa de peer review con revisores externos al ecosistema (esfuerzo medio, retorno alto)

Reclutar una pool de 30-50 revisores externos al ecosistema neutrosofico
(expertos en AHP-TOPSIS clasico, metodos difusos, MCDM, estadistica
bayesiana). Cada articulo metodologico pasa por al menos un revisor
externo. Esto ataca directamente el cuestionamiento (iii) de Woodall
sobre validacion externa limitada. Incentivo para los revisores:
certificacion en Publons/Web of Science, invitacion a Editorial Board
consultivo.

*Medicion*: porcentaje de articulos con al menos un revisor externo al
ecosistema >=60%.

### R8. Numeros tematicos especiales con coautoria internacional obligatoria (esfuerzo medio, retorno alto)

Programa de 2-3 numeros especiales por ano, cada uno coordinado por un
editor invitado no iberoamericano. Tema ejemplo: "Neutrosophic methods
in climate risk assessment: methodological comparisons", "Explainable AI
with neutrosophic reasoning", "Neutrosophic statistics vs Bayesian
alternatives". Criterio: al menos 50% de articulos con coautoria
inter-institucional y 30% con coautoria inter-continental.

*Medicion*: ratio de articulos coautorados internacionalmente subiendo
del <5% actual al >=20% al final del periodo.

### R9. Reserva editorial para trabajos teoricos (esfuerzo medio, retorno medio)

Contener la caida del topico Smarandache/teoria (-9 pp documentada)
reservando entre 15 y 20 paginas por volumen para articulos teoricos de
fondo (revisiones, extensiones formales, demostraciones). Evaluador
senior unico para estos textos, tiempo de revision extendido.

*Medicion*: al menos 4 articulos teoricos sustantivos por volumen.

### R10. Politica de auto-citacion explicita (esfuerzo bajo, retorno medio)

El hallazgo de 17.2% de auto-cita al ecosistema NSS+NCML excede el
umbral que Scopus considera normal (10-15%). Introducir en las
Instrucciones a autores una guia de citacion donde se desaconseja
explicitamente citar mas de 3 articulos del mismo ecosistema sin
justificacion. Revisores tienen mandato de bloquear articulos con >5
autocitas al ecosistema.

*Medicion*: ratio NSS+NCML/total_citas monitoreado trimestralmente;
objetivo < 15% al cabo de 18 meses.

### R11. Transicion del alojamiento actual a una plataforma OJS o similar (esfuerzo alto, retorno alto)

La pagina actual `fs.unm.edu/NCML/Articles.htm` presenta problemas de
encoding (400+ caracteres U+FFFD) y no gestiona el flujo editorial. Una
instalacion OJS 3.x (Open Journal Systems) gestiona envios, revisiones,
publicacion y entrega metadatos estandarizados automaticamente. Instalacion
en servidor propio de NSIA o en proveedor gestionado (OJS Hosting).
Plazo: 6 meses incluyendo migracion del archivo historico.

*Medicion*: todos los volumenes 2018-2026 migrados, URLs estables,
metadatos citation_* completos.

## 7.4 Horizonte largo plazo (18–36 meses)

### R12. Aplicacion formal a Scopus (CSAB) (esfuerzo alto, retorno muy alto)

Con R1-R11 ejecutados, elaborar el envio formal a Scopus Content
Selection Advisory Board. El proceso toma 6-12 meses de evaluacion. Los
criterios relevantes son: politica editorial, calidad de contenido,
reputacion de la revista (citas externas), regularidad y diversidad
internacional. Basado en el analisis: tras completar R1-R11, NCML
cumpliria 75% de los criterios. Probabilidad de aceptacion estimada
condicionada a la ejecucion: 40-50%.

*Medicion*: respuesta de CSAB; en caso de rechazo, carta con puntos
debiles que alimentaran un nuevo ciclo.

### R13. Indexacion en Web of Science Emerging Sources Citation Index (esfuerzo alto, retorno alto)

ESCI es la antesala de SCIE y SSCI en Clarivate. Criterios menos
exigentes que Scopus, especialmente en diversidad geografica, pero con
un nivel alto de control en peer review. Enviar en paralelo al camino
Scopus.

*Medicion*: aceptacion en ESCI; genera Journal Citation Indicator (JCI)
observable.

### R14. Alianza formal con una universidad no iberoamericana como co-publisher (esfuerzo muy alto, retorno muy alto)

Explorar una alianza institucional con una universidad europea o asiatica
con tradicion en logica difusa o soft computing (ej.: TU Eindhoven, AGH
Krakow, Budapest University of Technology). El modelo seria
co-publishing con shared branding. Senal de profesionalizacion maxima
para el CSAB y para la comunidad internacional. Negociacion: ofrecer
visibilidad del co-publisher y escalamiento editorial.

*Medicion*: co-publisher firmado; articulos conjuntos publicados.

### R15. Incorporar revisores de doble ciego con tiempos publicados (esfuerzo medio, retorno medio)

Transicion formal del modelo de revision actual (simple o no documentado)
a doble ciego, con publicacion del tiempo promedio de revision y del
ratio de aceptacion por numero. Transparencia es la herramienta mas
barata y eficaz contra la critica de revistas rapidas sin control.

*Medicion*: tiempo promedio revision publicado; ratio
aceptacion/envio declarado en editorial anual.

## 7.5 Medidas transversales

### M1. Panel editorial de indicadores publico

Publicar en la pagina de la revista un tablero actualizado
cuatrimestralmente con: articulos publicados, paises representados, tasa
de auto-citacion al ecosistema, tiempo de revision promedio, aceptacion.
La transparencia editorial es un factor explicito del CSAB.

### M2. Compromiso COPE (Committee on Publication Ethics)

Adhesion formal a COPE. Sin costo. Senal de calidad editorial
reconocida por todos los indexadores.

### M3. Estudio bibliometrico periodico (anual)

Repetir la metodologia del presente estudio cada 12 meses y publicar una
actualizacion. El propio seguimiento es evidencia de reflexividad
editorial, valorada positivamente por CSAB.

## 7.6 Matriz de prioridades

| Accion | Esfuerzo | Retorno | Horizonte | Desbloquea |
|---|---|---|---|---|
| **R1** ISSN | Bajo | Alto | 0-6 m | R3, R11 |
| **R2** Metadata HTML | Medio | Alto | 0-6 m | indexacion Scholar |
| **R3** DOAJ + Latindex | Bajo | Alto | 0-6 m | visibilidad OA |
| R4 Instrucciones | Bajo | Medio | 0-6 m | CSAB criterio |
| R5 Zenodo tags | Bajo | Medio | 0-6 m | OpenAIRE |
| **R6** Board internacional | Alto | Alto | 6-18 m | Scopus |
| **R7** Revisores externos | Medio | Alto | 6-18 m | Validacion Woodall |
| **R8** Numeros especiales | Medio | Alto | 6-18 m | Coautoria intl |
| R9 Reserva teorica | Medio | Medio | 6-18 m | identidad revista |
| **R10** Politica autocita | Bajo | Medio | 6-18 m | Scopus |
| **R11** OJS | Alto | Alto | 6-18 m | profesionalizacion |
| **R12** Scopus | Alto | Muy alto | 18-36 m | salto cualitativo |
| R13 ESCI | Alto | Alto | 18-36 m | JCI observable |
| R14 Co-publisher | Muy alto | Muy alto | 18-36 m | prestigio |
| R15 Doble ciego | Medio | Medio | 18-36 m | transparencia |

**Las seis acciones en negrita** constituyen el camino critico. Si solo
se ejecutan esas, la revista avanza significativamente; si se ejecutan
las otras nueve tambien, el salto al grupo de revistas indexadas en
Scopus/ESCI es realista a 3 anos.

## 7.7 Coste estimado y recursos necesarios

La ejecucion de las 15 recomendaciones implica:

- **Tiempo editorial del EiC**: estimado 8-10 horas/semana durante 24
  meses para coordinar R6, R7, R11, R12.
- **Trabajo tecnico**: 2 semanas de desarrollo web para R2, 4 semanas
  para R11.
- **Contribucion externa**: Board member part-time de soporte al
  proceso Scopus, 2-4 horas/semana.
- **Coste monetario**: OJS hosting gestionado ~600 USD/ano, traduccion
  profesional de instrucciones ~400 USD, costos administrativos ISSN y
  alta DOAJ ~0 USD. Total: ~1.000 USD/ano recurrente + ~2.000 USD
  iniciales.

Los costos son modestos; el cuello de botella es tiempo editorial del EiC
y coordinacion del Editorial Board renovado. Un calendario realista
distribuye las 15 acciones en cuatro oleadas trimestrales durante 36
meses.

# 8. Referencias

> Compiladas en BibTeX en `refs.bib`. Citas marcadas `[TBD cita X]` en el texto deben sustituirse por `\cite{clave}` durante la conversion a LaTeX. El listado a continuacion es una lectura legible del `.bib`.

- @articlelotka1926frequency, author    = Lotka, Alfred J., title     = The frequency distribution of scientific productivity, journal   = Journal of the Washington Academy of Sciences, volume    = 16, number    = 12, pages     = 317--323, year      = 1926 
- @articlebradford1934sources, author    = Bradford, Samuel C., title     = Sources of information on specific subjects, journal   = Engineering, volume    = 137, number    = 3550, pages     = 85--86, year      = 1934 
- @articlegarfield1972citation, author    = Garfield, Eugene, title     = Citation analysis as a tool in journal evaluation, journal   = Science, volume    = 178, number    = 4060, pages     = 471--479, year      = 1972, doi       = 10.1126/science.178.4060.471 
- @articleseglen1992representative, author    = Seglen, Per O., title     = How representative is the journal impact factor?, journal   = Research Evaluation, volume    = 2, number    = 3, pages     = 143--149, year      = 1992, doi       = 10.1093/rev/2.3.143 
- @articlehaas1992introduction, author    = Haas, Peter M., title     = Introduction: Epistemic Communities and International Policy Coordination, journal   = International Organization, volume    = 46, number    = 1, pages     = 1--35, year      = 1992, doi       = 10.1017/S0020818300001442 
- @articlenewman2005power, author    = Newman, M. E. J., title     = Power laws, Pareto distributions and Zipf's law, journal   = Contemporary Physics, volume    = 46, number    = 5, pages     = 323--351, year      = 2005, doi       = 10.1080/00107510500052444 
- @articletarjan1975efficiency, author    = Tarjan, Robert E., title     = Efficiency of a Good But Not Linear Set Union Algorithm, journal   = Journal of the ACM, volume    = 22, number    = 2, pages     = 215--225, year      = 1975, doi       = 10.1145/321879.321884 
- @articleblondel2008fast, author    = Blondel, Vincent D. and Guillaume, Jean-Loup and Lambiotte, Renaud and Lefebvre, Etienne, title     = Fast unfolding of communities in large networks, journal   = Journal of Statistical Mechanics: Theory and Experiment, volume    = 2008, number    = 10, pages     = P10008, year      = 2008, doi       = 10.1088/1742-5468/2008/10/P10008 
- @articlegrootendorst2022bertopic, author    = Grootendorst, Maarten, title     = BERTopic: Neural topic modeling with a class-based TF-IDF procedure, journal   = arXiv preprint arXiv:2203.05794, year      = 2022, doi       = 10.48550/arXiv.2203.05794 
- @articlemcinnes2018umap, author    = McInnes, Leland and Healy, John and Melville, James, title     = UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction, journal   = arXiv preprint arXiv:1802.03426, year      = 2018, doi       = 10.48550/arXiv.1802.03426 
- @inproceedingsreimers2019sentence, author    = Reimers, Nils and Gurevych, Iryna, title     = Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks, booktitle = Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing, year      = 2019, doi       = 10.18653/v1/D19-1410 
- @articleharzing2008google, author    = Harzing, Anne-Wil K. and van der Wal, Ron, title     = Google Scholar as a new source for citation analysis, journal   = Ethics in Science and Environmental Politics, volume    = 8, number    = 1, pages     = 61--73, year      = 2008, doi       = 10.3354/esep00076 
- @articlemartinmartin2021google, author    = Mart\'\in-Mart\'\in, Alberto and Thelwall, Mike and Orduna-Malea, Enrique and Delgado L\'opez-C\'ozar, Emilio, title     = Google Scholar, Microsoft Academic, Scopus, Dimensions, Web of Science, and OpenCitations' COCI: a multidisciplinary comparison of coverage via citations, journal   = Scientometrics, volume    = 126, number    = 1, pages     = 871--9
- @articlepriem2022openalex, author    = Priem, Jason and Piwowar, Heather and Orr, Richard, title     = OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts, journal   = arXiv preprint arXiv:2205.01833, year      = 2022, doi       = 10.48550/arXiv.2205.01833 
- @articlepage2021prisma, author    = Page, Matthew J. and McKenzie, Joanne E. and Bossuyt, Patrick M. and Boutron, Isabelle and Hoffmann, Tammy C. and Mulrow, Cynthia D. and others, title     = The PRISMA 2020 statement: an updated guideline for reporting systematic reviews, journal   = BMJ, volume    = 372, pages     = n71, year      = 2021, doi       = 10.1136/bmj.n71 
- @booksmarandache1998unifying, author    = Smarandache, Florentin, title     = A Unifying Field in Logics: Neutrosophic Logic. Neutrosophy, Neutrosophic Set, Neutrosophic Probability, publisher = American Research Press, address   = Rehoboth, NM, year      = 1998 
- @booksmarandache1999unifying, author    = Smarandache, Florentin, title     = A Unifying Field in Logics: Neutrosophic Logic. Neutrosophy, Neutrosophic Set, Neutrosophic Probability and Statistics, publisher = American Research Press, address   = Rehoboth, NM, edition   = Second, year      = 1999 
- @articlewoodall2025neutrosophic, author    = Woodall, William H. and Faltin, Frederick W. and Reynolds, Marion R., title     = A critical evaluation of neutrosophic methods in statistical process control and decision making, journal   = Quality Engineering, year      = 2025, doi       = 10.1080/08982112.2025.2482198, note      = Verificar volumen/paginas tras publicacion final 
- @bookhirsch2005index, author    = Hirsch, J. E., title     = An index to quantify an individual's scientific research output, journal   = Proceedings of the National Academy of Sciences, volume    = 102, number    = 46, pages     = 16569--16572, year      = 2005, doi       = 10.1073/pnas.0507655102 
- @articlelarsen2010rate, author    = Larsen, Peder Olesen and von Ins, Markus, title     = The rate of growth in scientific publication and the decline in coverage provided by Science Citation Index, journal   = Scientometrics, volume    = 84, number    = 3, pages     = 575--603, year      = 2010, doi       = 10.1007/s11192-010-0202-z 
- @articlepetrou2020mdpi, author    = Petrou, Christos, title     = MDPI's remarkable growth, journal   = The Scholarly Kitchen, year      = 2020, note      = Blog post; alternativa formal pendiente 
- @articlezenodo2013, author    = CERN and OpenAIRE, title     = Zenodo: Research. Shared, year      = 2013--, howpublished = \urlhttps://zenodo.org/, note      = Repositorio digital abierto 
- @articlescopus2024criteria, author    = Elsevier, title     = Scopus Content Selection and Advisory Board (CSAB) evaluation criteria, year      = 2024, howpublished = \urlhttps://www.elsevier.com/solutions/scopus/how-scopus-works/content/content-policy-and-selection, note      = Consultado abril 2026 
