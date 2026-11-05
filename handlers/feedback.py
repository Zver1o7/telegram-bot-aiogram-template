from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import Settings
from storage.db import Database

router = Router(name="feedback")
logger = logging.getLogger(__name__)


class FeedbackState(StatesGroup):
    waiting_text = State()


CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel_flow(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("Нечего отменять.", reply_markup=ReplyKeyboardRemove())
        return
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=ReplyKeyboardRemove())


@router.message(Command("feedback"))
async def feedback_start(message: Message, state: FSMContext) -> None:
    await state.set_state(FeedbackState.waiting_text)
    await message.answer(
        "Напишите ваше сообщение для обратной связи одним сообщением.\n"
        "Чтобы отменить, отправьте /cancel или нажмите «Отмена».",
        reply_markup=CANCEL_KB,
    )


@router.message(FeedbackState.waiting_text, F.text)
async def feedback_save(
    message: Message, state: FSMContext, db: Database, settings: Settings, bot: Bot
) -> None:
    text = (message.text or "").strip()
    if text.casefold() == "отмена":
        await cancel_flow(message, state)
        return
    if not text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение или /cancel.")
        return

    user = message.from_user
    user_id = user.id if user else 0
    username = user.username if user else None
    feedback_id = await db.save_feedback(user_id, username, text)
    await state.clear()
    await message.answer(
        f"Спасибо! Сообщение #{feedback_id} сохранено.", reply_markup=ReplyKeyboardRemove()
    )

    if settings.admin_ids and user_id not in settings.admin_ids:
        preview = text if len(text) <= 1000 else text[:1000] + "…"
        admin_text = (
            f"Новое feedback #{feedback_id}\n"
            f"От: {user_id} (@{username})\n\n{preview}"
        )
        for admin_id in settings.admin_ids:
            try:
                await bot.send_message(admin_id, admin_text)
            except Exception:
                logger.warning("Failed to notify admin %s about feedback", admin_id, exc_info=True)
