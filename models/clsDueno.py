from models.absPersona import Persona


class Dueno(Persona):
    def __init__(self, id_persona: str, nombre: str, telefono: str, email: str, direccion: str = ""):
        super().__init__(id_persona, nombre, telefono, email)
        self.direccion = direccion.strip()
