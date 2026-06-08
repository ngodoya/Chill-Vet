from abc import ABC, abstractmethod

class Persona(ABC): 
    def __init__(self, id: str, nombre: str):
        self._id = id
        self._nombre = nombre
    
#Como van a acceder desde otras subclases.