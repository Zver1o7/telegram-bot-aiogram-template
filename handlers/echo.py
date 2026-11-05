from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message

router = Router(name="echo")
logger = logging.getLogger(__name__)


@router.message(F.text)
async def echo_text(message: Message) -> None:
    logger.debug("Echoing message from chat_id=%s", message.chat.id)
    await message.answer(f"Вы написали: {message.text}")
