# Chill-Vet

Sistema de gestión para clínicas veterinarias que permite administrar clientes (dueños), mascotas y agendamiento de citas con control de disponibilidad y resolución de conflictos de horario.

---

## Requisitos Previos

- **Python:** `3.8` o superior (utilizamos anotaciones de tipo avanzadas como `from __future__ import annotations` y sintaxis moderna de la librería estándar `datetime`).

---

## Inicio Rápido

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/ngodoya/Chill-Vet.git
   cd Chill-Vet
   ```

2. **Ejecutar el proyecto:**

   ```bash
   python main.py
   ```

---

## Documentación y Wiki

Para consultar la información detallada sobre la arquitectura del proyecto, la estructura de paquetes/módulos y los diagramas de clases UML, revisa nuestra Wiki oficial:

[Wiki del Proyecto Chill-Vet](https://github.com/ngodoya/Chill-Vet/wiki)

En la Wiki encuentra:

- **Estructura de Módulos y Paquetes:** Explicación de los paquetes `models` y `services`.
- **Diagrama UML:** Especificaciones y relaciones entre las clases (`SistemaVeterinaria`, `GestorCitas`, `Calendario`, etc.).
## Calidad de Código y Estándares (CI/Linter)

El proyecto utiliza **Ruff** para garantizar el cumplimiento de los estándares de código de Python (PEP 8), detección de errores y formateo automático.

### Verificación local

Para verificar que el código cumple con las reglas del linter y el formato antes de realizar un commit, ejecuta:

```bash
# Comprobar errores de código e importaciones
ruff check .

# Verificar el formato del código
ruff format --check .