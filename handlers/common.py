from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я Telegram-бот шаблон.\n\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — справка\n\n"
        "Отправь мне любой текст — я отвечу эхо-сообщением."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Справка:\n"
        "• /start — начать работу\n"
        "• /help — показать эту справку\n"
        "• Любой текст — бот вернёт его в ответ"
    )
