# Contributing

Спасибо за интерес к проекту!

## Быстрый старт для разработки
1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   pip install -r requirements.txt
   pip install ruff
   ```
2. Скопируйте `.env.example` в `.env` и укажите `BOT_TOKEN`.
3. Запустите бота: `python bot.py` (или `make run`).

## Проверки перед PR
- Линт: `ruff check .` (или `make lint`)
- Тесты: `python -m unittest discover -s tests -v` (или `make test`)
- Компиляция: `python -m compileall -q .`

## Правила
- Не коммитьте `.env`, токены, локальные базы данных (`data/`, `*.db`).
- Сохраняйте шаблон простым и понятным; большие фичи лучше делать опциональными.
- Обновляйте `README.md` и `.env.example`, если меняется поведение/конфигурация.
