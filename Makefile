.PHONY: build up down logs migrate shell

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

