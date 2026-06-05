.PHONY: up down logs test lint dev

up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	pytest tests/ -v --cov=api --cov-fail-under=75

# Linter supprimé suite aux demandes, la commande lint ne fera rien ou un simple message.
lint:
	@echo "Linting ignoré (désactivé pour ce projet)."

dev-api:
	cd api && uvicorn main:app --reload --port 8000

dev-dash:
	cd dashboard && streamlit run app.py --server.port 8501
