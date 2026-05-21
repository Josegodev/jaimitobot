# Jaimito - Bot de Telegram para webs de proyecto

Jaimito es un bot minimo de Telegram para un curso de IA aplicada. Ayuda al alumnado a crear una web estatica de proyecto usando GitHub Pages.

El bot esta pensado para grupos de clase: no responde a todos los mensajes, solo a comandos concretos o cuando se le menciona. Esto reduce ruido y coste de API.

## Para que sirve

Jaimito puede ayudar a:

- Definir las secciones de una web de proyecto.
- Redactar la descripcion del problema y la solucion.
- Explicar como se usa IA en el proyecto.
- Crear ejemplos simples de `index.html`, `styles.css` y `README.md`.
- Revisar textos para la web.
- Explicar GitHub Pages paso a paso.

No publica la web por el alumno y no sustituye la revision docente.

## Requisitos

- Python 3.10 o superior.
- Un bot de Telegram creado con BotFather.
- Una API key de OpenAI.

## Instalacion local

Desde la raiz del repositorio:

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instala dependencias:

```bash
pip install -r telegram_web_assistant/requirements.txt
```

## Configuracion del .env

Copia el archivo de ejemplo:

```bash
copy telegram_web_assistant\.env.example .env
```

En Linux/macOS:

```bash
cp telegram_web_assistant/.env.example .env
```

Edita `.env`:

```env
TELEGRAM_BOT_TOKEN=pon_aqui_el_token_de_telegram
OPENAI_API_KEY=pon_aqui_tu_api_key_de_openai
OPENAI_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.2
TELEGRAM_ALLOWED_CHAT_IDS=
```

No subas `.env` a GitHub. Este repositorio ignora `.env` mediante `.gitignore`.

El archivo `.env` es solo para desarrollo local. En despliegues como Railway, las variables deben configurarse desde el panel del proveedor.

## Ejecucion

```bash
python telegram_web_assistant/jaimito_bot.py
```

El bot usa polling. No necesitas FastAPI, webhooks ni servidor HTTP.

Si falta `TELEGRAM_BOT_TOKEN`, el bot falla al arrancar con un mensaje claro. Si falta `OPENAI_API_KEY`, los comandos que llaman a OpenAI responderan con error controlado.

## Variables de entorno

| Variable | Obligatoria | Valor recomendado | Uso |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Si | Sin valor por defecto | Token del bot creado con BotFather. |
| `OPENAI_API_KEY` | Si para `/pregunta`, `/web` y menciones | Sin valor por defecto | Clave de OpenAI. No debe imprimirse ni subirse al repositorio. |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Modelo usado para responder. |
| `DEFAULT_TEMPERATURE` | No | `0.2` | Controla la variacion de las respuestas. Valor bajo para respuestas consistentes. |
| `TELEGRAM_ALLOWED_CHAT_IDS` | No | Vacio en desarrollo | Lista de chats autorizados separados por comas. Recomendado en clase real. |

## Despliegue en Railway

Este proyecto esta preparado para desplegarse en Railway como worker Python 24/7, sin FastAPI, sin webhooks y sin Docker.

Archivos usados por Railway desde la raiz del repositorio:

- `requirements.txt`: dependencias Python.
- `runtime.txt`: version de Python (`python-3.12`).
- `Procfile`: proceso worker.

Comando de arranque configurado:

```bash
python telegram_web_assistant/jaimito_bot.py
```

Pasos:

1. Sube el repositorio a GitHub.
2. En Railway, crea un nuevo proyecto desde el repositorio.
3. Configura el servicio como worker si Railway no lo detecta automaticamente.
4. En `Variables`, crea:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
   - `DEFAULT_TEMPERATURE`
   - `TELEGRAM_ALLOWED_CHAT_IDS`
5. Despliega el servicio.
6. Comprueba en los logs que aparece el evento `bot_start`.

En Railway no se sube `.env`. Las claves se configuran desde `Variables`.

Para una clase real, configura `TELEGRAM_ALLOWED_CHAT_IDS` con el id del grupo para evitar uso fuera del entorno autorizado.

## Como crear y anadir el bot a Telegram

1. Abre Telegram y habla con `@BotFather`.
2. Usa `/newbot` y sigue los pasos.
3. Copia el token en `TELEGRAM_BOT_TOKEN`.
4. Anade el bot al grupo de clase.
5. Si quieres que lea menciones en grupos, revisa en BotFather la privacidad del bot. Con los comandos funcionara aunque no lea todos los mensajes.

## Comandos disponibles

```text
/start
/ayuda
/pregunta <texto>
/web <texto>
/plantilla_web
/rubrica
/estado
```

Ejemplos:

```text
/pregunta Que secciones debe tener mi web?
/web Dame un index.html simple para mi proyecto
/web Explicame GitHub Pages paso a paso
@JaimitoBot ayudame a explicar mi proyecto
```

Los mensajes normales del grupo se ignoran.

## Whitelist de chats

`TELEGRAM_ALLOWED_CHAT_IDS` permite limitar en que grupos o chats responde el bot.

En desarrollo puede estar vacio:

```env
TELEGRAM_ALLOWED_CHAT_IDS=
```

Para una clase real se recomienda configurarlo:

```env
TELEGRAM_ALLOWED_CHAT_IDS=-1001234567890,123456789
```

Para obtener el `chat_id`, una forma sencilla es:

1. Ejecuta el bot con `TELEGRAM_ALLOWED_CHAT_IDS` vacio.
2. Escribe `/estado` en el grupo.
3. Copia el valor de `Chat ID actual`.
4. Pegalo en `TELEGRAM_ALLOWED_CHAT_IDS`.

No compartas tokens ni API keys en el grupo. Si alguien pega una clave por error, debe revocarla inmediatamente en el proveedor correspondiente.

## Pruebas basicas

Con el bot arrancado:

1. Escribe `/start`.
2. Escribe `/ayuda`.
3. Escribe `/plantilla_web`. Este comando no llama a OpenAI.
4. Escribe `/rubrica`. Este comando no llama a OpenAI.
5. Escribe `/pregunta Que secciones debe tener mi web?`.
6. Escribe `/web Dame una estructura para GitHub Pages`.

## Si OpenAI falla

Comprueba:

- Que `OPENAI_API_KEY` existe en `.env`.
- Que la clave no ha sido revocada.
- Que tienes conexion a internet.
- Que el modelo de `OPENAI_MODEL` esta disponible para tu cuenta.
- Que no hay limites de cuota o facturacion.

El bot no muestra detalles sensibles de errores ni imprime claves.

## Si el bot no responde en grupo

Comprueba:

- Que el bot esta dentro del grupo.
- Que usas `/pregunta`, `/web` o mencionas `@NombreDelBot`.
- Que `TELEGRAM_ALLOWED_CHAT_IDS` esta vacio o contiene el id correcto del grupo.
- Que el bot sigue ejecutandose en la terminal.
- Que el token de Telegram es correcto.
- Que la privacidad del bot en BotFather permite el comportamiento esperado.

## Logs

Los logs salen por stdout en formato JSON. Cada llamada a OpenAI incluye:

- `trace_id`
- `timestamp`
- `chat_id`
- `user_id`
- `command_or_trigger`
- `provider`
- `model`
- `latency_ms`
- `status`
- `error_type` si falla

No se registran tokens ni API keys.
