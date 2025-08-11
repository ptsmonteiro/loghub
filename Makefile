SHELL := /bin/bash

.PHONY: up down logs web shell test

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

web:
	docker compose up -d --build db web

shell:
	docker compose run --rm web bash

test:
	docker compose run --rm test

