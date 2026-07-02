from models.absPersona import Persona
class Dueno(Persona): 
    def __init__(self, id: str, nombre: str, telefono: str, email: str):
        super().__init__(id, nombre, telefono, email)
