from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

APP_VERSION = "0.4.0"


def _parse_admin_ids(raw: str) -> frozenset[int]:
    ids: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.add(int(part))
        except ValueError:
            continue
    return frozenset(ids)


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"
    admin_ids: frozenset[int] = field(default_factory=frozenset)
    db_path: str = "data/bot.db"
    run_mode: str = "polling"  # polling | webhook
    webhook_base_url: str = ""
    webhook_path: str = "/webhook"
    webhook_secret: str = ""
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    throttle_seconds: float = 0.7


def _get_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "BOT_TOKEN не задан. Создайте файл .env на основе .env.example и укажите токен."
        )
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
    db_path = os.getenv("DB_PATH", "data/bot.db").strip() or "data/bot.db"
    run_mode = os.getenv("RUN_MODE", "polling").strip().lower() or "polling"
    webhook_base_url = os.getenv("WEBHOOK_BASE_URL", "").strip().rstrip("/")
    webhook_path = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
    if not webhook_path.startswith("/"):
        webhook_path = "/" + webhook_path
    webhook_secret = os.getenv("WEBHOOK_SECRET", "").strip()
    app_host = os.getenv("APP_HOST", "0.0.0.0").strip() or "0.0.0.0"
    app_port = _get_int("APP_PORT", 8080)
    throttle_seconds = max(0.0, _get_float("THROTTLE_SECONDS", 0.7))
    return Settings(
        bot_token=token,
        log_level=log_level,
        admin_ids=admin_ids,
        db_path=db_path,
        run_mode=run_mode,
        webhook_base_url=webhook_base_url,
        webhook_path=webhook_path,
        webhook_secret=webhook_secret,
        app_host=app_host,
        app_port=app_port,
        throttle_seconds=throttle_seconds,
    )
