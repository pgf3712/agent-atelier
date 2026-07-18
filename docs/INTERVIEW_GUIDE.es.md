# Cómo explicar Agent Atelier en una entrevista

## ¿Qué es el proyecto?

Agent Atelier es un laboratorio educativo bilingüe y offline que muestra los mecanismos internos de un agente de IA. Su proveedor determinista permite ejecutar capítulos, pruebas y verificaciones de GitHub sin claves ni costes de modelo.

## ¿Es un agente o un workflow?

El motor es un bucle de agente porque el proveedor elige la siguiente acción estructurada a partir del estado. Aun así, está limitado por políticas similares a un workflow: la aplicación controla herramientas, schemas, presupuestos y estados terminales. Es deliberadamente más acotado que un agente autónomo generalista.

## ¿Por qué implementaste el bucle directamente?

El objetivo pedagógico es hacer visible la autoridad. `engine.py` enseña dónde se propone, valida, ejecuta y registra una acción. Se podría añadir una integración con un framework, pero ocultar esta secuencia debilitaría el aprendizaje.

## ¿Cómo evitas bucles infinitos?

El motor limita pasos, llamadas a herramientas y tiempo transcurrido cooperativo. También genera una huella de cada acción y bloquea repeticiones exactas. Los límites son independientes.

## ¿Cómo proteges las herramientas?

Solo pueden ejecutarse herramientas registradas. Sus argumentos se validan mediante contratos explícitos. La herramienta educativa únicamente consulta un corpus incluido en memoria: no puede leer rutas arbitrarias ni ejecutar comandos.

## ¿Qué controla el proveedor?

Únicamente propone la siguiente acción. No puede ejecutar herramientas, ampliar presupuestos, aprobar acciones sensibles ni validar sus propias citas. Esas decisiones pertenecen a la aplicación.

## ¿Qué diferencia hay entre estado, contexto y memoria?

El estado contiene datos temporales de una ejecución. El contexto es la selección enviada a una decisión. La memoria de sesión conserva deliberadamente información entre ejecuciones. El capítulo 3 muestra las tres capas por separado.

## ¿Cómo observas el agente sin mostrar razonamiento privado?

El motor emite eventos públicos versionados sobre acciones, herramientas validadas, resultados y decisiones de política. Los secretos se redactan y se rechazan eventos de razonamiento privado. La interfaz muestra estos eventos, no cadenas de pensamiento ocultas.

## ¿Cómo gestionas prompt injection?

El contenido recuperado se marca como dato no confiable. Los patrones sospechosos generan avisos, pero la defensa principal es arquitectónica: esos datos no reciben autoridad para cambiar políticas o permisos. La detección por patrones no se presenta como una solución completa.

## ¿Cómo funciona la aprobación humana?

La aprobación queda vinculada a una acción y argumentos exactos. El token es de un solo uso. Reutilizarlo o cambiar los argumentos provoca el rechazo.

## ¿Cómo evalúas el agente?

Cinco escenarios deterministas comprueban respuesta fundamentada, evidencia insuficiente, presupuesto cero, herramienta prohibida y citas inventadas. Cada escenario define estados y comprobaciones esperadas reproducibles en CI.

## ¿Los costes son reales?

No. El capítulo 9 utiliza unidades abstractas claramente etiquetadas. Enseña políticas independientes de coste y latencia sin fingir que los caracteres locales son tokens o dinero.

## ¿Qué cambiarías para producción?

Haría falta un adaptador de proveedor analizado desde seguridad, timeouts de transporte, autenticación, rate limits, almacenamiento persistente, aislamiento multiusuario, gestión de secretos, telemetría, escaneo de dependencias y evaluación específica del despliegue. El servidor incluido es únicamente una vista previa local.

## Resumen final

> Implementé el bucle para enseñar dónde viven realmente la autoridad, la validación y las condiciones de parada. Después convertí esas decisiones en algo observable, comprobable y bilingüe, con un proveedor determinista que cualquiera puede reproducir sin pagar una API.
