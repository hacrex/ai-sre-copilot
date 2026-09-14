.PHONY: install install-dev test lint typecheck fmt run up down clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest --cov=src --cov-report=term-missing

lint:
	ruff check apps/api/src apps/api/tests

fmt:
	ruff format apps/api/src apps/api/tests

typecheck:
	mypy apps/api/src

check: lint typecheck test

run:
	uvicorn src.main:app --reload --port 8000

up:
	docker compose up --build

down:
	docker compose down

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
