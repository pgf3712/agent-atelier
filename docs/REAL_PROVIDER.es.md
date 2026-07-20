# Proveedor de modelo real opcional

Agent Atelier puede estudiarse por completo con `SimulatedProvider`: es gratuito, determinista y se utiliza en las pruebas. El adaptador de OpenAI es una capa comparativa opcional para el capítulo 10; no es un requisito ni sustituye al arnés.

## Qué cambia

El motor, los presupuestos, la validación de herramientas y la comprobación de citas siguen bajo control de la aplicación. `OpenAIResponsesProvider` sustituye únicamente el componente que propone la siguiente acción. Utiliza el flujo de function calling de Responses API: el modelo propone `search_local_corpus`, la aplicación valida y ejecuta la herramienta y devuelve el resultado al modelo. El diseño sigue la [guía oficial de function calling](https://developers.openai.com/api/docs/guides/function-calling).

## Instalar la dependencia opcional

```powershell
python -m pip install -e ".[real]"
```

## Configurar el servidor local

Crea una clave en el panel de OpenAI y expónla como variable de entorno. La [guía oficial de inicio](https://developers.openai.com/api/docs/quickstart) indica que los SDK de OpenAI leen `OPENAI_API_KEY` desde el entorno.

Elige un modelo disponible en tu propio proyecto de API. Agent Atelier no fija un modelo por defecto porque las recomendaciones y la disponibilidad cambian.

Solo para la ventana actual de PowerShell:

```powershell
$env:OPENAI_API_KEY="tu-clave"
$env:AGENT_ATELIER_MODEL="id-de-un-modelo-habilitado"
$env:AGENT_ATELIER_PROVIDER="openai"
python -m agent_atelier.preview
```

Después abre el capítulo 10, selecciona OpenAI y confirma el aviso de API externa y costes. Para volver al recorrido gratuito, selecciona `Simulado` o elimina `AGENT_ATELIER_PROVIDER`.

## Lanzador de Windows más seguro

Después de instalar la dependencia opcional, haz doble clic en `OPEN_AGENT_ATELIER_REAL.bat`. Solicita el ID del modelo habilitado y después pide la clave mediante una entrada oculta de PowerShell. La clave nunca entra en el navegador, solo se expone al proceso local de vista previa y se elimina del entorno del proceso cuando se cierra el servidor.

El archivo normal `OPEN_AGENT_ATELIER.bat` siempre inicia el simulador gratuito y nunca solicita secretos. La guía de seguridad de claves de OpenAI recomienda variables de entorno y advierte que no se deben desplegar secretos en aplicaciones cliente.

## Fronteras de seguridad y coste

- La clave permanece en el entorno del proceso servidor. Nunca se acepta desde el navegador, se almacena en el navegador, se devuelve en respuestas ni se escribe en los logs de la aplicación.
- El simulador sigue siendo la opción predeterminada. La interfaz explica cuándo falta el SDK opcional y exige modelo y consentimiento de coste para una petición real.
- El proveedor real exige una confirmación explícita porque la pregunta sale del ordenador y el uso puede generar costes.
- La única función expuesta es la búsqueda permitida en el corpus local.
- Los argumentos siguen pasando por `validate_arguments`.
- Las citas siguen pasando por la comprobación de identificadores del motor.
- La vista previa se limita al equipo local por defecto.
- Nunca publiques `.env`, historiales de terminal con claves ni logs reales con prompts sensibles.

## Lo que no afirma este adaptador

Es una integración educativa, no un gateway de producción. Una versión productiva necesitaría autenticación, cuotas por usuario, reintentos y backoff, cancelación, contabilidad real de uso, reglas de conservación de auditoría y evaluaciones adversariales más amplias.
