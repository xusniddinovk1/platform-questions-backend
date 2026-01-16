

dev:
	uv run manage.py runserver

docker:
	docker rm platform-questions-backend || true
	docker run -d -p 8000:8000 platform-questions-backend

pre-prod:
	docker-compose -f docker/docker-compose.yaml build
	docker-compose -f docker/docker-compose.yaml up

stop:
	docker-compose -f docker/docker-compose.yaml down

lint:
	uv run ruff check --fix

format:
	uv run black .

typecheck:
	uv run mypy .

test:
	uv run pytest .

ci: format lint typecheck test
