from __future__ import annotations

import time

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import Settings
from runtime import stats
from storage.db import Database

router = Router(name="extra")


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


@router.message(Command("stats"))
async def cmd_stats(message: Message, settings: Settings, db: Database) -> None:
    user = message.from_user
    if not user or user.id not in settings.admin_ids:
        await message.answer("Команда /stats доступна только администраторам.")
        return

    uptime = stats.uptime_seconds()
    hours, rem = divmod(uptime, 3600)
    minutes, seconds = divmod(rem, 60)
    db_counts = await db.counts()
    await message.answer(
        "Статистика бота:\n"
        f"• Аптайм (текущий процесс): {hours:02d}:{minutes:02d}:{seconds:02d}\n"
        f"• Сообщений обработано: {stats.messages_seen}\n"
        f"• Callback-событий: {stats.callbacks_seen}\n"
        f"• Пользователей в БД: {db_counts['users']}\n"
        f"• Отзывов в БД: {db_counts['feedback']}"
    )
