from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, min_interval: float = 0.7) -> None:
        self.min_interval = max(0.0, float(min_interval))
        self._last_seen: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if self.min_interval <= 0 or not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)
        if event.from_user.is_bot:
            return await handler(event, data)

        uid = event.from_user.id
        now = time.monotonic()
        last = self._last_seen.get(uid, 0.0)
        if now - last < self.min_interval:
            # Drop silently for mild throttling; avoids chat spam.
            return None
        self._last_seen[uid] = now
        # Simple cleanup to bound memory.
        if len(self._last_seen) > 5000:
            cutoff = now - self.min_interval * 10
            self._last_seen = {k: v for k, v in self._last_seen.items() if v >= cutoff}
        return await handler(event, data)
