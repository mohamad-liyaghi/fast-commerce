.PHONY: help build run stop test admin confmap

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

confmap:
	kubectl create configmap fast-commerce-env --from-env-file=envs/cache.env --from-env-file=envs/celery.env --from-env-file=envs/jwt.env --from-env-file=envs/mail.env --from-env-file=envs/pg.env --from-env-file=envs/redis.env
