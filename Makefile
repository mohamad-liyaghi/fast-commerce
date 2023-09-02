.PHONY: help build run stop test admin

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  admin   - Create an admin user."
	@echo " ruff    - Run ruff check for backend code."



build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

stop:
	docker compose down

test:
	docker exec fast-commerce-backend pytest

admin:
	docker exec -it fast-commerce-backend python scripts/create_admin.py

ruff:
	docker exec -it fast-commerce-backend ruff check .