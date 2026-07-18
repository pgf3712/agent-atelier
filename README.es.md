# Agent Atelier de Paula e Indy

![Modo aprendizaje de Agent Atelier con Paula e Indy](docs/images/hero-learning-mode.png)

Agent Atelier es un laboratorio educativo bilingüe y offline para aprender cómo funcionan los agentes de IA desde dentro. Su primera versión ejecutable implementa un agente determinista de informes de investigación con acciones tipadas, herramientas permitidas explícitamente, seguimiento de evidencias, presupuestos de pasos y herramientas, detección de bucles y eventos públicos seguros.

El recorrido predeterminado no necesita clave de API ni conexión a internet. Existe un adaptador opcional de OpenAI para quien quiera probar un modelo real después de entender el arnés offline.

## Por qué lo construí

Creé este proyecto personal de portfolio para que la ingeniería de agentes dejara de parecer una caja negra. Mi objetivo no era colocar un chat delante de un modelo, sino **gamificar el proceso de comprender, construir, probar y explicar un arnés de agente desde dentro**.

El proyecto une tres partes de mi perfil: ingeniería de IA, enseñanza y artes visuales. El estudio nocturno de pixel art está inspirado en mi propio espacio creativo. Paula es una guía estilizada inspirada en mí e Indy está inspirado en mi gato siamés. Sus funciones son distintas a propósito: Paula explica los conceptos y los conecta con código real; Indy ofrece pistas opcionales y solo muestra una respuesta cuando el usuario se lo pide.

A medida que se completan los capítulos, crecen tanto el estudio como el modelo mental del alumno. La identidad visual es personal, pero cada elemento decorativo acompaña un objetivo técnico real.

## Estado actual

Cada laboratorio exige ahora una predicción antes de desbloquear el experimento. Predicciones, retos de código y explicaciones se resuelven eligiendo entre opciones específicas del capítulo, sin redactar párrafos ni identificadores. Las alternativas incorrectas representan errores mentales realistas y el feedback explica por qué fallan.

El nuevo Modo estudio permite repasar los once capítulos antes de practicar. Cada desplegable contiene una explicación sencilla, un ejemplo, un error frecuente, la prueba esperada y los archivos reales que se construirán.

El núcleo determinista y la interfaz bilingüe ya son ejecutables. Paula e Indy utilizan 22 PNG transparentes independientes derivados de forma reproducible de la hoja de pixel art grueso v2 aprobada.

Incluye:

- Motor de agente independiente de frameworks.
- Proveedor simulado reproducible.
- Corpus local pequeño.
- Validación de herramientas, presupuestos y citas.
- Interfaz inglés/castellano.
- Capítulos educativos iniciales.
- Evaluación determinista con cinco escenarios.
- Dirección visual y registro de procedencia.
- Un taller lateral con tres pasos de construcción ordenados por capítulo que muestra archivos, código, comando, salida y un reto guiado.
- Dos modos realmente distintos: Aprendizaje conserva las explicaciones de Paula; Taller prioriza código y práctica.
- Una escena fija diferente de Paula e Indy en cada capítulo, sin parpadeos ni saltos.
- Una secuencia única y visible por capítulo: **Comprende → Construye → Prueba → Explica → Completa**.
- Una explicación guiada que conecta una regla controlada por la aplicación con un resultado observado.
- Un fondo original de estudio pixel art nocturno bajo superficies azul marino translúcidas.

Paula e Indy no utilizan GIF ni animación dentro de los capítulos. Cada capítulo carga un PNG fijo y transparente distinto —leyendo, pensando, observando o celebrando— sin recortar la lámina original mediante CSS. Así no pueden aparecer orejas, colas o fragmentos de otra pose. El Indy dormido independiente de la barra lateral respira muy suavemente mediante CSS y muestra pequeñas `Z`; el movimiento se desactiva automáticamente si el usuario prefiere animación reducida.

Las poses se precargan, llevan una versión para evitar cachés antiguas y cuentan con una imagen segura de respaldo. Además, Indy funciona como ayuda opcional: al pulsar su insignia de interrogación aparece una pista contextual; la respuesta exacta permanece oculta tras una segunda acción deliberada.

Paula cumple una función distinta: al pulsar sobre ella se abre su cuaderno técnico del capítulo. Allí explica el modelo mental con más profundidad, ofrece un ejemplo concreto, señala el error más frecuente, conecta los archivos que se construyen y propone una respuesta breve para defender el concepto en una entrevista. Las preguntas también devuelven feedback razonado: no se limitan a indicar si una opción es correcta o incorrecta.

