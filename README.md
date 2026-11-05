# Telegram Bot Template

Простой шаблон Telegram-бота на Python и [aiogram 3](https://docs.aiogram.dev/).

## Возможности

- `/start` — приветствие и кнопки быстрого меню
- `/help` — справка
- `/about` (или кнопка «🤖 О боте») — информация о шаблоне и ссылка на репозиторий
- Ответ эхом на текстовые сообщения
- Inline-кнопка со ссылкой на GitHub в разделе «О боте»
- Регистрация команд бота в меню Telegram при старте
- Загрузка токена из `.env` и базовая обработка ошибок
- Логирование работы бота

## Требования

- Python 3.10+
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

## Быстрый старт

1. Клонируйте репозиторий или скачайте проект.
2. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # Windows (cmd) / macOS / Linux
   # source .venv/bin/activate  (macOS/Linux)
   # .venv\Scripts\activate.bat (cmd)

   pip install -r requirements.txt
   ```

3. Создайте файл `.env` на основе `.env.example` и укажите токен:

   ```env
   BOT_TOKEN=ваш_токен_от_BotFather
   ```

4. Запустите бота:

   ```bash
   python bot.py
   ```

## Структура проекта

```text
.
├── bot.py              # Точка входа: логирование, диспетчер, polling
├── config.py           # Загрузка настроек из окружения
├── handlers/
│   ├── __init__.py     # Регистрация роутеров
│   ├── common.py       # Команды /start и /help
│   └── echo.py         # Эхо-ответ на текст
├── requirements.txt    # Зависимости Python
├── .env.example        # Пример переменных окружения
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── LICENSE
└── README.md
```

## Запуск в Docker

1. Создайте `.env` на основе `.env.example` и укажите `BOT_TOKEN`.
2. Запустите:

   ```bash
   docker compose up --build
   ```

## Автор

- [Zver1o7](https://github.com/Zver1o7)

## Лицензия

Проект распространяется по лицензии MIT. См. файл [LICENSE](LICENSE).
