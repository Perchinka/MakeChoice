.PHONY: build up down logs migrate shell

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f web

migrate:
	docker-compose run --rm web alembic upgrade head

shell:
	docker-compose run --rm web bash
