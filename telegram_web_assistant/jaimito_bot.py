import re

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import Settings, load_settings
from logging_utils import configure_logging, log_event, new_trace_id
from openai_client import OpenAIClientError, ask_openai
from prompts import PLANTILLA_WEB, QUESTION_CONTEXT, RUBRICA, WEB_CONTEXT


TELEGRAM_MESSAGE_LIMIT = 3900
APP_VERSION = "hide-trace-id-2026-05-21"
COURSE_LINK = "https://josegodev.github.io/CURSO_IA/"
# In-memory counters are acceptable for this classroom bot. They reset on container restart.
QUESTION_COUNTS: dict[str, int] = {}
COURSE_LINK_SENT: set[str] = set()


def _settings(context: ContextTypes.DEFAULT_TYPE) -> Settings:
    return context.application.bot_data["settings"]


def get_user_chat_key(update: Update) -> str:
    chat_id = update.effective_chat.id if update.effective_chat else "unknown_chat"
    user_id = update.effective_user.id if update.effective_user else "unknown_user"
    return f"{chat_id}:{user_id}"


def _is_allowed(update: Update, settings: Settings) -> bool:
    chat = update.effective_chat
    if not chat or not settings.whitelist_enabled:
        return True
    return chat.id in settings.telegram_allowed_chat_ids


def clean_user_message(text: str) -> str:
    """Remove internal trace data from messages sent to Telegram users."""
    if not text:
        return ""
    lines = text.splitlines()
    return "\n".join(
        line for line in lines
        if not line.strip().lower().startswith("trace_id:")
    ).strip()


async def _send_text(update: Update, text: str) -> None:
    if not update.effective_message:
        return
    # trace_id is kept in logs only; it is never exposed to Telegram users.
    clean_text = clean_user_message(text)
    await update.effective_message.reply_text(clean_text[:TELEGRAM_MESSAGE_LIMIT])


async def reply_long_text(message, text: str) -> None:
    cleaned = clean_user_message(text)
    if not cleaned:
        await message.reply_text("No he podido generar una respuesta util.")
        return

    chunks = []
    current = ""

    for paragraph in cleaned.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) + 2 <= TELEGRAM_MESSAGE_LIMIT:
            current = f"{current}\n\n{paragraph}".strip()
        else:
            if current:
                chunks.append(current)
            if len(paragraph) <= TELEGRAM_MESSAGE_LIMIT:
                current = paragraph
            else:
                for i in range(0, len(paragraph), TELEGRAM_MESSAGE_LIMIT):
                    chunks.append(paragraph[i : i + TELEGRAM_MESSAGE_LIMIT])
                current = ""

    if current:
        chunks.append(current)

    for chunk in chunks:
        await message.reply_text(chunk)


async def maybe_send_course_link(update: Update) -> None:
    message = update.effective_message
    if not message:
        return

    key = get_user_chat_key(update)
    QUESTION_COUNTS[key] = QUESTION_COUNTS.get(key, 0) + 1

    if QUESTION_COUNTS[key] < 2 or key in COURSE_LINK_SENT:
        return

    COURSE_LINK_SENT.add(key)
    chat = update.effective_chat
    user = update.effective_user
    log_event(
        "course_link_sent",
        chat_id=chat.id if chat else None,
        user_id=user.id if user else None,
        question_count=QUESTION_COUNTS[key],
        status="ok",
    )
    await message.reply_text(
        "Por cierto, aqui tienes la web del curso para continuar con el proyecto:\n"
        f"{COURSE_LINK}"
    )


async def _reject_if_unauthorized(update: Update, settings: Settings) -> bool:
    if _is_allowed(update, settings):
        return False
    chat = update.effective_chat
    user = update.effective_user
    log_event(
        "unauthorized_chat",
        chat_id=chat.id if chat else None,
        user_id=user.id if user else None,
        status="ignored",
    )
    await _send_text(update, "Este chat no esta autorizado para usar Jaimito.")
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return
    await _send_text(
        update,
        "Hola, soy Jaimito.\n\n"
        "Te ayudo a preparar tu proyecto final del curso: una web sencilla donde "
        "explicaras una idea de uso de IA para resolver un problema real.\n\n"
        "Puedes pedirme ayuda para:\n"
        "- elegir una idea,\n"
        "- explicar el problema,\n"
        "- ordenar las secciones de la web,\n"
        "- escribir textos claros,\n"
        "- preparar la presentacion final.\n\n"
        "Usa:\n"
        "/pregunta tu duda\n"
        "/web ayuda especifica para tu web\n"
        "/plantilla_web para ver las secciones recomendadas\n"
        "/rubrica para ver como se valorara el proyecto",
    )


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return
    await _send_text(
        update,
        "Ejemplos de uso:\n\n"
        "/pregunta No se que problema elegir para mi proyecto\n\n"
        "/web Quiero hacer una web sobre una tienda que usa IA para responder "
        "preguntas de clientes\n\n"
        "/plantilla_web\n"
        "/rubrica\n\n"
        "No hace falta saber programar mucho. La idea es explicar bien el "
        "problema, la solucion y como la IA puede ayudar.\n\n"
        "En un grupo tambien puedes mencionarme con @nombre_bot y escribir tu duda.",
    )


