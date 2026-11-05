from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


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


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "BOT_TOKEN не задан. Создайте файл .env на основе .env.example и укажите токен."
        )
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
    db_path = os.getenv("DB_PATH", "data/bot.db").strip() or "data/bot.db"
    return Settings(
        bot_token=token, log_level=log_level, admin_ids=admin_ids, db_path=db_path
    )
