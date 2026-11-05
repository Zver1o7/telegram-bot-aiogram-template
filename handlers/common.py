from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

router = Router(name="common")

HELP_TEXT = (
    "Справка:\n"
    "• /start — начать работу и показать меню\n"
    "• /help — показать эту справку\n"
    "• /about — информация о шаблоне\n"
    "• Любой другой текст — бот вернёт его в ответ"
)

ABOUT_TEXT = (
    "🤖 Telegram Bot Template\n\n"
    "Шаблон на Python + aiogram 3.\n"
    "Возможности: команды, меню-кнопки, эхо, конфиг через .env, Docker.\n"
    "Исходный код и настройка — в README проекта."
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
    await message.answer(ABOUT_TEXT, reply_markup=MAIN_KEYBOARD)
