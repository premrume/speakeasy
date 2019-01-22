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

devk:
	@echo Killing all containers, images and volumes in this compose-file
	docker-compose down --rmi all --volumes
	@echo Killing any leftovers ... really killing them!!!
	docker volume prune
	docker rmi $$(docker images -q --filter "dangling=true")

devd:
	@echo Stop and remove the container for ${foo}
	docker-compose rm --force --stop ${foo}

devu:
	@echo Build  and Run in the forground the container for ${foo} 
	docker-compose build ${foo}
	docker-compose up ${foo}

devi:
	@echo Stop and remove the container for ${foo}
	docker-compose rm --force --stop ${foo}
	@echo Build  and Run in the forground the container for ${foo} 
	docker-compose build ${foo}
	docker-compose up ${foo}
