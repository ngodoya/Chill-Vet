from models import absPersona

class Veterinario(absPersona):
    def __init__(self, id: str, nombre: str, especialidad: str):
        super().__init__(id, nombre)
        self.especialidad = especialidad