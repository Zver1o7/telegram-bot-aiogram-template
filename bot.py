from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent

from config import get_settings
from handlers import get_routers


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


logger = logging.getLogger(__name__)


async def on_error(event: ErrorEvent) -> bool:
    logger.exception("Unhandled error: %s", event.exception, exc_info=event.exception)
    return True


async def main() -> None:
    setup_logging()
    settings = get_settings()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.errors.register(on_error)

    for router in get_routers():
        dp.include_router(router)

    logger.info("Bot starting (polling)...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
