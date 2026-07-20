# Capítulo 0 — ¿Agente, workflow o chatbot?

## Objetivo

Reconocer qué convierte un sistema en agéntico sin llamar “agente” a cualquier aplicación con un LLM.

## Modelo mental

- **Chatbot:** recibe un mensaje y genera una respuesta. Puede tener instrucciones, pero no necesariamente actúa.
- **Workflow:** sigue una secuencia elegida por quien desarrolla el sistema. Sus ramas son explícitas y predecibles.
- **Agente:** recibe un objetivo y puede elegir entre acciones permitidas, mientras la aplicación impone límites y permisos.

Un agente no es simplemente «un LLM que llama funciones». La aplicación que lo rodea debe validar acciones propuestas, ejecutar herramientas, devolver observaciones y decidir cuándo debe detenerse.

```text
objetivo → el proveedor propone → la aplicación valida → herramienta
   ↑                                                   ↓
   └──────────── estado + observación segura ──────────┘
```

## En Agent Atelier

`SimulatedProvider` propone un `AgentAction`. Nunca ejecuta herramientas. `run_agent` controla el bucle, comprueba el presupuesto, rechaza herramientas desconocidas, ejecuta las permitidas y valida las citas finales.

La separación es intencionada: la salida del modelo es una propuesta, no una autorización.

## Ejercicio

Clasifica cada sistema y explica por qué:

1. Un script fijo obtiene datos de ventas y envía el mismo informe cada lunes.
2. Un asistente de soporte decide entre consultar documentación, pedir un número de pedido o escalar a una persona.
3. Un chat reformula un párrafo sin utilizar herramientas.

Clasificación sugerida: workflow, agente y chatbot. Una buena respuesta explica quién elige la siguiente acción y qué límites siguen bajo el control de la aplicación.

## Error frecuente

Llamar agente a un workflow determinista porque utiliza un LLM. El uso del modelo en uno de sus pasos no define la arquitectura del sistema completo.

## Comprueba lo aprendido

**¿Por qué separaste el proveedor del motor?**

Porque un proveedor puede equivocarse o sustituirse. El motor debe conservar el control de herramientas, presupuestos, validación y estado observable independientemente del modelo que proponga la acción.
