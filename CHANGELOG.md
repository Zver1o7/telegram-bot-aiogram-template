# Changelog

## 0.4.0 - Мега-обнова (100-пунктный план, реализован ключевой набор)
- Добавлены `/version`, `/uptime`, `/broadcast` (админ, с ограничениями).
- Добавлен throttling middleware (анти-флуд, `THROTTLE_SECONDS`).
- Расширена конфигурация: `RUN_MODE` polling/webhook, `WEBHOOK_*`, `APP_HOST/PORT`.
- SQLite: индексы и выборка user_id для рассылки.
- Добавлены `Makefile`, базовые `tests/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`.
- Добавлен `docs/MEGA_UPDATE_100.md` (100 пунктов, статус реализации).
- Обновлены README, `.env.example`, структура и зависимости.

## 0.3.0
- SQLite (пользователи/отзывы), FSM `/feedback`, трекинг пользователей, улучшенный `/stats`.

## 0.2.0
- Модульная структура, роутеры, `/ping`, `/id`, callback, Docker, улучшенная обработка ошибок.

## 0.1.0
- Начальный шаблон aiogram 3: `/start`, `/help`, `/about`, эхо, конфиг `.env`.
