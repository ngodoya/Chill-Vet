.PHONY: lint lint-fix

lint:
	ruff check .
	ruff format --check .

lint-fix:
	ruff check . --fix
	ruff format .