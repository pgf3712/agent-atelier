# Capítulo 4 — Planificación y progreso

## Objetivo

Convertir un objetivo amplio en pasos explícitos y comprobables, recordando que un plan es una hipótesis modificable, no una garantía.

## Laboratorio interactivo

Crea un plan de investigación, revisa las condiciones de éxito y utiliza el control didáctico para simular que la aplicación ha recibido una prueba de la condición activa. El siguiente paso solo se activa después de esa verificación simulada.

`ResearchPlan` separa objetivo, pasos, condiciones y estados. El proveedor no certifica su propio trabajo; la aplicación controla el avance. En producción, el botón debe sustituirse por una comprobación de evidencias, un resultado de herramienta o una decisión humana.

## Ejercicio

Añade una operación de revisión que reactive un paso completado y registre el motivo. Decide si debe reabrir también los pasos posteriores.

## Errores frecuentes

- Confundir texto con estado ejecutable.
- Crear pasos sin condiciones de éxito.
- Completar pasos porque el modelo afirma haberlos realizado.
- Negarse a revisar un plan después de recibir nuevas evidencias.

## Pregunta de entrevista

**¿Por qué representas la planificación explícitamente?**

Porque permite inspeccionar y probar el progreso. Agent Atelier mantiene los estados bajo control de la aplicación y exige condiciones de éxito en lugar de confiar en narraciones convincentes.
