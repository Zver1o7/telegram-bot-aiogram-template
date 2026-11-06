.PHONY: install run lint format test docker-build docker-up docker-down

install:
	pip install -r requirements.txt

run:
	python bot.py

lint:
	ruff check .

format:
	ruff check . --fix

test:
	python -m unittest discover -s tests -p "test_*.py" -v

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down
