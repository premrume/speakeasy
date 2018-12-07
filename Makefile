all:
	docker-compose build install
	docker-compose up --force-recreate install
	docker-compose build
	docker-compose up -d
	docker-compose ps

clean:
	docker stop $$(docker ps -aq) || true
	docker rm $$(docker ps -aq) || true

mrproper:
	docker volume rm $$(docker volume ls -q | grep speakeasy)

