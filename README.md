# Telegram Bot Template

Простой шаблон Telegram-бота на Python и [aiogram 3](https://docs.aiogram.dev/).

## Возможности

- `/start` — приветствие и список команд
- `/help` — справка
- Ответ эхом на текстовые сообщения
- Загрузка токена из `.env`
- Базовое логирование

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
├── bot.py            # Точка входа и обработчики
├── requirements.txt  # Зависимости Python
├── .env.example      # Пример переменных окружения
├── .gitignore
├── LICENSE
└── README.md
```

## Публикация в GitHub

GitHub CLI (`gh`) не обязателен. Можно опубликовать так:

1. Создайте пустой репозиторий на GitHub (без README/License, если они уже есть локально).
2. Добавьте remote и отправьте изменения:

   ```bash
   git remote add origin https://github.com/<username>/<repo>.git
   git branch -M main
   git push -u origin main
   ```

> Не коммитьте файл `.env` — в нём хранится секретный токен.

## Лицензия

Проект распространяется по лицензии MIT. См. файл [LICENSE](LICENSE).