Al completar los once capítulos se desbloquea una celebración bilingüe con poses animadas originales de Paula e Indy, confeti respetuoso con movimiento reducido y una melodía de victoria sintetizada si el audio está activo. El premio puede volver a abrirse desde el indicador de progreso y enlaza directamente al [LinkedIn de Paula](https://www.linkedin.com/in/paula-garcia-fernandez-pgf3712) y a su [perfil de GitHub](https://github.com/pgf3712).

El audio acogedor opcional utiliza una pista ambiental original generada de forma reproducible por el propio repositorio, además de pequeños sonidos Web Audio de clic, capítulo y celebración. No contiene grabaciones de terceros, solo comienza tras una acción explícita, muestra su estado, guarda únicamente el volumen seleccionado y puede silenciarse en cualquier momento.

La auditoría pedagógica completa está en `docs/CURRICULUM_QA.md`.

La historia visual y el propósito pedagógico de Paula, Indy y el estudio se explican en `docs/DESIGN_STORY.md`.

## El recorrido visual de aprendizaje

### Estudia antes de construir

![Modo estudio con la guía completa de once capítulos y una lección desplegada](docs/images/study-mode-guide.png)

El Modo estudio ofrece a quien empieza una visión tranquila antes de tocar código. Cada capítulo conecta una idea en lenguaje sencillo con un ejemplo, un error frecuente, una prueba observable y los archivos reales que se construirán.

### Construye el arnés paso a paso

![Modo taller con un paso numerado, el archivo de código y un comando local simulado](docs/images/workshop-code-step.png)

El Modo taller convierte el concepto en tres pasos de construcción. El alumno inspecciona un archivo real y pequeño, entiende por qué existe, ejecuta una comprobación determinista y completa un reto guiado. La interfaz distingue claramente una simulación local de una llamada externa.

### Pide solo la ayuda que necesites

| Cuaderno técnico de Paula | Ayuda opcional de Indy |
|---|---|
| ![Cuaderno técnico de Paula conectando el concepto con archivos, errores y una respuesta de entrevista](docs/images/paula-technical-notebook.png) | ![Pista contextual de Indy junto al taller de código activo](docs/images/indy-contextual-hint.png) |
| Paula explica cómo se conectan las piezas y convierte la lección en una explicación defendible en una entrevista. | Indy empieza con una pista pequeña. La respuesta exacta permanece oculta tras una segunda acción deliberada. |

### Termina con evidencias, no solo con clics

![Premio final con Paula, Indy y el trofeo de Agent Atelier Builder](docs/images/completion-reward.png)

El premio se desbloquea al completar los once capítulos. Cierra el recorrido con una escena original, una celebración opcional respetuosa con el movimiento reducido y enlaces directos a los perfiles profesionales de la creadora.

## Vista previa rápida en Windows

Haz doble clic en:

```text
OPEN_AGENT_ATELIER.bat
```

Se abrirá `http://127.0.0.1:8765/web/`. Mantén abierta la ventana de terminal y pulsa `Ctrl+C` para detener el servidor.

Antes de publicar, haz doble clic en `VERIFY_AGENT_ATELIER.bat` para repetir las comprobaciones esenciales de GitHub Actions.

También puedes iniciarlo manualmente:

```bash
PYTHONPATH=src python -m agent_atelier.preview
```

## Proveedor real opcional

El capítulo 10 puede sustituir únicamente la capa del proveedor por un adaptador de OpenAI Responses API. La interfaz web pública nunca pide ni recibe una clave. En Windows, `OPEN_AGENT_ATELIER_REAL.bat` la solicita fuera del navegador, la mantiene únicamente en el proceso del servidor local y la elimina al cerrarlo. La interfaz sigue exigiendo consentimiento explícito antes de una llamada externa potencialmente de pago.

La instalación, los límites, el flujo de datos y los costes se explican en `docs/REAL_PROVIDER.es.md`. El proveedor simulado continúa siendo el predeterminado para aprender, probar y ejecutar la integración continua.

## Pruebas

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Evaluación reproducible

```bash
PYTHONPATH=src python -m agent_atelier.evaluate_cli
```

Los escenarios actuales comprueban:

- Respuesta respaldada por evidencias reales.
- Declaración honesta de información insuficiente.
- Cumplimiento del presupuesto de herramientas.
- Rechazo de herramientas no permitidas.
- Rechazo de citas inventadas.

GitHub Actions repite las pruebas, la compilación de Python, la validación sintáctica de JavaScript y la evaluación determinista en cada cambio. El workflow no necesita claves ni puede generar costes de un modelo.

## Cómo entender el repositorio

- `tutorials/`: capítulos ejecutables en ambos idiomas.
- `docs/decisions/`: decisiones técnicas y alternativas consideradas.
- `SECURITY.md`: límites y riesgos conocidos.
- `COPYRIGHT.md`: derechos de uso y copyright reservado.
- `ASSET_CREDITS.md`: creación y créditos de los recursos visuales y sonoros.
- `docs/INTERVIEW_GUIDE.es.md`: respuestas de entrevista conectadas con decisiones reales del código.

## Limitaciones honestas

- El proveedor predeterminado es simulado; el adaptador real opcional se limita al capítulo final integrado.
- El corpus de evidencias es local y deliberadamente pequeño.
- No existe búsqueda web real ni memoria persistente respaldada por base de datos.
- La autenticación y el uso multiusuario no están implementados.
- Los once capítulos (0–10) ya incluyen laboratorios diferentes y ejecutables en la interfaz local.

El proyecto se publica como portfolio con copyright reservado. Los términos de uso están en `COPYRIGHT.md` y los recursos propios se documentan en `ASSET_CREDITS.md`.

Consulta `README.md` para la portada canónica en inglés.
