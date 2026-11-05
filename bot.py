import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я Telegram-бот шаблон.\n\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — справка\n\n"
        "Отправь мне любой текст — я отвечу эхо-сообщением."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Справка:\n"
        "• /start — начать работу\n"
        "• /help — показать эту справку\n"
        "• Любой текст — бот вернёт его в ответ"
    )


@dp.message(F.text)
async def echo_text(message: Message) -> None:
    await message.answer(f"Вы написали: {message.text}")


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN не задан. Создайте файл .env на основе .env.example и укажите токен."
        )

    bot = Bot(token=token)
    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
