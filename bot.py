from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

from aiohttp import web
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, ErrorEvent, Message, TelegramObject
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import get_settings
from handlers import get_routers
from middlewares.throttling import ThrottlingMiddleware
from runtime import stats
from storage.db import Database

logger = logging.getLogger(__name__)


class MessageStatsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        stats.messages_seen += 1
        return await handler(event, data)


class CallbackStatsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        stats.callbacks_seen += 1
        return await handler(event, data)


class UserTrackingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user and not event.from_user.is_bot:
            db: Database | None = data.get("db")
            if db:
                try:
                    await db.upsert_user(
                        event.from_user.id,
                        event.from_user.username,
                        event.from_user.first_name,
                    )
                except Exception:
                    logger.warning("Failed to upsert user", exc_info=True)
        return await handler(event, data)


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


BOT_COMMANDS = [
    BotCommand(command="start", description="Начать работу с ботом"),
    BotCommand(command="help", description="Показать справку"),
    BotCommand(command="about", description="О боте"),
    BotCommand(command="ping", description="Проверить связь"),
    BotCommand(command="id", description="Показать ваш ID и ID чата"),
    BotCommand(command="version", description="Версия шаблона"),
    BotCommand(command="uptime", description="Аптайм процесса"),
    BotCommand(command="feedback", description="Отправить обратную связь"),
    BotCommand(command="cancel", description="Отменить текущее действие"),
    BotCommand(command="stats", description="Статистика (для админов)"),
    BotCommand(command="broadcast", description="Рассылка (для админов)"),
]


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(BOT_COMMANDS, scope=BotCommandScopeDefault())


async def on_error(event: ErrorEvent) -> bool:
    logger.exception("Unhandled error: %s", event.exception, exc_info=event.exception)
    update = event.update
    if update and update.message:
        try:
            await update.message.answer(
                "Произошла ошибка при обработке запроса. Попробуйте позже или /help."
            )
        except Exception:
            logger.debug("Failed to send error fallback message", exc_info=True)
    return True


def create_dispatcher(settings, db: Database) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.workflow_data.update(settings=settings, db=db)
    dp.message.outer_middleware(ThrottlingMiddleware(settings.throttle_seconds))
    dp.message.outer_middleware(MessageStatsMiddleware())
    dp.message.outer_middleware(UserTrackingMiddleware())
    dp.callback_query.outer_middleware(CallbackStatsMiddleware())
    dp.errors.register(on_error)
    for router in get_routers():
        dp.include_router(router)
    return dp


async def _on_startup(bot: Bot, settings, db: Database) -> None:
    await db.connect()
    logger.info("Database ready: %s", settings.db_path)
    await setup_bot_commands(bot)
    logger.info("Bot commands registered; admins=%s", len(settings.admin_ids))
    if settings.run_mode == "webhook" and settings.webhook_base_url:
        url = settings.webhook_base_url + settings.webhook_path
        await bot.set_webhook(
            url,
            secret_token=settings.webhook_secret or None,
            drop_pending_updates=False,
        )
        logger.info("Webhook set: %s", url)


async def _on_shutdown(bot: Bot) -> None:
    logger.info("Shutting down bot...")
    await bot.session.close()


def run_webhook(bot: Bot, dp: Dispatcher, settings) -> None:
    if not settings.webhook_base_url:
        raise RuntimeError("WEBHOOK_BASE_URL обязателен при RUN_MODE=webhook")
    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.webhook_secret or None
    ).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)
    logger.info(
        "Bot starting (webhook) on %s:%s%s",
        settings.app_host,
        settings.app_port,
        settings.webhook_path,
    )
    web.run_app(app, host=settings.app_host, port=settings.app_port)


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    db = Database(settings.db_path)
    bot = Bot(token=settings.bot_token)
    dp = create_dispatcher(settings, db)

    async def on_startup(bot: Bot) -> None:
        await _on_startup(bot, settings, db)

    dp.startup.register(on_startup)
    dp.shutdown.register(_on_shutdown)

    if settings.run_mode == "webhook":
        run_webhook(bot, dp, settings)
    else:
        logger.info("Bot starting (polling)...")
        asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
