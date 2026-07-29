# Chill-Vet

Sistema de gestión para clínicas veterinarias que permite administrar clientes (dueños), mascotas y agendamiento de citas con control de disponibilidad y resolución de conflictos de horario.

---

## Requisitos Previos

- **Python:** `3.8` o superior (utilizamos anotaciones de tipo avanzadas como `from __future__ import annotations` y sintaxis moderna de la librería estándar `datetime`).

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/ngodoya/Chill-Vet.git
cd Chill-Vet
```

### 2. Crear y activar el entorno virtual

- En Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

- En Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

Con el entorno virtual activado, instala las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

`requirements.txt` incluye tanto las dependencias del proyecto como las herramientas de calidad de código:

```
# Dependencias del proyecto
pandas>=2.0.0,<3.0.0

# Herramientas de calidad de código y CI
ruff==0.6.9
mypy>=1.5.0
```

> Este paso también puede hacerse con `make install` (ver la sección de Makefile más abajo), que además actualiza `pip` antes de instalar.

---

## Ejecutar la Aplicación

Con las dependencias instaladas y el entorno virtual activo, inicia la aplicación con:

```bash
python main.py
# Si no funciona pruebe:
python3 main.py
```

---

## Makefile: Comandos Disponibles

El proyecto incluye un `Makefile` que centraliza las tareas comunes de instalación, formateo, linting, verificación de tipos y limpieza, para no tener que recordar cada comando individual.

Para ver la lista de comandos disponibles en cualquier momento:

```bash
make help
```

| Comando          | Descripción                                            |
|-------------------|--------------------------------------------------------|
| `make install`    | Instala y actualiza las dependencias del proyecto      |
| `make format`     | Formatea el código automáticamente con Ruff             |
| `make lint`       | Corrige y revisa errores de estilo con Ruff              |
| `make typecheck`  | Ejecuta la revisión de tipos con Mypy                    |
| `make ci`         | Corre todo el flujo de verificación local (`format` + `lint` + `typecheck`) |
| `make clean`      | Elimina archivos temporales y cachés de Python           |

**Flujo recomendado antes de un commit:**

```bash
make ci
```

Esto formatea el código, corrige errores de estilo cuando es posible, y valida los tipos en un solo paso.

---

## Calidad de Código y Estándares (CI / Linter)

El proyecto utiliza **Ruff** para garantizar el cumplimiento de los estándares de código de Python (PEP 8), detección de errores y formateo automático, y **Mypy** para la revisión de tipos.

Para verificar que el código cumple con las reglas del linter y el formato antes de realizar un commit, ejecuta:

```bash
# Comprobar errores de código e importaciones
ruff check .

# Verificar el formato del código
ruff format --check .
```

Estas mismas verificaciones se ejecutan automáticamente en el pipeline de CI (ver el badge al inicio del documento).

---

## Documentación y Wiki

Para consultar la información detallada sobre la arquitectura del proyecto, la estructura de paquetes/módulos y los diagramas de clases UML, revisa nuestra Wiki oficial:

[Wiki del Proyecto Chill-Vet](https://github.com/ngodoya/Chill-Vet/wiki)

En la Wiki encontrarás:

- **Estructura de Módulos y Paquetes:** Explicación de los paquetes `models` y `services`.
- **Diagrama UML:** Especificaciones y relaciones entre las clases (`SistemaVeterinaria`, `GestorCitas`, `Calendario`, etc.).
- **Reglas de Negocio:** Detalle sobre la validación de solapamiento de citas y estados del sistema.