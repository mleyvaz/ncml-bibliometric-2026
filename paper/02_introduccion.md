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
