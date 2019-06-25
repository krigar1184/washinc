up:
	docker-compose up --build -d

down:
	docker-compose down

restart: down up

bash:
	docker-compose exec app bash

test:
	docker-compose run app pytest -sx
