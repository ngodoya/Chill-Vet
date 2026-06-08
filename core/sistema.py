from services import GestorCitas, Calendario
from persistence import GestorDatos

class SistemaVeterinaria:
    def __init__(self, gestor_citas: GestorCitas, calendario: Calendario):
        self.__gestor_citas = gestor_citas
        self.__calendario = calendario
        self.__gestor_datos = GestorDatos()

    def get_gestor_citas(self):
        return self.__gestor_citas
    
    def get_calendario(self):
        return self.__calendario
    
    def iniciar_sistema(self):
        print("Iniciando sistema de veterinaria...")

    def cerrar_sistema(self):
        print("Cerrando sistema de veterinaria...")