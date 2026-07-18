# Capítulo 2 — Herramientas tipadas y schemas

## Objetivo

Comprender por qué una llamada a herramienta es una propuesta no fiable y cómo la aplicación la convierte en una operación validada.

## Modelo mental

Una herramienta tiene cuatro partes independientes:

1. Un nombre estable que el proveedor puede proponer.
2. Una descripción comprensible de su finalidad.
3. Un contrato de argumentos controlado por la aplicación.
4. Un handler que puede ejecutar la aplicación, nunca directamente el proveedor.

```text
JSON del proveedor
     ↓ no fiable
lista permitida de herramientas
     ↓
campos obligatorios → tipos → restricciones → rechazo de extras
     ↓ validado
la aplicación invoca el handler
```

## El contrato de Agent Atelier

`ArgumentSpec` registra actualmente:

- Tipo de valor de Python.
- Descripción comprensible.
- Si el campo es obligatorio.
- Longitud mínima para textos.

`validate_arguments` rechaza:

- Argumentos que no formen un objeto.
- Campos obligatorios ausentes.
- Tipos incorrectos.
- Búsquedas vacías después de normalizarlas.
- Campos inesperados.

Rechazar campos inesperados es importante. Un proveedor no puede introducir un `path`, una `url` o un `command` no revisados dentro de una herramienta cuyo contrato solo permite `query`.

## Descubrimiento de herramientas

`public_tool_catalog()` expone solamente metadatos seguros, nunca funciones ejecutables. La vista local publica el catálogo mediante `GET /api/tools`, para que la futura pantalla Tools y el tutorial compartan la misma fuente de verdad que el motor.

## Ejercicio

Amplía `ArgumentSpec` con una longitud máxima opcional y añade pruebas para una consulta que la supere. Decide si la normalización debe ejecutarse antes o después de medirla y explica el motivo.

Diseño esperado: normalizar primero para que los espacios externos no consuman el límite y rechazar el texto demasiado largo antes de ejecutar el handler.

## Errores frecuentes

- Suponer que un JSON válido contiene argumentos válidos.
- Permitir al proveedor elegir cualquier función.
- Ignorar argumentos inesperados.
- Duplicar validaciones diferentes dentro de cada handler.
- Mostrar excepciones internas sin tratar.
- Confundir la descripción de una herramienta con un control de seguridad.

## Pregunta de entrevista

**¿Cómo validas las llamadas a herramientas?**

Agent Atelier resuelve el nombre propuesto mediante un registro explícito, valida el objeto completo con un contrato controlado por la aplicación, rechaza campos ausentes, incorrectos o inesperados y solo entonces ejecuta el handler. El proveedor nunca recibe una función Python ni autoridad directa de ejecución.
