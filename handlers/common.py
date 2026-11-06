from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

router = Router(name="common")

REPO_URL = "https://github.com/Zver1o7/telegram-bot-aiogram-template"

HELP_TEXT = (
    "Справка:\n"
    "• /start — начать работу и показать меню\n"
    "• /help — показать эту справку\n"
    "• /about — информация о шаблоне\n"
    "• /ping — проверить задержку/связь\n"
    "• /id — показать ваш ID и ID чата\n"
    "• /version — версия шаблона\n"
    "• /uptime — аптайм процесса\n"
    "• /feedback — отправить отзыв (FSM-сценарий)\n"
    "• /cancel — отменить текущее действие\n"
    "• /stats — статистика (только для админов)\n"
    "• /broadcast <текст> — рассылка (только для админов)\n"
    "• Любой другой текст — бот вернёт его в ответ"
)

ABOUT_TEXT = (
    "🤖 Telegram Bot Template\n\n"
    "Мега-шаблон на Python + aiogram 3.\n"
    "Возможности: команды, reply/inline-кнопки, callback, FSM (/feedback), "
    "SQLite, анти-флуд, polling/webhook, админ-инструменты, Docker.\n\n"
    "Автор: Zver1o7 (https://github.com/Zver1o7)"
)

ABOUT_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Проверить связь", callback_data="ping:check")],
        [InlineKeyboardButton(text="Открыть репозиторий на GitHub", url=REPO_URL)],
    ]
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🤖 О боте")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Напишите сообщение или выберите действие",
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я Telegram-бот шаблон.\n\n"
        "Используйте команды или кнопки ниже. Любой текст я повторю в ответ.",
        reply_markup=MAIN_KEYBOARD,
    )


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=MAIN_KEYBOARD)


@router.message(Command("about"))
@router.message(F.text == "🤖 О боте")
async def cmd_about(message: Message) -> None:
    await message.answer(ABOUT_TEXT, reply_markup=ABOUT_KEYBOARD)
