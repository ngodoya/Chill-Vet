from models import absPersona
class Dueno(absPersona): 
    def __init__(self, id: str, nombre: str, telefono: str, email: str):
        super().__init__(id, nombre)
        self.telefono = telefono
        self.email = email
