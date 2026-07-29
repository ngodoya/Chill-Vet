# Variables
PYTHON = python
PIP = pip

.PHONY: help install lint format typecheck ci clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instala y actualiza dependencias"
	@echo "  make format     - Formatea el código automáticamente con Ruff"
	@echo "  make lint       - Corrige y revisa errores de estilo con Ruff"
	@echo "  make typecheck  - Ejecuta la revisión de tipos con Mypy"
	@echo "  make ci         - Corre todo el flujo de verificación local"
	@echo "  make clean      - Elimina archivos temporales y cachés de Python"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

format:
	ruff format .

lint:
	ruff check . --fix || true

typecheck:
	mypy . --ignore-missing-imports || true

ci: format lint typecheck

clean:
	rm -rf .ruff_cache .mypy_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -r {} +