# Capítulo 10 — Aplicación completa de informes

## Objetivo

Ejecutar el sistema offline completo y conectar los conceptos anteriores sin mostrar todos los detalles al mismo tiempo.

## Laboratorio interactivo

Envía una pregunta. La aplicación muestra primero el resultado. Despliega plan, evidencias, eventos públicos, uso y evaluación únicamente cuando los necesites.

El servicio integrado:

1. Valida y planifica la pregunta.
2. Ejecuta el agente acotado con el proveedor simulado.
3. Utiliza únicamente la herramienta local registrada.
4. Acepta solo citas conocidas.
5. Se detiene con honestidad cuando faltan evidencias.
6. Estima uso abstracto y latencia.
7. Incluye evidencia de evaluación determinista.

## Ejercicio

Ejecuta una pregunta soportada y otra sin evidencias. Compara plan, evidencias, limitaciones y estado final. Pon después a cero el presupuesto de herramientas en código y predice el resultado.

## Errores frecuentes

- Sustituir la progresión educativa por un dashboard complejo.
- Confundir integración con preparación para producción.
- Ocultar limitaciones cuando una ejecución termina bien.
- Mantener lógica de demostración diferente del motor probado.

## Pregunta de entrevista

**¿Qué cambiarías para producción?**

Añadiría aislamiento multiusuario autenticado, almacenamiento transaccional, proveedores reales con uso, caducidad e identidad para aprobaciones, trazas distribuidas, seguridad de contenidos, despliegue endurecido y monitorización. El núcleo educativo no afirma incluir estas capacidades.
