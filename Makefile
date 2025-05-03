# Makefile for Homelette Flask Backend

# define variables
DOCKER_COMPOSE = docker compose -f backend/docker-compose.yml
DOCKER_BUILD = docker build -f backend/Dockerfile
message = "Initial migration"

.PHONY: help
help:
	@echo "Homelette Flask Backend Makefile Guide"
	@echo "--------------------------------"
	@echo "Available commands:"
	@echo "  make build       - Build Flask backend Docker image"
	@echo "  make start       - Start all services (Flask+MariaDB)"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs of all containers"
	@echo "  make flask-logs  - View logs of Flask container only"
	@echo "  make db-logs     - View logs of MariaDB container only"
	@echo "  make flask-shell - Open Flask container shell"
	@echo "  make db-shell    - Open MariaDB container shell"
	@echo "  make clean       - Clean Docker resources (use with caution)"
	@echo "  make migrate     - Execute database migrations"
	@echo "  make test        - Run tests"

# build docker image
.PHONY: build
build:
	@echo "Build backend Docker image..."
	$(DOCKER_COMPOSE) build

# start services
.PHONY: start
start:
	@echo "Start all services (Flask+MariaDB)..."
	$(DOCKER_COMPOSE) up -d

# stop services
.PHONY: stop
stop:
	@echo "Stopping all services..."
	$(DOCKER_COMPOSE) down

# restart services
.PHONY: restart
restart:
	@echo "Restarting all services..."
	$(DOCKER_COMPOSE) restart

# view all logs
.PHONY: logs
logs:
	@echo "View logs of all containers..."
	$(DOCKER_COMPOSE) logs --tail=100 -f

# view Flask logs
.PHONY: flask-logs
flask-logs:
	@echo "View logs of Flask container..."
	$(DOCKER_COMPOSE) logs --tail=100 -f flask

# view MariaDB logs
.PHONY: db-logs
db-logs:
	@echo "View logs of MariaDB container..."
	$(DOCKER_COMPOSE) logs --tail=100 -f mariadb

# enter Flask container shell
.PHONY: flask-shell
flask-shell:
	@echo "Enter Flask container shell..."
	$(DOCKER_COMPOSE) exec flask bash || $(DOCKER_COMPOSE) exec flask sh

# enter MariaDB container shell
.PHONY: db-shell
db-shell:
	@echo "Enter MariaDB container shell..."
	$(DOCKER_COMPOSE) exec mariadb bash

# enter MariaDB database shell
.PHONY: db-client
db-client:
	@echo "Enter MariaDB database shell..."
	$(DOCKER_COMPOSE) exec mariadb mysql -u homelette_user -p123aaa homelette

# initialize database migrations
.PHONY: migrate-init
migrate-init:
	@echo "Initialize database migrations..."
	$(DOCKER_COMPOSE) exec flask flask db init

# create migration script
.PHONY: migrate-create
migrate-create:
	@echo "Create database migration script..."
	$(DOCKER_COMPOSE) exec flask flask db migrate -m "$(message)"

# apply migration
.PHONY: migrate-apply
migrate-apply:
	@echo "Apply database migration..."
	$(DOCKER_COMPOSE) exec flask flask db upgrade

# full migration process (create and apply)
.PHONY: migrate
migrate:
	@echo "Execute full database migration process..."
	$(DOCKER_COMPOSE) exec flask flask db migrate -m "$(message)"
	$(DOCKER_COMPOSE) exec flask flask db upgrade

# run tests
.PHONY: test
test:
	@echo "Run tests..."

# clean docker resources
.PHONY: clean
clean:
	@echo "Warning: This will clean all related Docker resources, including data. This action is irreversible!"
	@read -p "Are you sure to continue? [y/N]: " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "Stopping and removing all services..."; \
		$(DOCKER_COMPOSE) down -v; \
		echo "Cleanup successful"; \
	else \
		echo "Operation cancelled"; \
	fi

# set default target
.DEFAULT_GOAL := help 