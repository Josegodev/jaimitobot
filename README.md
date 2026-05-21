# Jaimito

Bot de Telegram en Python para ayudar al alumnado de un curso de IA aplicada a crear una web estatica de proyecto con GitHub Pages.

El bot se ejecuta como worker Python 24/7, usa polling con `python-telegram-bot` y llama directamente a la API de OpenAI. No usa FastAPI, webhooks ni Docker.

## Ejecucion local

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
pip install -r requirements.txt
```

Crea `.env` a partir del ejemplo:

```bash
copy telegram_web_assistant\.env.example .env
```

En Linux/macOS:

```bash
cp telegram_web_assistant/.env.example .env
```

Arranca el bot:

```bash
python telegram_web_assistant/jaimito_bot.py
```

## Variables de entorno

| Variable | Obligatoria | Valor por defecto | Uso |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Si | Ninguno | Token del bot de Telegram. |
| `OPENAI_API_KEY` | Si para consultas OpenAI | Ninguno | Clave de OpenAI. |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Modelo usado por el bot. |
| `DEFAULT_TEMPERATURE` | No | `0.2` | Variacion de las respuestas. |
| `TELEGRAM_ALLOWED_CHAT_IDS` | No | Vacio | Chats permitidos, separados por comas. |

No subas `.env` a GitHub.

## Despliegue en Railway

Este repositorio incluye los archivos necesarios para Railway:

- `requirements.txt`
- `runtime.txt`
- `Procfile`

Comando de arranque:

```bash
python telegram_web_assistant/jaimito_bot.py
```

En Railway no se sube `.env`. Las claves se configuran desde `Variables`:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `DEFAULT_TEMPERATURE`
- `TELEGRAM_ALLOWED_CHAT_IDS`

Para una clase real, configura `TELEGRAM_ALLOWED_CHAT_IDS` con el id del grupo autorizado.

Mas detalle en [telegram_web_assistant/README.md](telegram_web_assistant/README.md).
