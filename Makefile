# ═══════════════════════════════════════════════════════════════
# POE Agentified STR System — Makefile
# ═══════════════════════════════════════════════════════════════

.PHONY: help up down build restart logs ps shell clean test lint format db-migrate db-seed db-shell backend-up frontend-up agent-up mocks-up

# ──────────────────────────────────────────────
# Default target
# ──────────────────────────────────────────────
help:
	@echo "POE Agentified STR System — Available Commands"
	@echo ""
	@echo "  Core:"
	@echo "    make up           Start all services (detached)"
	@echo "    make down         Stop all services"
	@echo "    make build        Build all images"
	@echo "    make restart      Restart all services"
	@echo "    make logs         Follow logs (all services)"
	@echo "    make ps           Show running containers"
	@echo ""
	@echo "  Shells:"
	@echo "    make shell-backend       Backend container shell"
	@echo "    make shell-frontend      Frontend container shell"
	@echo "    make shell-agent         Agent runtime shell"
	@echo "    make shell-db            PostgreSQL psql shell"
	@echo "    make shell-redis         Redis CLI"
	@echo "    make shell-nats          NATS CLI"
	@echo ""
	@echo "  Database:"
	@echo "    make db-migrate   Run Alembic migrations"
	@echo "    make db-revision  Create new migration"
	@echo "    make db-seed      Seed development data"
	@echo "    make db-reset     Drop and recreate database"
	@echo ""
	@echo "  Development:"
	@echo "    make backend-up   Start only backend + deps"
	@echo "    make frontend-up  Start only frontend + deps"
	@echo "    make agent-up     Start only agent runtime + deps"
	@echo "    make mocks-up     Start PMS mock servers"
	@echo ""
	@echo "  Testing:"
	@echo "    make test         Run all tests"
	@echo "    make test-unit    Unit tests only"
	@echo "    make test-integration  Integration tests"
	@echo "    make test-e2e     End-to-end tests"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make lint         Run all linters"
	@echo "    make format       Format code (black, prettier)"
	@echo "    make typecheck    Type checking (mypy, tsc)"
	@echo ""
	@echo "  Cleanup:"
	@echo "    make clean        Remove containers, volumes, images"
	@echo "    make clean-all    Nuclear clean (including node_modules)"
	@echo ""
	@echo "  Profiles:"
	@echo "    make up-prod      Start with production profile"

# ──────────────────────────────────────────────
# Docker Compose Base Command
# ──────────────────────────────────────────────
DC := docker compose -f docker-compose.yml
DC_MOCKS := docker compose -f docker-compose.yml --profile mocks

# ──────────────────────────────────────────────
# Core Lifecycle
# ──────────────────────────────────────────────
up:
	$(DC) up -d --remove-orphans

down:
	$(DC) down --remove-orphans

build:
	$(DC) build --parallel

restart:
	$(DC) restart

logs:
	$(DC) logs -f --tail=100

logs-backend:
	$(DC) logs -f --tail=100 backend

logs-frontend:
	$(DC) logs -f --tail=100 frontend

logs-agent:
	$(DC) logs -f --tail=100 agent-runtime

logs-db:
	$(DC) logs -f --tail=100 postgres

ps:
	$(DC) ps

# ──────────────────────────────────────────────
# Shells
# ──────────────────────────────────────────────
shell-backend:
	$(DC) exec backend bash

shell-frontend:
	$(DC) exec frontend bash

shell-agent:
	$(DC) exec agent-runtime bash

shell-db:
	$(DC) exec postgres psql -U $${POSTGRES_USER:-poe} -d $${POSTGRES_DB:-poe_str}

shell-redis:
	$(DC) exec redis redis-cli

shell-nats:
	$(DC) exec nats nats --server localhost:4222

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────
db-migrate:
	$(DC) exec backend alembic upgrade head

db-revision:
	@read -p "Migration message: " msg; \
	$(DC) exec backend alembic revision --autogenerate -m "$$msg"

db-seed:
	$(DC) exec backend python -m app.db.seed

db-reset:
	$(DC) exec postgres psql -U $${POSTGRES_USER:-poe} -c "DROP DATABASE IF EXISTS $${POSTGRES_DB:-poe_str}; CREATE DATABASE $${POSTGRES_DB:-poe_str};"
	$(MAKE) db-migrate
	$(MAKE) db-seed

# ──────────────────────────────────────────────
# Development Profiles
# ──────────────────────────────────────────────
backend-up:
	$(DC) up -d postgres nats redis backend

frontend-up:
	$(DC) up -d postgres nats redis backend frontend

agent-up:
	$(DC) up -d postgres nats redis agent-runtime

mocks-up:
	$(DC_MOCKS) up -d ownerrez-mock hospitable-mock

# ──────────────────────────────────────────────
# Testing
# ──────────────────────────────────────────────
test: test-unit test-integration

test-unit:
	$(DC) exec backend pytest tests/unit -v --tb=short
	$(DC) exec frontend npm run test:unit

test-integration:
	$(DC) exec backend pytest tests/integration -v --tb=short

test-e2e:
	$(DC) exec frontend npm run test:e2e

test-coverage:
	$(DC) exec backend pytest tests/unit --cov=app --cov-report=term-missing
	$(DC) exec frontend npm run test:coverage

# ──────────────────────────────────────────────
# Code Quality
# ──────────────────────────────────────────────
lint: lint-backend lint-frontend

lint-backend:
	$(DC) exec backend ruff check app tests
	$(DC) exec backend mypy app

lint-frontend:
	$(DC) exec frontend npm run lint

format: format-backend format-frontend

format-backend:
	$(DC) exec backend ruff format app tests
	$(DC) exec backend ruff check --fix app tests

format-frontend:
	$(DC) exec frontend npm run format

typecheck: typecheck-backend typecheck-frontend

typecheck-backend:
	$(DC) exec backend mypy app

typecheck-frontend:
	$(DC) exec frontend npm run typecheck

# ──────────────────────────────────────────────
# Cleanup
# ──────────────────────────────────────────────
clean:
	$(DC) down -v --remove-orphans --rmi local

clean-all: clean
	rm -rf 07_CODE/frontend/node_modules 07_CODE/frontend/.next
	rm -rf 07_CODE/backend/.pytest_cache 07_CODE/backend/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

# ──────────────────────────────────────────────
# Production
# ──────────────────────────────────────────────
up-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────
install-deps:
	$(DC) exec backend pip install -e ".[dev]"
	$(DC) exec frontend npm install

generate-openapi:
	$(DC) exec backend python -c "from app.main import app; import json; print(json.dumps(app.openapi(), indent=2))" > docs/api/openapi.json

prune:
	docker system prune -f --volumes