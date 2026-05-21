import time

from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError

from config import Settings
from logging_utils import log_event
from prompts import SYSTEM_PROMPT


MAX_OUTPUT_TOKENS = 1200
OPENAI_TIMEOUT_SECONDS = 25


class OpenAIClientError(Exception):
    pass


def ask_openai(
    *,
    settings: Settings,
    trace_id: str,
    chat_id: int | None,
    user_id: int | None,
    command_or_trigger: str,
    user_text: str,
    extra_context: str | None = None,
) -> str:
    if not settings.openai_api_key:
        raise OpenAIClientError(
            "Falta OPENAI_API_KEY. Configurala en variables de entorno o en .env."
        )

    client = OpenAI(api_key=settings.openai_api_key, timeout=OPENAI_TIMEOUT_SECONDS)
    started = time.perf_counter()
    status = "ok"
    error_type = None

    user_content = user_text
    if extra_context:
        user_content = f"{extra_context}\n\nConsulta del alumno:\n{user_text}"

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=settings.default_temperature,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            status = "error"
            error_type = "empty_response"
            raise OpenAIClientError("OpenAI no devolvio contenido.")
        return content.strip()
    except APITimeoutError as exc:
        status = "error"
        error_type = "timeout"
        raise OpenAIClientError(
            "OpenAI ha tardado demasiado en responder. Prueba de nuevo en unos segundos."
        ) from exc
    except APIConnectionError as exc:
        status = "error"
        error_type = "network"
        raise OpenAIClientError(
            "No se pudo conectar con OpenAI. Revisa la conexion y prueba de nuevo."
        ) from exc
    except OpenAIError as exc:
        status = "error"
        error_type = type(exc).__name__
        raise OpenAIClientError(
            "OpenAI no pudo procesar la consulta ahora. Prueba de nuevo mas tarde."
        ) from exc
    finally:
        latency_ms = round((time.perf_counter() - started) * 1000)
        log_event(
            "openai_call",
            trace_id=trace_id,
            chat_id=chat_id,
            user_id=user_id,
            command_or_trigger=command_or_trigger,
            provider="openai",
            model=settings.openai_model,
            latency_ms=latency_ms,
            status=status,
            error_type=error_type,
        )
