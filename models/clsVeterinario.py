from models.absPersona import Persona

class Veterinario(Persona):
    def __init__(self, id_persona: str, nombre: str, telefono: str, email: str, especialidad: str):
        super().__init__(id_persona, nombre, telefono, email)
        self.especialidad = especialidad