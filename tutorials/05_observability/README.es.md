# Capítulo 5 — Eventos, trazas y depuración

## Objetivo

Observar la ejecución sin exponer secretos ni cadenas de pensamiento privadas.

## Laboratorio interactivo

Publica un evento seguro, prueba otro que contiene una clave y solicita publicar razonamiento privado. La aplicación oculta el secreto y rechaza el tipo de evento privado.

Los eventos públicos explican qué ocurrió: categoría de acción, herramienta validada, identificadores de resultado, decisiones de política y estado final. No muestran borradores internos.

## Ejercicio

Incluye un secreto canario dentro de una lista anidada y demuestra que nunca aparece en la salida serializada.

## Errores frecuentes

- Registrar peticiones y cabeceras completas.
- Llamar observabilidad al razonamiento privado.
- Usar payloads sin versión.
- Guardar resultados completos sin límites de tamaño o sensibilidad.

## Comprueba lo aprendido

**¿Cómo haces observable un agente de forma segura?**

Agent Atelier emite tipos de evento permitidos y versionados con payloads redactados. Muestra acciones y resultados diseñados para depurar, mientras rechaza explícitamente eventos de razonamiento privado.
