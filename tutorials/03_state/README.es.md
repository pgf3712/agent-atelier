# Capítulo 3 — Estado, contexto y memoria

## Objetivo

Separar tres conceptos que suelen utilizarse incorrectamente como sinónimos.

- **Estado de ejecución:** datos cambiantes de una única ejecución, como pasos, evidencias y estado final.
- **Contexto:** selección de información disponible para tomar la siguiente decisión.
- **Memoria:** información conservada deliberadamente para recuperarla en ejecuciones posteriores.

El contexto es una vista, no una base de datos. La memoria no debe contener automáticamente todo lo visto. El estado no puede filtrarse silenciosamente a otra sesión.

## Laboratorio interactivo

Guarda una preferencia, inicia otra ejecución y compara los tres bloques. Cambia el valor temporal, se reconstruye el contexto y el dato recordado permanece hasta borrarlo. El almacén está en memoria, por lo que cerrar el servidor lo vacía intencionadamente.

## Ejercicio

Guarda un dato para `paula` y otro para `guest`. Comprueba que las sesiones no se mezclan y borra únicamente `guest`.

## Errores frecuentes

- Enviar la base de datos completa al modelo como contexto.
- Persistir todos los mensajes como memoria permanente.
- Compartir una lista global entre usuarios.
- Permitir escrituras de memoria sin una política de aplicación.
- Suponer que un dato recordado siempre seguirá siendo correcto.

## Comprueba lo aprendido

**¿Cómo diferencias estado, contexto y memoria?**

El estado pertenece a una ejecución, el contexto es una selección acotada para decidir y la memoria es información conservada explícitamente entre ejecuciones. Agent Atelier representa y prueba esos ciclos de vida por separado.
