# Capítulo 7 — Evaluación reproducible

## Objetivo

Sustituir la afirmación vaga «el agente funciona» por escenarios concretos y resultados esperados exactos.

## Laboratorio interactivo

Ejecuta la misma batería determinista usada por consola y pruebas. Cada caso muestra estado esperado, estado real y comprobaciones calculables.

Los contratos actuales cubren respuesta con evidencias, información insuficiente, presupuesto cero, herramienta prohibida y cita inventada.

## Ejercicio

Provoca un fallo cambiando un estado esperado. Lee el informe, restaura el contrato y añade un escenario de argumentos mal formados.

## Errores frecuentes

- Medir únicamente el estilo de la respuesta.
- Usar una demostración feliz como evaluación completa.
- Pedir a un modelo que juzgue controles con respuestas deterministas.
- Publicar una media sin mostrar fallos individuales.

## Comprueba lo aprendido

**¿Cómo evalúas un agente?**

Agent Atelier comienza con contratos deterministas para herramientas, schemas, parada, presupuestos y citas. Las rúbricas humanas o basadas en modelos pueden evaluar lenguaje después, pero no sustituyen comprobaciones exactas de seguridad.
