# Capítulo 9 — Coste, latencia y presupuestos

## Objetivo

Medir recursos explícitamente y mantener separados los límites de coste y latencia.

## Laboratorio interactivo

Cambia el tamaño de entrada/salida, herramientas y latencia simulada. La calculadora convierte el uso en unidades abstractas e informa si cada presupuesto se cumple. Las unidades abstractas evitan inventar precios de un proveedor real.

## Ejercicio

Crea una configuración que cumpla coste pero falle latencia y otra que haga lo contrario. Explica por qué un único umbral ocultaría información útil.

## Errores frecuentes

- Informar tokens o dólares que el proveedor no devuelve.
- Comprobar el presupuesto solo al terminar.
- Confundir latencia y coste monetario.
- Ocultar los supuestos de estimación.

## Pregunta de entrevista

**¿Cómo controlas el coste de un agente?**

Agent Atelier mide entrada, salida y herramientas, aplica una política explícita y muestra sus supuestos. Un adaptador real sustituiría unidades abstractas por uso del proveedor sin cambiar la frontera presupuestaria.
