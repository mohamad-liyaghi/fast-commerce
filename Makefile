.PHONY: help build run stop test admin confmap k8s

help:
	@echo "Available targets:"
	@echo "  help    - Show this help message."
	@echo "  build   - Build the docker image."
	@echo "  run     - Run the docker container."
	@echo "  stop    - Stop the docker container."
	@echo "  test    - Run the tests."
	@echo "  admin   - Create an admin user."
	@echo " confmap - Create a configmap for kubernetes."
	@echo " k8s - Run project using kubernetes."
	@echo " test_k8s - Test Project On Kubernetes."


build:
	docker compose build

run:
ifeq ($(DETACHED),true)
	docker compose up -d
else
	docker compose up
endif

deploy:
	docker compose -f docker-compose.prod.yaml up -d

stop:
	docker compose down

test:
	docker exec fast-commerce-backend pytest

admin:
	docker exec -it fast-commerce-backend python scripts/create_admin.py

confmap:
	kubectl create configmap fast-commerce-env --from-env-file=backend/envs/cache.env --from-env-file=backend/envs/celery.env --from-env-file=backend/envs/jwt.env --from-env-file=backend/envs/mail.env --from-env-file=backend/envs/pg.env --from-env-file=backend/envs/redis.env

k8s:
	kubectl apply -f kubernetes/

test_k8s:
	kubectl exec -it $(shell kubectl get pods | grep backend | awk '{print $$1}') -- pytest
