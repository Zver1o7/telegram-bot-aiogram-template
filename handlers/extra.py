from __future__ import annotations

import asyncio
import time

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message

from config import APP_VERSION, Settings
from runtime import stats
from storage.db import Database

router = Router(name="extra")

_last_broadcast_at: dict[int, float] = {}
BROADCAST_COOLDOWN_SECONDS = 60


def _format_uptime(seconds: int) -> str:
    hours, rem = divmod(max(0, seconds), 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


@router.message(Command("ping"))
async def cmd_ping(message: Message) -> None:
    started = time.perf_counter()
    sent = await message.answer("Pong! Измеряю задержку...")
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    await sent.edit_text(f"Pong! Ответ за ~{elapsed_ms} мс.")


@router.callback_query(F.data == "ping:check")
async def cb_ping(callback: CallbackQuery) -> None:
    await callback.answer("Бот на связи ✅", show_alert=False)


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    user = message.from_user
    user_id = user.id if user else "unknown"
    chat_id = message.chat.id
    await message.answer(f"Ваш user ID: {user_id}\nID чата: {chat_id}")


@router.message(Command("version"))
async def cmd_version(message: Message) -> None:
    await message.answer(f"Версия шаблона: {APP_VERSION}\nАвтор: Zver1o7")


@router.message(Command("uptime"))
async def cmd_uptime(message: Message) -> None:
    await message.answer(f"Аптайм (текущий процесс): {_format_uptime(stats.uptime_seconds())}")


@router.message(Command("stats"))
async def cmd_stats(message: Message, settings: Settings, db: Database) -> None:
    user = message.from_user
    if not user or user.id not in settings.admin_ids:
        await message.answer("Команда /stats доступна только администраторам.")
        return

    db_counts = await db.counts()
    await message.answer(
        "Статистика бота:\n"
        f"• Версия: {APP_VERSION}\n"
        f"• Аптайм (текущий процесс): {_format_uptime(stats.uptime_seconds())}\n"
        f"• Сообщений обработано: {stats.messages_seen}\n"
        f"• Callback-событий: {stats.callbacks_seen}\n"
        f"• Пользователей в БД: {db_counts['users']}\n"
        f"• Отзывов в БД: {db_counts['feedback']}"
    )


@router.message(Command("broadcast"))
async def cmd_broadcast(
    message: Message, command: CommandObject, settings: Settings, db: Database, bot: Bot
) -> None:
    user = message.from_user
    if not user or user.id not in settings.admin_ids:
        await message.answer("Команда /broadcast доступна только администраторам.")
        return

    text = (command.args or "").strip()
    if not text:
        await message.answer(
            "Использование: /broadcast <текст сообщения>\n"
            "Рассылка отправляется пользователям, известным боту (из БД)."
        )
        return

    now = time.monotonic()
    last = _last_broadcast_at.get(user.id, 0.0)
    wait = BROADCAST_COOLDOWN_SECONDS - (now - last)
    if wait > 0:
        await message.answer(f"Подождите {int(wait)} сек. перед следующей рассылкой.")
        return
    _last_broadcast_at[user.id] = now

    user_ids = await db.get_user_ids(limit=500)
    if not user_ids:
        await message.answer("В БД нет пользователей для рассылки.")
        return

    await message.answer(f"Запускаю рассылку для {len(user_ids)} пользователей...")
    delivered = 0
    failed = 0
    for uid in user_ids:
        try:
            await bot.send_message(uid, text)
            delivered += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await message.answer(f"Рассылка завершена. Доставлено: {delivered}, ошибок: {failed}.")
