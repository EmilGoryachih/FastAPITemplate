#!make

.PHONY: run
run:
	@uvicorn main:app --reload --host 0.0.0.0 --port 80

.PHONY: init-alembic
init-alembic:
	@alembic init alembic && cd ..

.PHONY: migration-create
migration-create:
	@alembic revision --autogenerate -m "$(name)" && cd ..

.PHONY: migration-up
migration-up:
	@alembic upgrade head && cd ..

.PHONY: migration-down
migration-down:
	@alembic downgrade -1 && cd ..
