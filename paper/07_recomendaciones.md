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
