from dataclasses import dataclass
import os

from dotenv import load_dotenv


DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.6


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str | None
    openai_model: str
    default_temperature: float
    telegram_allowed_chat_ids: set[int]

    @property
    def whitelist_enabled(self) -> bool:
        return bool(self.telegram_allowed_chat_ids)


def _parse_allowed_chat_ids(raw_value: str | None) -> set[int]:
    if not raw_value:
        return set()

    chat_ids: set[int] = set()
    for item in raw_value.split(","):
        value = item.strip()
        if not value:
            continue
        try:
            chat_ids.add(int(value))
        except ValueError as exc:
            raise ValueError(
                "TELEGRAM_ALLOWED_CHAT_IDS debe contener ids numericos separados por comas."
            ) from exc
    return chat_ids


def _parse_temperature(raw_value: str | None) -> float:
    if not raw_value:
        return DEFAULT_TEMPERATURE
    try:
        return float(raw_value)
    except ValueError as exc:
        raise ValueError("DEFAULT_TEMPERATURE debe ser un numero.") from exc


def load_settings() -> Settings:
    load_dotenv()

    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not telegram_bot_token:
        raise RuntimeError(
            "Falta TELEGRAM_BOT_TOKEN. Define la variable de entorno o crea un archivo .env."
        )

    return Settings(
        telegram_bot_token=telegram_bot_token,
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip() or None,
        openai_model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        default_temperature=_parse_temperature(os.getenv("DEFAULT_TEMPERATURE")),
        telegram_allowed_chat_ids=_parse_allowed_chat_ids(
            os.getenv("TELEGRAM_ALLOWED_CHAT_IDS")
        ),
    )
