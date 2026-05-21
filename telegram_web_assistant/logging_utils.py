import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        stream=sys.stdout,
    )


def new_trace_id() -> str:
    return uuid4().hex


def log_event(event: str, **fields: Any) -> None:
    payload = {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **fields,
    }
    logging.info(json.dumps(payload, ensure_ascii=True, default=str))
