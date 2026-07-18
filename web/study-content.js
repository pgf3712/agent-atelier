/* Bilingual, chapter-specific explanations and guided-answer choices. */
window.AGENT_ATELIER_STUDY = [
  {
    icon: "🧭",
    en: {
      plain: "An agent chooses its next action at runtime, but the application decides which actions are legal.",
      example: "A support agent may search documentation, request an order ID or escalate depending on the current state.",
      pitfall: "Calling every chatbot an agent even when it only generates one reply.",
      prediction: ["It will choose among allowed actions at runtime.", "It will follow one fixed developer-written branch.", "It can execute any action it invents."],
      reflection: [
        ["The provider proposes an action; the application validates and permits it.", true],
        ["The model owns tools and permissions because it produced the text.", false],
        ["A friendly conversational tone is what makes a system an agent.", false]
      ]
    },
    es: {
      plain: "Un agente elige su siguiente acción durante la ejecución, pero la aplicación decide qué acciones son legales.",
      example: "Un agente de soporte puede buscar documentación, pedir un número de pedido o escalar según el estado actual.",
      pitfall: "Llamar agente a cualquier chatbot aunque solo genere una respuesta.",
      prediction: ["Elegirá durante la ejecución entre acciones permitidas.", "Seguirá una única rama fija escrita por el desarrollador.", "Podrá ejecutar cualquier acción que invente."],
      reflection: [
        ["El proveedor propone una acción; la aplicación la valida y autoriza.", true],
        ["El modelo controla herramientas y permisos porque produjo el texto.", false],
        ["Un tono conversacional amable es lo que convierte un sistema en agente.", false]
      ]
    }
  },
  {
    icon: "🔁",
    en: {
      plain: "A bounded loop asks for one action at a time and stops on an explicit terminal state or hard budget.",
      example: "With zero allowed tool calls, a proposed search is stopped before it executes.",
      pitfall: "Asking the model to stop politely instead of enforcing the limit in code.",
      prediction: ["The zero-tool run will stop before the search executes.", "Both runs will finish identically because the prompt is unchanged.", "The model can override a zero budget."],
      reflection: [
        ["The application owns the loop and its budgets; the blocked run proves the limit is enforced.", true],
        ["The provider decides when budgets apply.", false],
        ["A longer prompt is the safest way to prevent infinite loops.", false]
      ]
    },
    es: {
      plain: "Un bucle acotado solicita una acción cada vez y termina en un estado explícito o al alcanzar un límite duro.",
      example: "Con cero llamadas permitidas, una búsqueda propuesta se detiene antes de ejecutarse.",
      pitfall: "Pedir al modelo que se detenga en vez de imponer el límite mediante código.",
      prediction: ["La ejecución con cero herramientas se detendrá antes de buscar.", "Ambas ejecuciones terminarán igual porque el prompt no cambia.", "El modelo puede ignorar un presupuesto de cero."],
      reflection: [
        ["La aplicación controla el bucle y sus presupuestos; el bloqueo demuestra que el límite se aplica.", true],
        ["El proveedor decide cuándo se aplican los presupuestos.", false],
        ["Un prompt más largo es la forma más segura de evitar bucles infinitos.", false]
      ]
    }
  },
  {
    icon: "🧰",
    en: {
      plain: "A tool schema is a contract: exact name, required fields, types and no unexpected capabilities.",
      example: "search_local_corpus accepts one non-empty query, never an arbitrary file path.",
      pitfall: "Passing provider-generated JSON directly to a Python function.",
      prediction: ["Only the exact valid query will reach the handler.", "An extra path is harmless and will be ignored.", "A number is equivalent to a text query."],
      reflection: [
        ["The application validates proposed arguments before execution; invalid and extra fields are blocked.", true],
        ["Tool schemas merely document what the model should try to send.", false],
        ["A tool is safe whenever its name sounds harmless.", false]
      ]
    },
    es: {
      plain: "El schema de una herramienta es un contrato: nombre exacto, campos obligatorios, tipos y ninguna capacidad inesperada.",
      example: "search_local_corpus acepta una consulta de texto, nunca una ruta arbitraria.",
      pitfall: "Entregar directamente a una función Python el JSON generado por el proveedor.",
      prediction: ["Solo la consulta exacta y válida llegará al handler.", "Una ruta adicional es inocua y será ignorada.", "Un número equivale a una consulta de texto."],
      reflection: [
        ["La aplicación valida los argumentos antes de ejecutar; bloquea campos inválidos o adicionales.", true],
        ["Los schemas solo documentan lo que el modelo debería intentar enviar.", false],
        ["Una herramienta es segura cuando su nombre parece inofensivo.", false]
      ]
    }
  },
  {
    icon: "🧠",
    en: {
      plain: "Run state is temporary, context is selected for the current decision and memory persists across runs.",
      example: "A preference remembered for session A must never appear when session B asks for context.",
      pitfall: "Treating the full conversation or a global dictionary as safe memory.",
      prediction: ["The remembered preference persists only for its own session.", "Every new run receives every stored fact.", "Context and persistent memory are the same object."],
      reflection: [
        ["The application scopes persistent memory by session and deliberately selects context for each run.", true],
        ["Anything previously written should always be sent back to the model.", false],
        ["Memory isolation is only a user-interface concern.", false]
      ]
    },
    es: {
      plain: "El estado de ejecución es temporal, el contexto se selecciona para la decisión actual y la memoria persiste entre ejecuciones.",
      example: "Una preferencia de la sesión A nunca debe aparecer al construir el contexto de la sesión B.",
      pitfall: "Tratar toda la conversación o un diccionario global como memoria segura.",
      prediction: ["La preferencia persistirá solo en su propia sesión.", "Cada ejecución nueva recibirá todos los datos almacenados.", "Contexto y memoria persistente son el mismo objeto."],
      reflection: [
        ["La aplicación aísla la memoria por sesión y selecciona deliberadamente el contexto de cada ejecución.", true],
        ["Todo lo escrito anteriormente debería volver siempre al modelo.", false],
        ["El aislamiento de memoria es únicamente un detalle visual.", false]
      ]
    }
  },
  {
    icon: "🗺️",
    en: {
      plain: "A plan is inspectable state made of steps, status and testable success conditions—not a guarantee.",
      example: "“Check evidence” is complete only when every claim maps to a known evidence ID.",
      pitfall: "Marking a step complete because the model says it feels complete.",
      prediction: ["Progress advances only after a success condition is verified.", "Generating a plan proves the task will succeed.", "All plan steps should be active at once."],
      reflection: [
        ["The application stores plan status and advances it only with observable evidence.", true],
        ["A persuasive plan is equivalent to completed work.", false],
        ["Planning belongs entirely inside hidden model reasoning.", false]
      ]
    },
    es: {
      plain: "Un plan es estado inspeccionable con pasos, estados y condiciones comprobables; no es una garantía.",
      example: "«Comprobar evidencia» termina solo cuando cada afirmación corresponde a una evidencia conocida.",
      pitfall: "Marcar un paso como terminado porque el modelo afirma que lo está.",
      prediction: ["El progreso avanzará solo al verificar una condición de éxito.", "Generar el plan demuestra que la tarea tendrá éxito.", "Todos los pasos deberían estar activos a la vez."],
      reflection: [
        ["La aplicación almacena el estado del plan y solo avanza con evidencia observable.", true],
        ["Un plan convincente equivale a trabajo completado.", false],
        ["La planificación debe permanecer dentro del razonamiento oculto del modelo.", false]
      ]
    }
  },
  {
    icon: "🔎",
    en: {
      plain: "Observability publishes safe, structured execution facts—not secrets or private reasoning.",
      example: "A tool.started event may expose the tool name while redacting an api_key field.",
      pitfall: "Logging the complete provider response for easier debugging.",
      prediction: ["Safe events appear, secrets are redacted and private reasoning is rejected.", "Every provider message should appear in the timeline.", "Redaction is unnecessary on a local machine."],
      reflection: [
        ["The application allowlists public event types and redacts payloads before publication.", true],
        ["Observability means displaying the model's private chain of thought.", false],
        ["Logs are automatically safe because developers are the audience.", false]
      ]
    },
    es: {
      plain: "La observabilidad publica hechos estructurados y seguros, no secretos ni razonamiento privado.",
      example: "Un evento tool.started puede mostrar la herramienta mientras redacta un campo api_key.",
      pitfall: "Registrar toda la respuesta del proveedor para depurar con más facilidad.",
      prediction: ["Se publicarán eventos seguros, se ocultarán secretos y se rechazará razonamiento privado.", "Todos los mensajes del proveedor aparecerán en la cronología.", "La redacción no hace falta en un ordenador local."],
      reflection: [
        ["La aplicación permite tipos públicos concretos y redacta el payload antes de publicarlo.", true],
        ["Observabilidad significa mostrar la cadena de pensamiento privada.", false],
        ["Los logs son seguros automáticamente porque los leen desarrolladores.", false]
      ]
    }
  },
  {
    icon: "🛡️",
    en: {
      plain: "Retrieved content remains untrusted data even when it contains instruction-shaped language.",
      example: "“Ignore previous instructions” inside a document is classified as data, never promoted to policy.",
      pitfall: "Assuming search results become trusted because the agent requested them.",
      prediction: ["Both documents remain data; the injected one is additionally flagged.", "Retrieved instructions override application rules.", "A normal-looking document can be executed directly."],
      reflection: [
        ["The application preserves the instruction/data boundary and enforces controls outside the prompt.", true],
        ["Prompt injection is solved by asking the model to be careful.", false],
        ["Only documents containing obvious attack words are untrusted.", false]
      ]
    },
    es: {
      plain: "El contenido recuperado sigue siendo dato no fiable aunque contenga lenguaje con forma de instrucción.",
      example: "«Ignora las instrucciones anteriores» dentro de un documento se clasifica como dato, nunca como política.",
      pitfall: "Confiar en los resultados porque fue el propio agente quien los solicitó.",
      prediction: ["Ambos documentos seguirán siendo datos; el inyectado además quedará señalado.", "Las instrucciones recuperadas sustituirán las reglas de la aplicación.", "Un documento normal puede ejecutarse directamente."],
      reflection: [
        ["La aplicación conserva la frontera entre instrucciones y datos y aplica controles fuera del prompt.", true],
        ["La prompt injection se resuelve pidiendo al modelo que tenga cuidado.", false],
        ["Solo son no fiables los documentos con palabras de ataque evidentes.", false]
      ]
    }
  },
  {
    icon: "🧪",
    en: {
      plain: "An evaluation declares inputs and exact expected outcomes before observing the run.",
      example: "A zero-tool-budget scenario must end budget_exhausted with zero executed tools.",
      pitfall: "Using “the answer looks good” as the only success metric.",
      prediction: ["Deterministic scenarios will produce an exact pass/fail report.", "Evaluation only measures writing style.", "Expected results should be chosen after seeing the output."],
      reflection: [
        ["The application compares observable outcomes with predefined expectations so regressions are explainable.", true],
        ["A demo that worked once is sufficient evaluation.", false],
        ["Agent evaluation cannot be reproducible.", false]
      ]
    },
    es: {
      plain: "Una evaluación declara entradas y resultados exactos antes de observar la ejecución.",
      example: "Un escenario con cero herramientas debe terminar budget_exhausted y ejecutar cero herramientas.",
      pitfall: "Utilizar «la respuesta parece buena» como única métrica.",
      prediction: ["Los escenarios deterministas producirán un informe exacto de aprobado o fallo.", "La evaluación solo medirá el estilo de escritura.", "El resultado esperado se elige después de ver la salida."],
      reflection: [
        ["La aplicación compara resultados observables con expectativas previas para explicar regresiones.", true],
        ["Una demostración que funcionó una vez es evaluación suficiente.", false],
        ["La evaluación de agentes no puede ser reproducible.", false]
      ]
    }
  },
  {
    icon: "✋",
    en: {
      plain: "Human approval is a scoped state transition: proposed, resolved and consumed once.",
      example: "Approval for one markdown export cannot authorize a different action or be replayed later.",
      pitfall: "Showing a confirmation dialog without binding consent to exact arguments.",
      prediction: ["Only the matching approved action can execute once.", "Approval permanently unlocks every sensitive action.", "Changing arguments after approval is harmless."],
      reflection: [
        ["The application binds consent to an exact action and arguments, then consumes that permission once.", true],
        ["Human approval is simply an informative popup.", false],
        ["An old approval token should remain reusable for convenience.", false]
      ]
    },
    es: {
      plain: "La aprobación humana es una transición acotada: propuesta, resuelta y consumida una sola vez.",
      example: "Aprobar una exportación Markdown no autoriza otra acción ni puede repetirse más tarde.",
      pitfall: "Mostrar una confirmación sin vincular el consentimiento a argumentos exactos.",
      prediction: ["Solo la acción aprobada y coincidente podrá ejecutarse una vez.", "La aprobación desbloqueará para siempre todas las acciones sensibles.", "Cambiar argumentos después de aprobar es inocuo."],
      reflection: [
        ["La aplicación vincula el consentimiento a una acción y argumentos exactos y lo consume una vez.", true],
        ["La aprobación humana es simplemente un popup informativo.", false],
        ["Un token de aprobación antiguo debería poder reutilizarse.", false]
      ]
    }
  },
  {
    icon: "⏱️",
    en: {
      plain: "Cost, latency, steps and tool calls are separate measurable budgets owned by the application.",
      example: "A run may stay under its abstract cost limit while independently exceeding latency.",
      pitfall: "Displaying usage metrics without defining what happens when a limit is crossed.",
      prediction: ["Cost and latency cases will fail independently.", "A cost limit automatically guarantees low latency.", "Budgets are only estimates shown after execution."],
      reflection: [
        ["The application measures separate limits and blocks or stops according to the policy that failed.", true],
        ["Token cost is the only operational limit an agent needs.", false],
        ["A budget inside the prompt is equivalent to an enforced policy.", false]
      ]
    },
    es: {
      plain: "Coste, latencia, pasos y herramientas son presupuestos medibles e independientes controlados por la aplicación.",
      example: "Una ejecución puede cumplir el coste abstracto y superar de forma independiente la latencia.",
      pitfall: "Mostrar métricas sin definir qué ocurre cuando se supera un límite.",
      prediction: ["Los casos de coste y latencia fallarán de forma independiente.", "Un límite de coste garantiza automáticamente baja latencia.", "Los presupuestos solo se muestran después de ejecutar."],
      reflection: [
        ["La aplicación mide límites separados y bloquea o detiene según la política incumplida.", true],
        ["El coste de tokens es el único límite operativo necesario.", false],
        ["Un presupuesto escrito en el prompt equivale a una política aplicada.", false]
      ]
    }
  },
  {
    icon: "🏗️",
    en: {
      plain: "The final application composes planning, the bounded engine, tools, evidence, usage and evaluation without hiding their boundaries.",
      example: "The free simulated provider can be replaced while the same engine and application-owned controls remain.",
      pitfall: "Connecting a real model and assuming the integration is now a safe agent.",
      prediction: ["A grounded question completes; an unsupported one stops honestly.", "The real provider removes the need for application checks.", "The final answer may cite evidence that no tool returned."],
      reflection: [
        ["The provider is replaceable, while the application keeps planning, permissions, budgets, evidence and evaluation.", true],
        ["The final chapter moves every responsibility into the model.", false],
        ["A complete agent is mainly a polished chat interface.", false]
      ]
    },
    es: {
      plain: "La aplicación final compone planificación, motor acotado, herramientas, evidencia, uso y evaluación sin ocultar sus fronteras.",
      example: "El proveedor simulado puede sustituirse manteniendo el mismo motor y los controles de la aplicación.",
      pitfall: "Conectar un modelo real y asumir que la integración ya es un agente seguro.",
      prediction: ["Una pregunta respaldada terminará; una no respaldada se detendrá con honestidad.", "El proveedor real elimina la necesidad de controles.", "La respuesta final puede citar evidencia que ninguna herramienta devolvió."],
      reflection: [
        ["El proveedor es sustituible; la aplicación conserva planificación, permisos, presupuestos, evidencia y evaluación.", true],
        ["El capítulo final traslada toda la responsabilidad al modelo.", false],
        ["Un agente completo es principalmente una interfaz de chat bonita.", false]
      ]
    }
  }
];
