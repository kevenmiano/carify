.PHONY: help install run test clean shell docs

# Variáveis
PYTHON = poetry run python
FLASK = poetry run flask
PORT = 3000

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências do projeto
	poetry install

run: ## Inicia o servidor Flask (recomendado)
	$(PYTHON) -m carify.app

run-dev: ## Inicia o servidor Flask em modo desenvolvimento
	$(PYTHON) -m carify.app

run-flask: ## Inicia o servidor usando Flask CLI
	$(FLASK) --app carify.app run --debug --port $(PORT)

run-gunicorn: ## Inicia o servidor com Gunicorn (produção)
	poetry run gunicorn carify.app:app --bind 0.0.0.0:$(PORT) --workers 4

test: ## Executa os testes unitários
	$(PYTHON) -m unittest discover tests -v

test-watch: ## Executa os testes em modo watch (precisa de pytest-watch)
	poetry run ptw tests

test-coverage: ## Executa os testes com cobertura
	poetry run coverage run -m unittest discover tests
	poetry run coverage report
	poetry run coverage html

shell: ## Ativa o ambiente virtual do Poetry
	poetry shell

docs: ## Abre a documentação Scalar no navegador
	@echo "Abrindo documentação Scalar..."
	@echo "Scalar UI: http://localhost:$(PORT)/docs/scalar/"
	@xdg-open http://localhost:$(PORT)/docs/scalar/ 2>/dev/null || open http://localhost:$(PORT)/docs/scalar/ 2>/dev/null || echo "Abra manualmente: http://localhost:$(PORT)/docs/scalar/"

clean: ## Remove arquivos temporários e cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

lint: ## Executa linters (se configurado)
	poetry run ruff check . || true
	poetry run black --check . || true

format: ## Formata o código
	poetry run black . || echo "Black não instalado"
	poetry run isort . || echo "isort não instalado"

update: ## Atualiza as dependências
	poetry update

lock: ## Atualiza o poetry.lock
	poetry lock

add: ## Adiciona uma nova dependência (uso: make add PKG=nome-do-pacote)
	poetry add $(PKG)

add-dev: ## Adiciona uma dependência de desenvolvimento (uso: make add-dev PKG=nome-do-pacote)
	poetry add --group dev $(PKG)

seed: ## Popula o banco com dados fictícios
	$(PYTHON) scripts/seed_data.py

api-test: ## Testa os endpoints da API (requer httpie)
	http GET http://localhost:$(PORT)/health
	http GET http://localhost:$(PORT)/proprietarios

docker-up: ## Inicia todos os serviços Docker (MariaDB, Jaeger, Grafana, Tempo)
	@which docker > /dev/null || (echo "Docker não encontrado. Instale o Docker primeiro." && exit 1)
	@docker compose version > /dev/null 2>&1 || docker-compose version > /dev/null 2>&1 || (echo "Docker Compose não encontrado. Instale o Docker Compose primeiro." && exit 1)
	@if docker compose version > /dev/null 2>&1; then \
		docker compose up -d; \
	else \
		docker-compose up -d; \
	fi

docker-down: ## Para todos os serviços Docker
	@if docker compose version > /dev/null 2>&1; then \
		docker compose down; \
	else \
		docker-compose down; \
	fi

docker-logs: ## Ver logs dos serviços Docker
	@if docker compose version > /dev/null 2>&1; then \
		docker compose logs -f; \
	else \
		docker-compose logs -f; \
	fi

docker-jaeger: ## Inicia apenas Jaeger
	@if docker compose version > /dev/null 2>&1; then \
		docker compose up -d jaeger; \
	else \
		docker-compose up -d jaeger; \
	fi

docker-grafana: ## Inicia Grafana + Tempo
	@if docker compose version > /dev/null 2>&1; then \
		docker compose up -d grafana tempo; \
	else \
		docker-compose up -d grafana tempo; \
	fi

docker-db: ## Inicia apenas MariaDB
	@if docker compose version > /dev/null 2>&1; then \
		docker compose up -d mariadb; \
	else \
		docker-compose up -d mariadb; \
	fi

docker-restart: ## Reinicia todos os serviços
	@if docker compose version > /dev/null 2>&1; then \
		docker compose restart; \
	else \
		docker-compose restart; \
	fi

docker-clean: ## Para e remove volumes
	@if docker compose version > /dev/null 2>&1; then \
		docker compose down -v; \
	else \
		docker-compose down -v; \
	fi

jaeger: ## Abre Jaeger UI no navegador
	@xdg-open http://localhost:16686 2>/dev/null || open http://localhost:16686 2>/dev/null || echo "Jaeger: http://localhost:16686"

grafana: ## Abre Grafana no navegador
	@xdg-open http://localhost:3001 2>/dev/null || open http://localhost:3001 2>/dev/null || echo "Grafana: http://localhost:3001 (admin/admin)"

observability: docker-jaeger docker-grafana jaeger grafana ## Configura observabilidade completa

dev: install docker-jaeger run ## Instala, inicia Jaeger e roda servidor

all: clean install test docker-up run ## Setup completo