async def plantilla_web(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return
    await _send_text(update, PLANTILLA_WEB)


async def rubrica(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return
    await _send_text(update, RUBRICA)


async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return
    whitelist = "activa" if settings.whitelist_enabled else "inactiva"
    chat = update.effective_chat
    await _send_text(
        update,
        "Jaimito esta operativo.\n"
        f"Modelo configurado: {settings.openai_model}\n"
        f"Whitelist de chat: {whitelist}\n"
        f"Chat ID actual: {chat.id if chat else 'no disponible'}",
    )


async def _handle_ai_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    command_or_trigger: str,
    user_text: str,
    extra_context: str | None = None,
) -> None:
    settings = _settings(context)
    if await _reject_if_unauthorized(update, settings):
        return

    if not user_text.strip():
        await _send_text(update, "Escribe tu consulta despues del comando.")
        return

    trace_id = new_trace_id()
    chat = update.effective_chat
    user = update.effective_user

    try:
        answer = ask_openai(
            settings=settings,
            trace_id=trace_id,
            chat_id=chat.id if chat else None,
            user_id=user.id if user else None,
            command_or_trigger=command_or_trigger,
            user_text=user_text.strip(),
            extra_context=extra_context,
        )
        if not update.effective_message:
            return
        await reply_long_text(update.effective_message, answer)
        await maybe_send_course_link(update)
    except OpenAIClientError as exc:
        log_event(
            "bot_response_error",
            trace_id=trace_id,
            chat_id=chat.id if chat else None,
            user_id=user.id if user else None,
            command_or_trigger=command_or_trigger,
            status="error",
            error_type=type(exc).__name__,
        )
        await _send_text(
            update,
            "No he podido responder ahora. Intentalo de nuevo en unos segundos.",
        )


async def pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_ai_request(
        update,
        context,
        command_or_trigger="/pregunta",
        user_text=" ".join(context.args),
        extra_context=QUESTION_CONTEXT,
    )


async def web(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_ai_request(
        update,
        context,
        command_or_trigger="/web",
        user_text=" ".join(context.args),
        extra_context=WEB_CONTEXT,
    )


def _remove_bot_mention(text: str, bot_username: str | None) -> str:
    if not bot_username:
        return text
    pattern = re.compile(rf"@{re.escape(bot_username)}\b", flags=re.IGNORECASE)
    return pattern.sub("", text).strip()


async def mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    bot_username = context.bot.username
    if not bot_username or f"@{bot_username.lower()}" not in message.text.lower():
        return

    user_text = _remove_bot_mention(message.text, bot_username)
    await _handle_ai_request(
        update,
        context,
        command_or_trigger="mention",
        user_text=user_text,
        extra_context=WEB_CONTEXT,
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_event(
        "telegram_error",
        trace_id=new_trace_id(),
        status="error",
        error_type=type(context.error).__name__ if context.error else None,
    )


def build_application(settings: Settings) -> Application:
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", ayuda))
    application.add_handler(CommandHandler("pregunta", pregunta))
    application.add_handler(CommandHandler("web", web))
    application.add_handler(CommandHandler("plantilla_web", plantilla_web))
    application.add_handler(CommandHandler("rubrica", rubrica))
    application.add_handler(CommandHandler("estado", estado))
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND
            & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
            mention,
        )
    )
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    configure_logging()
    settings = load_settings()
    application = build_application(settings)
    log_event(
        "bot_start",
        provider="telegram",
        app_version=APP_VERSION,
        model=settings.openai_model,
        whitelist_enabled=settings.whitelist_enabled,
        status="ok",
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
