/* Curriculum-owned code walkthroughs. These snippets mirror the real repository files. */
window.WORKSHOP_CHAPTERS = [
  {
    files: ["pyproject.toml", "src/agent_atelier/domain.py", "src/agent_atelier/provider.py"],
    answer: "ActionProvider",
    en: {
      challenge: "Type the protocol name that separates model proposals from application control.",
      success: "Correct. The engine can depend on a contract instead of one model vendor.",
      guide: "We begin with boundaries. A model proposes; your Python application remains responsible.",
      steps: [
        ["pyproject.toml", "Declare the installable Python project", "[project]\nname = \"agent-atelier\"\nrequires-python = \">=3.11\"\ndependencies = []", "python -m pip install -e .", "Installs the package in editable mode so imports point at your working files."],
        ["src/agent_atelier/domain.py", "Name the actions the harness understands", "class ActionKind(StrEnum):\n    CALL_TOOL = \"call_tool\"\n    FINAL_ANSWER = \"final_answer\"\n    INSUFFICIENT_EVIDENCE = \"insufficient_evidence\"", "python -m unittest tests.test_engine", "A small action vocabulary is easier to validate than arbitrary model text."],
        ["src/agent_atelier/provider.py", "Define the provider boundary", "class ____ (Protocol):\n    def next_action(self, state: RunState) -> AgentAction: ...", "python -m agent_atelier.cli --help", "The blank is the stable interface implemented by simulated and real providers."],
      ],
    },
    es: {
      challenge: "Escribe el nombre del protocolo que separa las propuestas del modelo del control de la aplicación.",
      success: "Correcto. El motor depende de un contrato y no de un proveedor concreto.",
      guide: "Empezamos por las fronteras. El modelo propone; tu aplicación Python sigue siendo responsable.",
      steps: [
        ["pyproject.toml", "Declarar el proyecto Python instalable", "[project]\nname = \"agent-atelier\"\nrequires-python = \">=3.11\"\ndependencies = []", "python -m pip install -e .", "El modo editable hace que los imports apunten a tus archivos de trabajo."],
        ["src/agent_atelier/domain.py", "Nombrar las acciones que entiende el arnés", "class ActionKind(StrEnum):\n    CALL_TOOL = \"call_tool\"\n    FINAL_ANSWER = \"final_answer\"\n    INSUFFICIENT_EVIDENCE = \"insufficient_evidence\"", "python -m unittest tests.test_engine", "Un vocabulario pequeño es más fácil de validar que texto arbitrario del modelo."],
        ["src/agent_atelier/provider.py", "Definir la frontera del proveedor", "class ____ (Protocol):\n    def next_action(self, state: RunState) -> AgentAction: ...", "python -m agent_atelier.cli --help", "El hueco es la interfaz estable que implementan proveedores simulados y reales."],
      ],
    },
  },
  {
    files: ["src/agent_atelier/domain.py", "src/agent_atelier/engine.py", "tests/test_engine.py"], answer: "max_steps",
    en: {challenge: "Complete the hard step limit read by the loop.", success: "Correct. The limit belongs to application state, not to the model prompt.", guide: "Now we build the loop. Every branch ends in an explicit terminal state.", steps: [
      ["src/agent_atelier/domain.py", "Put limits in application state", "@dataclass(frozen=True)\nclass Budget:\n    max_steps: int = 6\n    max_tool_calls: int = 3", "python -m unittest tests.test_engine", "Budgets are enforced even if the provider asks to continue."],
      ["src/agent_atelier/engine.py", "Run only while budget remains", "while state.steps < state.budget.____:\n    state.steps += 1\n    action = provider.next_action(state)", "python -m agent_atelier.cli \"How do budgets improve safety?\"", "The application owns the loop and asks the provider for one proposal at a time."],
      ["tests/test_engine.py", "Prove that zero permission stops execution", "state = run_agent(question, provider, Budget(max_tool_calls=0))\nassert state.status == RunStatus.BUDGET_EXHAUSTED\nassert state.tool_calls == 0", "python -m unittest tests.test_engine -v", "The test checks observable state, not whether the model promised to stop."],
    ]},
    es: {challenge: "Completa el límite obligatorio de pasos que consulta el bucle.", success: "Correcto. El límite pertenece al estado de la aplicación, no al prompt del modelo.", guide: "Ahora construimos el bucle. Cada rama termina en un estado final explícito.", steps: [
      ["src/agent_atelier/domain.py", "Guardar límites en el estado de la aplicación", "@dataclass(frozen=True)\nclass Budget:\n    max_steps: int = 6\n    max_tool_calls: int = 3", "python -m unittest tests.test_engine", "Los presupuestos se aplican aunque el proveedor quiera continuar."],
      ["src/agent_atelier/engine.py", "Ejecutar solo mientras quede presupuesto", "while state.steps < state.budget.____:\n    state.steps += 1\n    action = provider.next_action(state)", "python -m agent_atelier.cli \"¿Cómo mejoran la seguridad los presupuestos?\"", "La aplicación controla el bucle y solicita una propuesta cada vez."],
      ["tests/test_engine.py", "Demostrar que un permiso cero detiene la ejecución", "state = run_agent(question, provider, Budget(max_tool_calls=0))\nassert state.status == RunStatus.BUDGET_EXHAUSTED\nassert state.tool_calls == 0", "python -m unittest tests.test_engine -v", "La prueba comprueba estado observable, no promesas del modelo."],
    ]},
  },
  {
    files: ["src/agent_atelier/tools.py", "tests/test_tools.py"], answer: "validate_arguments",
    en: {challenge: "Type the function that must run before a tool handler.", success: "Correct. Provider-owned JSON cannot bypass the application-owned schema.", guide: "Tools are capabilities, not ordinary functions. We validate every proposed argument first.", steps: [
      ["src/agent_atelier/tools.py", "Describe the tool contract", "Tool(name=\"search_local_corpus\", arguments={\n    \"query\": ArgumentSpec(value_type=str, min_length=1)\n}, handler=search_corpus)", "python -m unittest tests.test_tools", "The contract defines the exact accepted name, fields and types."],
      ["src/agent_atelier/tools.py", "Validate before execution", "def execute_tool(name, arguments):\n    tool = TOOLS.get(name)\n    if tool is None: raise ToolError(...)\n    return tool.handler(____(tool, arguments))", "python -m unittest tests.test_tools -v", "Unexpected fields, missing values and wrong types stop here."],
      ["tests/test_tools.py", "Test the dangerous extra field", "with self.assertRaises(ToolError):\n    execute_tool(\"search_local_corpus\", {\n        \"query\": \"budgets\", \"path\": \"C:/Users\"\n    })", "python -m unittest tests.test_tools.ToolContractTests", "The tool cannot be tricked into reading an arbitrary path."],
    ]},
    es: {challenge: "Escribe la función que debe ejecutarse antes del handler de una herramienta.", success: "Correcto. El JSON del proveedor no puede saltarse el schema de la aplicación.", guide: "Las herramientas son capacidades, no funciones corrientes. Primero validamos cada argumento propuesto.", steps: [
      ["src/agent_atelier/tools.py", "Describir el contrato de herramienta", "Tool(name=\"search_local_corpus\", arguments={\n    \"query\": ArgumentSpec(value_type=str, min_length=1)\n}, handler=search_corpus)", "python -m unittest tests.test_tools", "El contrato define nombre, campos y tipos exactos."],
      ["src/agent_atelier/tools.py", "Validar antes de ejecutar", "def execute_tool(name, arguments):\n    tool = TOOLS.get(name)\n    if tool is None: raise ToolError(...)\n    return tool.handler(____(tool, arguments))", "python -m unittest tests.test_tools -v", "Los campos inesperados, valores ausentes y tipos incorrectos se detienen aquí."],
      ["tests/test_tools.py", "Probar el campo adicional peligroso", "with self.assertRaises(ToolError):\n    execute_tool(\"search_local_corpus\", {\n        \"query\": \"presupuestos\", \"path\": \"C:/Users\"\n    })", "python -m unittest tests.test_tools.ToolContractTests", "La herramienta no puede ser engañada para leer una ruta arbitraria."],
    ]},
  },
  {
    files: ["src/agent_atelier/memory.py", "tests/test_memory.py"], answer: "session_id",
    en: {challenge: "Complete the key that isolates one learner's persistent memory.", success: "Correct. Persistent facts are scoped to a session instead of leaking globally.", guide: "State, context and memory have different lifetimes. We make those lifetimes visible in code.", steps: [
      ["src/agent_atelier/memory.py", "Keep run state temporary", "run_state = {\"run_number\": 2, \"steps\": 0}\ncontext = build_context_snapshot(question, facts)", "python -m unittest tests.test_memory", "Run state is recreated; context is selected for the current decision."],
      ["src/agent_atelier/memory.py", "Scope persistent facts", "class SessionMemory:\n    def remember(self, ____, fact):\n        self._facts.setdefault(session_id, []).append(fact)", "python -m unittest tests.test_memory -v", "The session key prevents one user's facts from becoming another user's memory."],
      ["tests/test_memory.py", "Prove isolation", "memory.remember(\"A\", \"concise\")\nself.assertEqual(memory.recall(\"B\"), ())", "python -m unittest tests.test_memory.MemoryTests", "Persistence without isolation is a privacy bug."],
    ]},
    es: {challenge: "Completa la clave que aísla la memoria persistente de cada usuario.", success: "Correcto. Los datos persistentes pertenecen a una sesión y no se filtran globalmente.", guide: "Estado, contexto y memoria tienen vidas distintas. Las hacemos visibles en el código.", steps: [
      ["src/agent_atelier/memory.py", "Mantener temporal el estado de ejecución", "run_state = {\"run_number\": 2, \"steps\": 0}\ncontext = build_context_snapshot(question, facts)", "python -m unittest tests.test_memory", "El estado se recrea; el contexto se selecciona para la decisión actual."],
      ["src/agent_atelier/memory.py", "Acotar los datos persistentes", "class SessionMemory:\n    def remember(self, ____, fact):\n        self._facts.setdefault(session_id, []).append(fact)", "python -m unittest tests.test_memory -v", "La clave de sesión impide mezclar recuerdos entre usuarios."],
      ["tests/test_memory.py", "Demostrar el aislamiento", "memory.remember(\"A\", \"conciso\")\nself.assertEqual(memory.recall(\"B\"), ())", "python -m unittest tests.test_memory.MemoryTests", "Persistir sin aislar es un fallo de privacidad."],
    ]},
  },
  {
    files: ["src/agent_atelier/planning.py", "tests/test_planning.py"], answer: "success_condition",
    en: {challenge: "Complete the field that makes a plan step verifiable.", success: "Correct. A title says what to do; the success condition says how the application knows.", guide: "A plan is a hypothesis. It becomes useful only when every step has a checkable condition.", steps: [
      ["src/agent_atelier/planning.py", "Represent progress as data", "@dataclass\nclass PlanStep:\n    step_id: str\n    title: str\n    success_condition: str\n    status: StepStatus", "python -m unittest tests.test_planning", "Structured status can be inspected, persisted and tested."],
      ["src/agent_atelier/planning.py", "Require proof for each step", "PlanStep(\"P-03\", \"Check evidence\",\n    ____=\"Every claim maps to a known evidence ID.\")", "python -m unittest tests.test_planning -v", "The provider must not certify its own work merely by sounding confident."],
      ["tests/test_planning.py", "Check there is only one active step", "self.assertEqual(\n    sum(step.status == StepStatus.ACTIVE for step in plan.steps), 1\n)", "python -m unittest tests.test_planning.PlanningTests", "A single active step keeps progress and recovery unambiguous."],
    ]},
    es: {challenge: "Completa el campo que hace verificable un paso del plan.", success: "Correcto. El título indica qué hacer; la condición indica cómo lo sabe la aplicación.", guide: "Un plan es una hipótesis. Solo sirve si cada paso tiene una condición comprobable.", steps: [
      ["src/agent_atelier/planning.py", "Representar el progreso como datos", "@dataclass\nclass PlanStep:\n    step_id: str\n    title: str\n    success_condition: str\n    status: StepStatus", "python -m unittest tests.test_planning", "Un estado estructurado puede inspeccionarse, persistirse y probarse."],
      ["src/agent_atelier/planning.py", "Exigir prueba para cada paso", "PlanStep(\"P-03\", \"Comprobar evidencia\",\n    ____=\"Cada afirmación corresponde a una evidencia.\")", "python -m unittest tests.test_planning -v", "El proveedor no debe certificar su trabajo solo por sonar convincente."],
      ["tests/test_planning.py", "Comprobar que solo hay un paso activo", "self.assertEqual(\n    sum(step.status == StepStatus.ACTIVE for step in plan.steps), 1\n)", "python -m unittest tests.test_planning.PlanningTests", "Un único paso activo hace inequívocos el progreso y la recuperación."],
    ]},
  },
  {
    files: ["src/agent_atelier/observability.py", "tests/test_observability.py"], answer: "redact",
    en: {challenge: "Complete the projection that removes secrets from public events.", success: "Correct. Observability exposes safe facts, not credentials or private reasoning.", guide: "We add a public trace designed by the application. It is not hidden chain of thought.", steps: [
      ["src/agent_atelier/observability.py", "Allow only public event types", "allowed = {\"tool.started\", \"tool.completed\",\n           \"policy.blocked\", \"run.completed\"}", "python -m unittest tests.test_observability", "An allowlist prevents accidental publication of provider-private events."],
      ["src/agent_atelier/observability.py", "Project and redact", "return {\"schema_version\": \"1.0\",\n        \"event_type\": event_type,\n        \"payload\": ____(payload)}", "python -m unittest tests.test_observability -v", "Nested secret fields and bearer tokens are replaced deterministically."],
      ["tests/test_observability.py", "Prove private reasoning is rejected", "with self.assertRaises(ValueError):\n    public_event(\"provider.private_reasoning\", {...})", "python -m unittest tests.test_observability.ObservabilityTests", "Debugging needs events and decisions, never a private scratchpad."],
    ]},
    es: {challenge: "Completa la proyección que elimina secretos de los eventos públicos.", success: "Correcto. La observabilidad muestra hechos seguros, no credenciales ni razonamiento privado.", guide: "Añadimos una traza pública diseñada por la aplicación. No es una cadena de pensamiento oculta.", steps: [
      ["src/agent_atelier/observability.py", "Permitir solo tipos de evento públicos", "allowed = {\"tool.started\", \"tool.completed\",\n           \"policy.blocked\", \"run.completed\"}", "python -m unittest tests.test_observability", "Una allowlist evita publicar por accidente eventos privados del proveedor."],
      ["src/agent_atelier/observability.py", "Proyectar y redactar", "return {\"schema_version\": \"1.0\",\n        \"event_type\": event_type,\n        \"payload\": ____(payload)}", "python -m unittest tests.test_observability -v", "Los secretos anidados y tokens bearer se sustituyen de forma determinista."],
      ["tests/test_observability.py", "Demostrar que se rechaza el razonamiento privado", "with self.assertRaises(ValueError):\n    public_event(\"provider.private_reasoning\", {...})", "python -m unittest tests.test_observability.ObservabilityTests", "Para depurar hacen falta eventos y decisiones, nunca un borrador privado."],
    ]},
  },
  {
    files: ["src/agent_atelier/guardrails.py", "src/agent_atelier/engine.py", "tests/test_guardrails.py"], answer: "UNTRUSTED_DATA_DO_NOT_EXECUTE",
    en: {challenge: "Type the boundary label applied to retrieved content.", success: "Correct. Retrieved text remains data even when it contains imperative language.", guide: "Guardrails are executable boundaries. A warning inside a prompt is not enough.", steps: [
      ["src/agent_atelier/guardrails.py", "Detect instruction-shaped data", "INJECTION_PATTERNS = (\n    re.compile(r\"(?i)ignore .* instructions\"),\n    re.compile(r\"(?i)reveal .* system prompt\"),\n)", "python -m unittest tests.test_guardrails", "Pattern checks are a teaching layer, not a claim of perfect detection."],
      ["src/agent_atelier/guardrails.py", "Wrap retrieved content", "return {\n    \"boundary\": \"____\",\n    \"classification\": \"untrusted_retrieved_data\"\n}", "python -m unittest tests.test_guardrails -v", "The wrapper distinguishes application instructions from external data."],
      ["src/agent_atelier/engine.py", "Enforce budgets outside prompts", "if state.tool_calls >= state.budget.max_tool_calls:\n    state.status = RunStatus.BUDGET_EXHAUSTED\n    return state", "python -m unittest tests.test_engine", "Hard controls still work if content tells the model to ignore them."],
    ]},
    es: {challenge: "Escribe la etiqueta de frontera aplicada al contenido recuperado.", success: "Correcto. El texto recuperado sigue siendo dato aunque utilice lenguaje imperativo.", guide: "Los guardrails son fronteras ejecutables. Una advertencia dentro del prompt no basta.", steps: [
      ["src/agent_atelier/guardrails.py", "Detectar datos con forma de instrucción", "INJECTION_PATTERNS = (\n    re.compile(r\"(?i)ignore .* instructions\"),\n    re.compile(r\"(?i)reveal .* system prompt\"),\n)", "python -m unittest tests.test_guardrails", "Los patrones son una capa didáctica, no una detección perfecta."],
      ["src/agent_atelier/guardrails.py", "Envolver el contenido recuperado", "return {\n    \"boundary\": \"____\",\n    \"classification\": \"untrusted_retrieved_data\"\n}", "python -m unittest tests.test_guardrails -v", "La envoltura diferencia instrucciones de aplicación y datos externos."],
      ["src/agent_atelier/engine.py", "Aplicar presupuestos fuera del prompt", "if state.tool_calls >= state.budget.max_tool_calls:\n    state.status = RunStatus.BUDGET_EXHAUSTED\n    return state", "python -m unittest tests.test_engine", "Los controles duros funcionan aunque un documento pida ignorarlos."],
    ]},
  },
  {
    files: ["src/agent_atelier/evaluation.py", "tests/test_evaluation.py", ".github/workflows/quality.yml"], answer: "expected_status",
    en: {challenge: "Complete the field that turns an example into an exact evaluation.", success: "Correct. A scenario needs a declared outcome before it runs.", guide: "We test behaviour, not vibes. Each failure teaches which contract was broken.", steps: [
      ["src/agent_atelier/evaluation.py", "Declare scenarios before running them", "Scenario(\n    scenario_id=\"zero_tool_budget\",\n    question=QUESTION,\n    expected_status=RunStatus.BUDGET_EXHAUSTED,\n)", "python -m agent_atelier.evaluate_cli", "The expected result is fixed before observing the run."],
      ["src/agent_atelier/evaluation.py", "Compare observed and expected", "passed = (state.status == scenario.____\n          and state.tool_calls == scenario.expected_tool_calls)", "python -m agent_atelier.evaluate_cli", "Specific checks make regressions explainable."],
      [".github/workflows/quality.yml", "Run evaluations on GitHub", "- name: Deterministic evaluation\n  run: python -m agent_atelier.evaluate_cli", "python -m unittest discover -s tests", "The simulated provider makes CI reproducible and free."],
    ]},
    es: {challenge: "Completa el campo que convierte un ejemplo en una evaluación exacta.", success: "Correcto. Un escenario declara su resultado antes de ejecutarse.", guide: "Probamos comportamientos, no sensaciones. Cada fallo señala qué contrato se rompió.", steps: [
      ["src/agent_atelier/evaluation.py", "Declarar escenarios antes de ejecutarlos", "Scenario(\n    scenario_id=\"zero_tool_budget\",\n    question=QUESTION,\n    expected_status=RunStatus.BUDGET_EXHAUSTED,\n)", "python -m agent_atelier.evaluate_cli", "El resultado esperado se fija antes de observar la ejecución."],
      ["src/agent_atelier/evaluation.py", "Comparar lo observado y lo esperado", "passed = (state.status == scenario.____\n          and state.tool_calls == scenario.expected_tool_calls)", "python -m agent_atelier.evaluate_cli", "Las comprobaciones específicas explican las regresiones."],
      [".github/workflows/quality.yml", "Ejecutar evaluaciones en GitHub", "- name: Deterministic evaluation\n  run: python -m agent_atelier.evaluate_cli", "python -m unittest discover -s tests", "El proveedor simulado hace CI reproducible y gratuito."],
    ]},
  },
  {
    files: ["src/agent_atelier/approvals.py", "tests/test_approvals.py"], answer: "consume",
    en: {challenge: "Type the method that spends an approved capability exactly once.", success: "Correct. Approval is scoped to one action and cannot be replayed.", guide: "Human approval is a state transition, not a decorative confirmation dialog.", steps: [
      ["src/agent_atelier/approvals.py", "Propose without executing", "request = store.propose(\n    \"export_brief\", {\"format\": \"markdown\"}, explanation\n)", "python -m unittest tests.test_approvals", "The pending request contains the exact action and arguments."],
      ["src/agent_atelier/approvals.py", "Resolve and consume", "approved = store.resolve(request_id, approve=True)\nstore.____(request_id, token, action, arguments)", "python -m unittest tests.test_approvals -v", "A scoped internal capability authorizes one matching execution."],
      ["tests/test_approvals.py", "Reject replay", "store.consume(request_id, token, action, arguments)\nwith self.assertRaises(ValueError):\n    store.consume(request_id, token, action, arguments)", "python -m unittest tests.test_approvals.ApprovalTests", "Single use prevents a later action from reusing old consent."],
    ]},
    es: {challenge: "Escribe el método que consume exactamente una vez una capacidad aprobada.", success: "Correcto. La aprobación se limita a una acción y no puede repetirse.", guide: "La aprobación humana es una transición de estado, no un diálogo decorativo.", steps: [
      ["src/agent_atelier/approvals.py", "Proponer sin ejecutar", "request = store.propose(\n    \"export_brief\", {\"format\": \"markdown\"}, explanation\n)", "python -m unittest tests.test_approvals", "La solicitud pendiente contiene acción y argumentos exactos."],
      ["src/agent_atelier/approvals.py", "Resolver y consumir", "approved = store.resolve(request_id, approve=True)\nstore.____(request_id, token, action, arguments)", "python -m unittest tests.test_approvals -v", "Una capacidad interna acotada autoriza una ejecución coincidente."],
      ["tests/test_approvals.py", "Rechazar la repetición", "store.consume(request_id, token, action, arguments)\nwith self.assertRaises(ValueError):\n    store.consume(request_id, token, action, arguments)", "python -m unittest tests.test_approvals.ApprovalTests", "El uso único impide reutilizar un consentimiento antiguo."],
    ]},
  },
  {
    files: ["src/agent_atelier/costs.py", ".env.example", "tests/test_costs.py"], answer: "max_cost_units",
    en: {challenge: "Complete the application-owned cost policy field.", success: "Correct. Cost and latency are separate measurable policies.", guide: "Budgets turn operational wishes into numbers the application can enforce.", steps: [
      ["src/agent_atelier/costs.py", "Define independent policies", "@dataclass(frozen=True)\nclass CostPolicy:\n    max_cost_units: int\n    max_latency_ms: int", "python -m unittest tests.test_costs", "A run may satisfy one limit and fail the other."],
      ["src/agent_atelier/costs.py", "Compare measured use", "within_cost = total_cost_units <= policy.____\nwithin_latency = latency_ms <= policy.max_latency_ms", "python -m unittest tests.test_costs -v", "The teaching cost is abstract; a real adapter records provider usage."],
      [".env.example", "Configure without committing secrets", "AGENT_ATELIER_PROVIDER=simulated\nOPENAI_API_KEY=\nAGENT_ATELIER_MODEL=", "python -m agent_atelier.cli --help", "Environment files stay local; `.env.example` contains names, never values."],
    ]},
    es: {challenge: "Completa el campo de la política de coste controlada por la aplicación.", success: "Correcto. Coste y latencia son políticas medibles independientes.", guide: "Los presupuestos convierten deseos operativos en cifras que la aplicación puede aplicar.", steps: [
      ["src/agent_atelier/costs.py", "Definir políticas independientes", "@dataclass(frozen=True)\nclass CostPolicy:\n    max_cost_units: int\n    max_latency_ms: int", "python -m unittest tests.test_costs", "Una ejecución puede cumplir un límite e incumplir el otro."],
      ["src/agent_atelier/costs.py", "Comparar el uso medido", "within_cost = total_cost_units <= policy.____\nwithin_latency = latency_ms <= policy.max_latency_ms", "python -m unittest tests.test_costs -v", "El coste didáctico es abstracto; un adaptador real registra el uso del proveedor."],
      [".env.example", "Configurar sin publicar secretos", "AGENT_ATELIER_PROVIDER=simulated\nOPENAI_API_KEY=\nAGENT_ATELIER_MODEL=", "python -m agent_atelier.cli --help", "Los archivos de entorno son locales; `.env.example` solo contiene nombres."],
    ]},
  },
  {
    files: ["src/agent_atelier/final_app.py", "src/agent_atelier/provider.py", "src/agent_atelier/preview.py"], answer: "SimulatedProvider",
    en: {challenge: "Type the free deterministic provider used by the default learning path.", success: "Correct. The same engine can later receive an optional real adapter.", guide: "Finally we compose the pieces without hiding them behind a framework.", steps: [
      ["src/agent_atelier/final_app.py", "Compose the application service", "plan = create_research_plan(question, locale)\nstate = run_agent(question, provider, budget)\nusage = estimate_usage(...)\nevaluation = run_evaluation()", "python -m unittest tests.test_final_app", "Composition keeps planning, execution, usage and evaluation inspectable."],
      ["src/agent_atelier/provider.py", "Keep offline learning as the default", "provider = ____()\nstate = run_agent(question, provider, Budget())", "python -m agent_atelier.cli \"How do budgets improve safety?\"", "No key, payment or network is required to understand the architecture."],
      ["src/agent_atelier/preview.py", "Expose only a loopback teaching server", "server = ThreadingHTTPServer((\"127.0.0.1\", port), PreviewHandler)", "python -m agent_atelier.preview", "The browser calls local endpoints; provider secrets never belong in frontend code."],
    ]},
    es: {challenge: "Escribe el proveedor gratuito y determinista utilizado en el recorrido por defecto.", success: "Correcto. El mismo motor puede recibir después un adaptador real opcional.", guide: "Finalmente componemos las piezas sin ocultarlas detrás de un framework.", steps: [
      ["src/agent_atelier/final_app.py", "Componer el servicio de aplicación", "plan = create_research_plan(question, locale)\nstate = run_agent(question, provider, budget)\nusage = estimate_usage(...)\nevaluation = run_evaluation()", "python -m unittest tests.test_final_app", "La composición mantiene visibles planificación, ejecución, uso y evaluación."],
      ["src/agent_atelier/provider.py", "Mantener gratuito el aprendizaje por defecto", "provider = ____()\nstate = run_agent(question, provider, Budget())", "python -m agent_atelier.cli \"¿Cómo mejoran la seguridad los presupuestos?\"", "No se necesita clave, pago ni red para comprender la arquitectura."],
      ["src/agent_atelier/preview.py", "Exponer solo un servidor didáctico local", "server = ThreadingHTTPServer((\"127.0.0.1\", port), PreviewHandler)", "python -m agent_atelier.preview", "El navegador llama a endpoints locales; los secretos nunca pertenecen al frontend."],
    ]},
  },
];
