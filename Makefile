.PHONY: *

up:
	docker-compose up --build -d

down:
	docker-compose down

restart: down up

bash:
	docker-compose exec app bash

pyshell:
	docker-compose exec app python

test:
	docker-compose run app pytest -sx

logs:
	docker-compose logs -f app
