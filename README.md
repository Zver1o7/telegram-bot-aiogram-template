# Telegram Bot Template

Расширенный шаблон Telegram-бота на Python и [aiogram 3](https://docs.aiogram.dev/).  
Автор: [Zver1o7](https://github.com/Zver1o7)

Репозиторий: [telegram-bot-aiogram-template](https://github.com/Zver1o7/telegram-bot-aiogram-template)

## Возможности

- Команды: `/start`, `/help`, `/about`, `/ping`, `/id`, `/feedback`, `/cancel`, `/stats` (для админов)
- Кнопки быстрого меню (reply keyboard) и inline-кнопки (callback + ссылка на GitHub)
- **FSM-сценарий**: `/feedback` собирает отзыв и сохраняет его в SQLite
- **SQLite** (`aiosqlite`): учёт пользователей, сохранение отзывов, счётчики для `/stats`
- Эхо-ответ на обычные текстовые сообщения
- Регистрация команд в меню Telegram при старте
- Конфигурация через `.env` (`BOT_TOKEN`, `LOG_LEVEL`, `ADMIN_IDS`, `DB_PATH`)
- Статистика: аптайм текущего процесса + счётчики в памяти + данные из БД
- Глобальная обработка ошибок с логированием и пользовательским fallback-сообщением
- Docker / Docker Compose (с volume для данных)
- `pyproject.toml` (метаданные, зависимости, Ruff)

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
   DB_PATH=data/bot.db
   ```

   `ADMIN_IDS` — необязательно: укажите свой Telegram user ID (узнать: `/id`), чтобы использовать `/stats` и получать уведомления об отзывах.

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
| `/ping` | Проверка ответа/задержки |
| `/id` | Показать ваш user ID и ID чата |
| `/feedback` | Отправить отзыв (сохраняется в SQLite) |
| `/cancel` | Отменить текущее действие (например, ввод отзыва) |
| `/stats` | Статистика (только для `ADMIN_IDS`) |

## Переменные окружения

| Переменная | Обязательно | Описание |
|---|---:|---|
| `BOT_TOKEN` | да | Токен бота от @BotFather |
| `LOG_LEVEL` | нет | `DEBUG`, `INFO`, `WARNING`, `ERROR` (по умолчанию `INFO`) |
| `ADMIN_IDS` | нет | ID администраторов через запятую |
| `DB_PATH` | нет | Путь к SQLite-файлу (по умолчанию `data/bot.db`) |

## Структура проекта

```text
.
├── bot.py              # Точка входа: БД, FSM storage, middleware, polling
├── config.py           # Загрузка и валидация настроек из .env
├── runtime.py          # Счётчики в памяти (аптайм/события)
├── storage/
│   ├── __init__.py
│   └── db.py           # SQLite (aiosqlite): пользователи, отзывы
├── handlers/
│   ├── __init__.py     # Подключение роутеров
│   ├── common.py       # /start, /help, /about, кнопки
│   ├── extra.py        # /ping, /id, /stats, callback
│   ├── feedback.py     # /feedback, /cancel, FSM
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

1. Создайте `.env` на основе `.env.example` и укажите `BOT_TOKEN` (и при необходимости `ADMIN_IDS`, `LOG_LEVEL`, `DB_PATH`).
2. Запустите:

   ```bash
   docker compose up --build
   ```

В `docker-compose.yml` каталог `./data` монтируется в `/app/data`, чтобы файл SQLite сохранялся между перезапусками.

## Примечания

- Счётчики сообщений/callback и аптайм в `/stats` считаются **для текущего процесса**; пользователи и отзывы хранятся в **SQLite**.
- Не коммитьте `.env` и локальные файлы БД (`data/`, `*.db` уже в `.gitignore`).
- Для продакшена можно заменить polling на webhook, добавить миграции БД и более строгую модель прав/администрирования.

## Автор

- [Zver1o7](https://github.com/Zver1o7)

## Лицензия

Проект распространяется по лицензии MIT. См. файл [LICENSE](LICENSE).
