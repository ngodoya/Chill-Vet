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

# Instalar dependencias
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Formatear el código automáticamente
format:
	ruff format .

# Revisar estilo y autocorregir lo posible
lint:
	ruff check . --fix || true

# Verificar tipos
typecheck:
	mypy . --ignore-missing-imports || true

# Ejecutar la misma verificación del CI en tu máquina antes de hacer git push
ci: format lint typecheck

# Limpiar archivos de caché generados por Python, Ruff y Mypy
clean:
	rm -rf .ruff_cache .mypy_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -r {} +