# Capítulo 6 — Guardrails y datos no fiables

## Objetivo

Mantener las salidas del proveedor y los documentos recuperados dentro de fronteras explícitas de datos.

## Laboratorio interactivo

Inspecciona una fuente normal y otra con «ignora las instrucciones anteriores». Ambas se clasifican como datos recuperados no fiables; la sospechosa añade una advertencia. Ninguna puede conceder permisos.

La detección de patrones es defensa adicional, no una solución completa. El control fuerte es arquitectónico: el texto es dato, las herramientas permanecen permitidas explícitamente y la política de la aplicación controla la ejecución.

## Ejercicio

Prueba un documento demasiado grande y comprueba que se rechaza antes de almacenarlo o enviarlo al proveedor. Añade después una frase benigna con la palabra «instrucciones» evitando un falso positivo.

## Errores frecuentes

- Pedir al mismo modelo que decida si algo es seguro y confiar ciegamente.
- Tratar una web conocida como fuente de instrucciones fiables.
- Intentar resolver la inyección solo mediante una frase en el prompt.
- Dar a los contenidos recuperados herramientas sin restricciones.

## Pregunta de entrevista

**¿Cómo mitigas prompt injection?**

Agent Atelier marca el contenido recuperado como dato no fiable, aplica límites y advertencias, impide que modifique herramientas, valida cada acción y mantiene operaciones sensibles bajo políticas de aplicación.
