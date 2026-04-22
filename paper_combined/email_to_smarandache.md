# Correo a Florentin Smarandache

**Para:** Florentin Smarandache <smarand@unm.edu>
**CC:** Yismandry Gonzalez Vargas <yismandrygonzalezvargas@gmail.com>
**Asunto:** Borrador combinado — retrospectiva NCML + extension
neutrosofica, y propuesta de pasos para seguir impulsando la revista

---

Estimado Florentin,

Te escribo para compartir el borrador del articulo que acabamos de
cerrar con Yismandry Gonzalez Vargas (ALCN, Cuba). Se titula *"Eight
Years of Neutrosophic Computing and Machine Learning: a Bibliometric
Retrospective and a Neutrosophic Extension to Bibliometric Analysis
(2018–2026)"* y combina dos piezas que inicialmente habiamos imaginado
como articulos separados: una retrospectiva bibliometrica clasica de
NCML y una propuesta metodologica que introduce la neutrosofia como
herramienta para el propio analisis bibliometrico. El manuscrito
completo (10.100 palabras, 12 figuras, 6 tablas, 27 referencias) esta
adjunto como .docx y tambien disponible en
https://github.com/mleyvaz/ncml-bibliometric-2026 con todo el codigo
reproducible bajo licencia MIT y los datos bajo CC-BY 4.0.

## 1. Por que decidimos combinarlo en un solo paper

La retrospectiva describe NCML con metodos bibliometricos clasicos
(Lotka, Bradford, h-index, red de coautoria, modelado de topicos). El
framework neutrosofico toma el mismo corpus y reinterpreta cada
indicador como un triple (T, I, F) donde la indeterminacion se
**computa a partir de los datos**, no se elicita de expertos. La
combinacion es lo mas honesto que podemos ofrecer: el framework no
existe como teoria desacoplada, nace de un problema empirico concreto
(la discrepancia 10x entre OpenAlex y Google Scholar en el propio
NCML) y se valida con un experimento operativo: un ranking de autores
agregado por SVNWA (Ye 2014) que difiere substancialmente del ranking
clasico por conteo (Kendall τ = 0.20, top-10 overlap 5/10).

## 2. Como responde a Woodall et al. (2025)

Los tres cuestionamientos de Woodall, Faltin y Reynolds (Quality
Engineering, abril 2025) reciben respuesta empirica directa en el
paper:

- **"La eleccion de tres componentes rara vez se justifica por la
  estructura de los datos".** El framework deriva T, I, F de
  bootstrap, distancias a centroides, y acuerdos entre fuentes
  bibliograficas — nunca de escalas linguisticas. Removida la
  indeterminacion, se destruye informacion empiricamente presente.
  Esta es la respuesta mas fuerte posible al cuestionamiento.
- **"Las comparaciones con alternativas fuzzy o bayesianas son
  ausentes o superficiales".** La Seccion 5.6.3 demuestra que el
  reordenamiento que produce SVNWA **no lo puede reproducir** ninguna
  de las tres alternativas (fuzzy clasica colapsa I-F, intuitionistic
  exige T+F≤1 que nuestros datos violan, probabilidad requiere
  likelihoods que no existen para tres de las cuatro dimensiones). La
  Seccion 6.5 lo discute explicitamente.
- **"El ecosistema citacional es cerrado y autorreferencial".** La
  Seccion 4.4 lo confirma empiricamente (NSS+NCML = 17.2% de citas
  detectadas) y la Seccion 7 propone quince recomendaciones
  editoriales concretas para mitigarlo. No minimizamos la critica;
  la absorbemos como agenda.

En terminos simples: en vez de defendernos de Woodall, **le damos la
razon donde la tiene y demostramos con un experimento que ademas
existe un uso de neutrosofia donde sus tres componentes son
irreductibles**. Creo que ese framing es mas eficaz que cualquier
defensa frontal — convierte a Woodall en interlocutor en vez de
adversario.

## 3. Hallazgos sobre la difusion de la neutrosofia via NCML

Mas alla de lo metodologico, la retrospectiva produjo varios
resultados que muestran que NCML ha cumplido su mision de difundir la
neutrosofia como herramienta de investigacion aplicada. Destaco los
cinco mas relevantes:

- **1.363 autores unicos** han publicado en NCML en siete anos, con
  349 autores nuevos solo en 2025. La mayoria son investigadores que
  *aprendieron* neutrosofia para su trabajo; solo una minoria proviene
  de tu escuela directa. La revista ha funcionado como puerta de
  entrada al metodo.
- **La agenda tematica se diversifico a 24 topicos distintos**
  cubriendo derecho, medicina clinica, educacion, ingenieria,
  sostenibilidad municipal y teoria pura. Neutrosofia paso de ser
  una rama logica especializada a ser una caja de herramientas para
  tesis de grado en seis paises iberoamericanos.
- **Tres revistas cubanas no-neutrosoficas entraron al nucleo Bradford
  de citaciones** (Universidad y Sociedad, Serie Cientifica UCI,
  Revista Conrado). Son publicaciones de educacion e informatica
  sin afiliacion con NSIA, y citan a NCML regularmente — evidencia
  directa de que la neutrosofia cruzo el limite del ecosistema
  original hacia la literatura cubana en sentido amplio.
