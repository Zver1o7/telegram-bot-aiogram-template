# Telegram Bot Template

Расширенный шаблон Telegram-бота на Python и [aiogram 3](https://docs.aiogram.dev/).  
Автор: [Zver1o7](https://github.com/Zver1o7)

Репозиторий: [telegram-bot-aiogram-template](https://github.com/Zver1o7/telegram-bot-aiogram-template)

## Возможности

- Команды: `/start`, `/help`, `/about`, `/ping`, `/id`, `/stats` (для админов)
- Кнопки быстрого меню (reply keyboard) и inline-кнопки (callback + ссылка на GitHub)
- Эхо-ответ на обычные текстовые сообщения
- Регистрация команд в меню Telegram при старте
- Конфигурация через `.env` (`BOT_TOKEN`, `LOG_LEVEL`, `ADMIN_IDS`)
- Базовая статистика в памяти (аптайм, счётчики сообщений/callback) и команда `/stats`
- Глобальная обработка ошибок с логированием и пользовательским fallback-сообщением
- Готовность к запуску в Docker / Docker Compose
- Базовая конфигурация проекта в `pyproject.toml` (в т.ч. Ruff)

## Требования

- Python 3.10+
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

## Быстрый старт

1. Склонируйте репозиторий и перейдите в папку проекта.
2. Создайте виртуальное окружение и установите зависимости:

   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   # source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. Создайте `.env` на основе `.env.example`:

   ```env
   BOT_TOKEN=ваш_токен_от_BotFather
   LOG_LEVEL=INFO
   ADMIN_IDS=123456789
   ```

   `ADMIN_IDS` — необязательно: укажите свой Telegram user ID (можно узнать командой `/id`), чтобы использовать `/stats`.

4. Запустите бота:

   ```bash
   python bot.py
   ```

## Команды

| Команда | Описание |
|---|---|
| `/start` | Приветствие и меню |
| `/help` | Справка |
| `/about` | О шаблоне и ссылка на репозиторий |
| `/ping` | Проверка ответа бота |
| `/id` | Показать ваш user ID и ID чата |
| `/stats` | Статистика с момента запуска (только для `ADMIN_IDS`) |

## Переменные окружения

| Переменная | Обязательно | Описание |
|---|---:|---|
| `BOT_TOKEN` | да | Токен бота от @BotFather |
| `LOG_LEVEL` | нет | `DEBUG`, `INFO`, `WARNING`, `ERROR` (по умолчанию `INFO`) |
| `ADMIN_IDS` | нет | ID администраторов через запятую |

## Структура проекта

```text
.
├── bot.py              # Точка входа: настройки, middleware, polling
├── config.py           # Загрузка и валидация настроек из .env
├── runtime.py          # Простая статистика в памяти
├── handlers/
│   ├── __init__.py     # Подключение роутеров
│   ├── common.py       # /start, /help, /about, кнопки
│   ├── extra.py        # /ping, /id, /stats, callback-обработчики
│   └── echo.py         # Эхо-ответ на текст
├── pyproject.toml      # Метаданные проекта и конфигурация Ruff
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

1. Создайте `.env` на основе `.env.example` и укажите `BOT_TOKEN` (и при необходимости `ADMIN_IDS`, `LOG_LEVEL`).
2. Запустите:

   ```bash
   docker compose up --build
   ```

## Примечания

- Статистика `/stats` хранится **в памяти** и сбрасывается при перезапуске бота.
- Не коммитьте `.env` — в нём находятся секреты.
- Для продакшена можно заменить polling на webhook и подключить постоянное хранилище (БД) для состояния/статистики.

## Автор

- [Zver1o7](https://github.com/Zver1o7)

## Лицензия

Проект распространяется по лицензии MIT. См. файл [LICENSE](LICENSE).
