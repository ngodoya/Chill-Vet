class GestorCitas: 
    def __init__(self, citas: dict): 
        self.__citas = citas

    def agendar_cita(self, cita): 
        print("Agendar cita")
    def cancelar_cita(self, cita):
        print("Cancelar cita")
    def obtener_citas(self, fecha):
        print("Obtener citas")
    def obtener_todas(self): 
        print("Obtener todas las citas") 