- **La comunidad C29 de la red de coautoria** (tu nucleo teorico, 9
  miembros con 61 articulos combinados) es la que tiene mas
  productividad por autor (6.8 vs 4.1 del cluster ecuatoriano mas
  grande). El ranking SVNWA de la Seccion 5.6 confirma que los
  autores con foco teorico suben fuertemente cuando se consideran
  dimensiones mas alla del volumen — en otras palabras, tu escuela
  sigue siendo el centro de gravedad intelectual de la revista
  aunque proporcionalmente publique menos articulos que las escuelas
  aplicadas.
- **h5-index de NCML en Google Scholar Metrics = 10**, con
  h5-mediana = 25, que en comparacion con NSS (h5 = 57) e IJNS
  (h5 = 31) posiciona a NCML como la mas joven de las tres hermanas
  pero ya con impacto medible, no marginal. La discrepancia con
  OpenAlex (h = 1) es el hallazgo operativo del paper: el impacto
  esta ahi, solo que los indices commerciales no lo ven completo.

## 4. Diez pasos que propongo para seguir impulsando NCML

La Seccion 7 del paper enumera quince recomendaciones editoriales
detalladas. De esas, quisiera pedir tu acompanamiento especifico en
las que tu posicion hace diferencia directa. Las ordeno de mayor a
menor peso:

1. **Liderar la diversificacion internacional del Editorial Board.**
   Tu red directa (University of New Mexico + colaboradores en
   Europa del Este, Asia y Norteamerica) es la palanca mas efectiva
   para cumplir el objetivo de 40% no iberoamericanos al cabo de 18
   meses. Es el requisito bloqueante para Scopus.
2. **Invitar explicitamente a 5-10 revisores externos al ecosistema**
   (especialistas en fuzzy clasica, Bayesian MCDM, statistical
   process control). Tu rol como EiC de NSS te da acceso a
   investigadores que a mi me serian dificiles de alcanzar. El paper
   propone que cada articulo metodologico pase por al menos uno de
   estos revisores — responde directamente al tercer punto de
   Woodall.
3. **Coeditar un numero especial sobre *Neutrosophy vs Fuzzy vs
   Bayesian: Methodological Comparisons***. Es el antidoto exacto
   contra la critica "falta comparacion con alternativas". Si te
   animas, yo armo la call for papers y tu eliges al Guest Editor
   externo.
4. **Reservar 15-20 paginas por volumen para teoria neutrosofica de
   fondo.** El paper muestra que el topico T7 (tu nucleo teorico)
   cayo -9.0 pp en la composicion de NCML entre 2018-2020 y
   2023-2025. La revista necesita tus articulos teoricos para no
   drenarse en aplicaciones.
5. **Revisar la version final del manuscrito** antes del envio. Tu
   lectura es la unica garantia de que el tratamiento teorico de
   neutrosofia este correcto y de que el tono del dialogo con Woodall
   sea defendible.
6. **Autorizar el uso del nombre NSIA Publishing** para la solicitud
   de ISSN electronico propio de NCML. Sin ISSN seguimos bloqueados
   para DOAJ, Latindex y REDIB (punto R1 del paper).
7. **Co-firmar una carta de presentacion a Scopus CSAB** cuando el
   resto de requisitos editoriales esten completos (~18-24 meses de
   trabajo). Tu trayectoria y h-index dan credibilidad al envio.
8. **Proponer que NSS y NCML adopten formalmente COPE** (Committee on
   Publication Ethics) simultaneamente. Senal barata y de alto
   impacto para la indexacion.
9. **Presentar la retrospectiva + framework en el proximo congreso
   NSIA**. Una charla conjunta seria la mejor forma de comunicar el
   mensaje y recibir feedback temprano antes del envio formal a una
   revista Q2 externa (estoy pensando Symmetry o Soft Computing si
   queres que despues armemos un segundo paper derivado).
10. **Escribir una respuesta formal a Woodall et al. (2025)** — no
    como critica a ellos, sino como "methodological note" reconociendo
    los puntos validos y mostrando el ejemplo del presente paper como
    uso no-decorativo de neutrosofia. Podriamos coordinarla via
    *Quality Engineering* o *International Journal of Neutrosophic
    Science*. Te propongo que vos lleves esa voz.

## 5. Calendario propuesto

- **Esta semana**: lectura del manuscrito combinado y comentarios.
- **Proximas 2 semanas**: incorporo tus cambios, Yismandry validacion
  final, nos ponemos de acuerdo sobre revista destino (mi voto:
  enviarlo primero a NCML como retrospectiva editorial con COI
  declarado, y un segundo paper derivado a Symmetry o IJNS).
- **Mes 1-2**: envio, gestion de peer review externo.
- **Mes 3-6**: empezamos a ejecutar los 10 puntos de arriba en
  paralelo.

Te adjunto el docx. El repositorio GitHub esta publico y actualizado
(commit `b8f628f`). Cualquier revisor puede clonar y reproducir los
resultados en ~30 minutos. Si queres, te paso acceso para que veas el
codigo directo.

Quedo atento a tus comentarios. Si preferis una llamada antes de
leer con calma, decime horario y me adapto.

Un fuerte abrazo,

Maikel Leyva Vazquez
Editor-in-Chief, Neutrosophic Computing and Machine Learning
Universidad Bolivariana del Ecuador / Universidad de Guayaquil
mleyvaz@gmail.com
