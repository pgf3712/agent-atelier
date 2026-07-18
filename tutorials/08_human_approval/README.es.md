# Capítulo 8 — Aprobación humana

## Objetivo

Pausar efectos sensibles y conceder un permiso limitado que no pueda reutilizarse.

## Laboratorio interactivo

Propón exportar el informe `B-001` como Markdown. Aprueba o deniega. La aprobación crea una capacidad ligada a la acción y argumentos exactos; al usarla se consume. Un segundo uso falla.

La demo no escribe un archivo real. Enseña por separado la transición de autorización y el efecto lateral.

## Ejercicio

Aprueba Markdown e intenta exportar PDF con el mismo permiso. Explica por qué debe rechazarse por su digest de argumentos.

## Errores frecuentes

- Pedir permiso después de actuar.
- Interpretar un «sí» global como permiso futuro.
- Reutilizar tokens de aprobación.
- Mostrar una confirmación sin argumentos ni consecuencias.

## Pregunta de entrevista

**¿Qué acciones requieren aprobación humana?**

Las acciones con efectos externos, cambios irreversibles, divulgación sensible o gasto deben detenerse. Agent Atelier vincula el permiso a una acción y argumentos exactos y lo consume una sola vez.
