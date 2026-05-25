# ChillVet: Sistema de Gestión para Veterinarias

Bienvenido a **ChillVet**, una aplicación de escritorio desarrollada en Python orientada a facilitar y optimizar la administración de procesos habituales en una clínica veterinaria.

Nuestra meta es brindar una herramienta poderosa y sencilla para registrar, consultar, analizar y visualizar la información vital de tu veterinaria: mascotas, dueños, personal, citas y mucho más.

---

## Características principales

- **CRUD completo**: gestión de mascotas, dueños, veterinarios, citas y historiales médicos.
- **Control de entradas, salidas y estadía** de mascotas.
- **Gestión de turnos y personal**.
- **Manejo de información clínica** y control de tratamientos, vacunas y consultas.
- **Gestión y agendamiento de citas**, con control de estado.
- **Persistencia robusta de datos** con archivos CSV y uso de `pandas` para manipulación y análisis.
- **Extracción y análisis de datos**, generación de informes y reportes estadísticos.
- **Gráficas comparativas e informes automáticos** gracias a `matplotlib`.
- **Interfaz gráfica amigable** (escritorio GUI 100% Python).

---

## Tecnologías utilizadas

- **Python 3.10+**
- **pandas** (gestión y análisis de datos)
- **matplotlib** (visualización de datos)
- **tkinter** o **PySimpleGUI** (interfaz gráfica, decidir según preferencia del equipo)
- **Estructura modular POO**: código organizado en módulos/core/services con clases bien definidas.

---

## Instalación

1. **Clona el repositorio:**
    ```bash
    git clone https://github.com/ngodoya/Chill-Vet.git
    cd Chill-Vet
    ```
2. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

---

## Uso

- Al iniciar la aplicación, tendrás acceso a la interfaz principal donde podrás:
    - Registrar y consultar mascotas y dueños
    - Agendar, mostrar, modificar y cancelar citas
    - Gestionar el personal y sus turnos
    - Registrar entradas y salidas
    - Explorar los historiales médicos
    - Generar y visualizar reportes gráficos e informes de datos consolidados
- Los datos se guardan de manera segura y pueden ser exportados (CSV/Excel) para consultas externas.
- La navegación es intuitiva y pensada para usuarios no técnicos.

---

## Objetivos del proyecto

- Proveer una solución Open Source, modular y escalable para la gestión veterinaria.
- Facilitar el trabajo diario, el análisis y la toma de decisiones sobre la operación de una clínica.
- Permitir el análisis y visualización sencilla de los datos para informar la gestión y mejorar la atención.
- Fomentar la integración de buenas prácticas de programación orientada a objetos y uso avanzado de librerías de datos en Python.

---

*La estructura de paquetes, el UML y la documentación detallada se encuentran en la sección Wiki del repositorio.*