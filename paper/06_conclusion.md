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
