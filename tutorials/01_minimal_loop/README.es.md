# Capítulo 1 — El bucle acotado más pequeño

## Objetivo

Leer y explicar el bucle mínimo que convierte propuestas de acción en una ejecución segura y finita.

## El bucle

La implementación está en `src/agent_atelier/engine.py`:

1. Validar la pregunta de investigación.
2. Crear un estado explícito.
3. Pedir al proveedor una acción estructurada.
4. Validar el tipo de acción y sus campos obligatorios.
5. Detectar llamadas repetidas.
6. Comprobar los presupuestos de pasos y herramientas.
7. Ejecutar solamente una herramienta de la lista permitida.
8. Incorporar al estado las evidencias devueltas.
9. Aceptar la respuesta final solo si todas sus citas existen en el estado.
10. Terminar con un estado nominal y observable.

## ¿Por qué debe estar acotado?

Sin condiciones de parada obligatorias, un modelo puede repetir herramientas, consumir tiempo sin límite o continuar cuando ya no dispone de evidencias útiles. El prompt puede pedirle que se detenga, pero es la aplicación quien debe garantizarlo.

Finales implementados:

- `completed`
- `insufficient_evidence`
- `budget_exhausted`
- `blocked`
- `failed` (reservado para una política de errores posterior)

## Pruébalo

Ejecuta:

```bash
PYTHONPATH=src python -m agent_atelier.cli "How do agent budgets improve safety?"
```

Después establece en cero el presupuesto de herramientas desde la web. El proveedor seguirá proponiendo una búsqueda, pero el motor impedirá que se ejecute.

## Ejercicio

Añade un proveedor de prueba que proponga una respuesta con la cita `E-999`. Predice el estado final antes de ejecutar la prueba.

Resultado esperado: `blocked`, porque los identificadores de evidencia nacen de resultados de herramientas; el proveedor no puede inventarlos.

## Errores frecuentes

- Contar solamente las herramientas que terminan correctamente.
- Definir el límite de pasos únicamente en el prompt.
- Confiar en el JSON del proveedor solo porque se ha podido parsear.
- Generar una respuesta convincente cuando la búsqueda no devuelve evidencias.

## Comprueba lo aprendido

**¿Cómo evitas los bucles infinitos?**

Agent Atelier impone pasos y llamadas máximas desde la aplicación, registra huellas de las acciones para detectar repeticiones y utiliza estados terminales explícitos. Estos controles no dependen de que el proveedor obedezca las instrucciones.
