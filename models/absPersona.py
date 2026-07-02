from abc import ABC


class Persona(ABC):
    def __init__(self, id_persona: str, nombre: str, telefono: str, email: str):
        self.id_persona = id_persona.strip()
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()

    def actualizar_datos(
    self,
    nombre: str | None = None,
    telefono: str | None = None,
    email: str | None = None
    ) -> None:
        if nombre is not None:
            self.nombre = nombre.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if email is not None:
            self.email = email.strip()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id_persona}, nombre={self.nombre}, telefono={self.telefono}, email={self.email})"