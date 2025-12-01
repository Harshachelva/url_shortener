.PHONY: help build up down logs clean restart status test-api

help:
	@echo "URL Shortener - Available commands:"
	@echo "  make build       - Build all Docker containers"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make clean       - Remove all containers, volumes, and images"
	@echo "  make restart     - Restart all services"
	@echo "  make status      - Show status of all services"
	@echo "  make test-api    - Test the API endpoints"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services starting..."
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:5000"
	@echo "Redis: localhost:6379"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-frontend:
	docker-compose logs -f frontend

clean:
	docker-compose down -v --rmi all
	@echo "All containers, volumes, and images removed"

restart:
	docker-compose restart

status:
	docker-compose ps

test-api:
	@echo "Testing API health..."
	@curl -s http://localhost:5000/health | python3 -m json.tool
	@echo "\nTesting URL shortening..."
	@curl -s -X POST http://localhost:5000/shorten \
		-H "Content-Type: application/json" \
		-d '{"url": "https://www.example.com/very-long-url"}' | python3 -m json.tool
shell-api:
	docker exec -it flask-api /bin/bash

shell-redis:
	docker exec -it redis-server redis-cli