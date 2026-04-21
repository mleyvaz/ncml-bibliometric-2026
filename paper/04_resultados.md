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
