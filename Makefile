# Executables (local)
DOCKER_COMP = docker-compose

# Docker containers
PHP_CONT = $(DOCKER_COMP) exec webserver
DB_CONT = $(DOCKER_COMP) exec mysql
NPM_CONT = $(DOCKER_COMP) exec node

## —— Docker 🐳 ————————————————————————————————————————————————————————————————
build:  ## Builds the Docker images
	@$(DOCKER_COMP) build --pull --no-cache

up:  ## Start the docker hub in detached mode (no logs)
	@$(DOCKER_COMP) up --detach

down:  ## Stop the docker hub
	@$(DOCKER_COMP) down --remove-orphans

sh:  ## Connect to the PHP FPM container
	@$(PHP_CONT) bash

pull:  ## Build project after pull
	@$(PHP_CONT) sh -c "\
			composer install; \
			php bin/console d:s:u --dump-sql --force --complete; \
	"

dsu:  ## Build project after pull
	@$(PHP_CONT) sh -c "\
			php bin/console d:s:u --dump-sql --force --complete; \
		"

clear-cache:
	@$(PHP_CONT) sh -c "\
			APP_ENV=prod php bin/console cache:clear; \
			php bin/console cache:pool:clear cache.global_clearer; \
		"
	sudo chmod 777 -R var/*

build-npm:
	@$(NPM_CONT) sh -c "\
			yarn build \
		"

import-data:  ## Import data to db
	sudo docker-compose exec -T mysql mysql spadajace_kwadraciki -u root -p12345678 < public/squares-backup.sql

export-data:  ## Export data from db
	sudo $(DB_CONT) mysqldump spadajace_kwadraciki -u root -p12345678 > public/squares-backup.sql

update:
	git pull
	$(MAKE) pull
	$(MAKE) clear-cache
	$(MAKE) build-npm

