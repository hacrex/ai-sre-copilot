install:
	python -m pip install -r apps/api/requirements.txt

test:
	PYTHONPATH=apps/api/src pytest apps/api/tests

run:
	uvicorn apps.api.src.main:app --reload --port 8000

up:
	docker compose up --build

down:
	docker compose down
