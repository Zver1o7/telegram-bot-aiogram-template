from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class BotStats:
    started_at: float = field(default_factory=time.time)
    messages_seen: int = 0
    callbacks_seen: int = 0

    def uptime_seconds(self) -> int:
        return max(0, int(time.time() - self.started_at))


stats = BotStats()
