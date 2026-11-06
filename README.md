# Telegram Bot Template

Расширенный (мега) шаблон Telegram-бота на Python и [aiogram 3](https://docs.aiogram.dev/).  
Автор: [Zver1o7](https://github.com/Zver1o7) · Репозиторий: [telegram-bot-aiogram-template](https://github.com/Zver1o7/telegram-bot-aiogram-template)

> План и статус большого обновления (100 пунктов): [`docs/MEGA_UPDATE_100.md`](docs/MEGA_UPDATE_100.md)

## Возможности

- **Команды**: `/start`, `/help`, `/about`, `/ping`, `/id`, `/version`, `/uptime`, `/feedback`, `/cancel`, `/stats` (админы), `/broadcast <текст>` (админы)
- **UX**: reply-меню, inline-кнопки (callback + ссылка), команды в меню Telegram
- **FSM**: сценарий обратной связи `/feedback` с отменой
- **SQLite (`aiosqlite`)**: пользователи, отзывы, индексы, счётчики; трекинг пользователей
- **Надёжность**: глобальная обработка ошибок, fallback-сообщение пользователю, анти-флуд (throttling middleware)
- **Конфиг**: `.env` (`BOT_TOKEN`, `LOG_LEVEL`, `ADMIN_IDS`, `DB_PATH`, режим polling/webhook и др.)
- **Режимы запуска**: polling (по умолчанию) или webhook (`aiohttp`)
- **Dev/качество**: `pyproject.toml` (Ruff), базовые `unittest`-тесты, `Makefile`, CI workflow
- **Документы**: `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, мега-план

## Требования

- Python 3.10+
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)

## Быстрый старт (polling)

1. Установите зависимости:
   ```bash
   python -m venv .venv
   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Создайте `.env` на основе `.env.example` и задайте `BOT_TOKEN` (опционально `ADMIN_IDS`, `LOG_LEVEL`, `DB_PATH`).
3. Запустите:
   ```bash
   python bot.py
   # или: make run
   ```

## Webhook (опционально)

Установите в `.env`:
```env
RUN_MODE=webhook
WEBHOOK_BASE_URL=https://your-domain.example
WEBHOOK_PATH=/webhook
WEBHOOK_SECRET=long-random-secret
APP_HOST=0.0.0.0
APP_PORT=8080
```
Требуется публичный HTTPS-URL, который принимает запросы Telegram. Для локальной разработки обычно удобнее `RUN_MODE=polling`.

## Команды

| Команда | Описание |
|---|---|
| `/start` | Приветствие и меню |
| `/help` | Справка |
| `/about` | О шаблоне и ссылка на репозиторий |
| `/ping` | Проверка ответа/задержки |
| `/id` | Ваш user ID и ID чата |
| `/version` | Версия шаблона |
| `/uptime` | Аптайм процесса |
| `/feedback` | Отправить отзыв (FSM, сохраняется в SQLite) |
| `/cancel` | Отменить текущее действие |
| `/stats` | Статистика (только `ADMIN_IDS`) |
| `/broadcast <текст>` | Рассылка известным пользователям из БД (только `ADMIN_IDS`, с cooldown/лимитами) |

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `BOT_TOKEN` | — | **Обязательно.** Токен от @BotFather |
| `LOG_LEVEL` | `INFO` | Уровень логирования |
| `ADMIN_IDS` | пусто | ID админов через запятую |
| `DB_PATH` | `data/bot.db` | Путь к SQLite |
| `RUN_MODE` | `polling` | `polling` или `webhook` |
| `WEBHOOK_BASE_URL` | пусто | Базовый URL для webhook |
| `WEBHOOK_PATH` | `/webhook` | Путь webhook |
| `WEBHOOK_SECRET` | пусто | Секрет webhook (рекомендуется) |
| `APP_HOST` | `0.0.0.0` | Хост HTTP-сервера (webhook) |
| `APP_PORT` | `8080` | Порт HTTP-сервера (webhook) |
| `THROTTLE_SECONDS` | `0.7` | Анти-флуд интервал (`0` — выкл) |

## Структура проекта

```text
.
├── bot.py                # Точка входа: lifecycle, polling/webhook
├── config.py             # Настройки/env
├── runtime.py            # In-memory счётчики
├── handlers/             # Роутеры: common, extra, feedback, echo
├── middlewares/          # Throttling и др.
├── storage/db.py         # SQLite (aiosqlite)
├── tests/                # Базовые тесты
├── docs/MEGA_UPDATE_100.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```

## Docker

```bash
docker compose up --build
```
Каталог `./data` монтируется в `/app/data` для сохранения SQLite.

## Разработка

```bash
make lint   # ruff check .
make test   # unittest
```

## Примечания

- In-memory счётчики/аптайм процесса сбрасываются при рестарте; пользователи и отзывы — в SQLite.
- Не коммитьте `.env` и локальные БД (`data/`, `*.db`).
- `/broadcast` — мощная команда: используйте только доверенным `ADMIN_IDS`.

## Автор

- [Zver1o7](https://github.com/Zver1o7)

## Лицензия

MIT — см. [LICENSE](LICENSE).
