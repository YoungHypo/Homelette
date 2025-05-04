# Makefile for Homelette Backend

# define variables
DOCKER_COMPOSE = docker compose
message = "Initial migration"

.PHONY: help
help:
	@echo "Homelette Backend Makefile Guide"
	@echo "--------------------------------"
	@echo "Available commands:"
	@echo "  make build       - Build all Docker images"
	@echo "  make start       - Start all services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make clean       - Clean Docker resources (use with caution)"
	@echo "  make migrate     - Execute database migrations"
	@echo "  make migrate-init - Initialize database migrations"
	@echo "  make migrate-create - Create database migration script"
	@echo "  make migrate-apply - Apply database migration"
	@echo "  make test        - Run tests"

# build docker image
.PHONY: build
build:
	@echo "Build all Docker images..."
	$(DOCKER_COMPOSE) build

# start services
.PHONY: start
start:
	@echo "Start all services..."
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

# initialize database migrations (use API service for this)
.PHONY: migrate-init
migrate-init:
	@echo "Initialize database migrations..."
	$(DOCKER_COMPOSE) exec flask-api flask db init

# create migration script (use API service for this)
.PHONY: migrate-create
migrate-create:
	@echo "Create database migration script..."
	$(DOCKER_COMPOSE) exec flask-api flask db migrate -m "$(message)"

# apply migration (use API service for this)
.PHONY: migrate-apply
migrate-apply:
	@echo "Apply database migration..."
	$(DOCKER_COMPOSE) exec flask-api flask db upgrade

# full migration process (create and apply)
.PHONY: migrate
migrate:
	@echo "Execute full database migration process..."
	$(DOCKER_COMPOSE) exec flask-api flask db migrate -m "$(message)"
	$(DOCKER_COMPOSE) exec flask-api flask db upgrade

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