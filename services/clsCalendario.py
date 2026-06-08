class Calendario: 
    def __init__(self, citas_por_fecha: dict):
        self.__citas_por_fecha = citas_por_fecha
    
    def get_citas_por_fecha(self):
        return self.__citas_por_fecha
    def set_citas_por_fecha(self, citas_por_fecha: dict):
        self.__citas_por_fecha = citas_por_fecha
    
    def mostrar_mes(self, mes, año): 
        print("Mes, año")

    def marcar_disponibilidad(self, fecha, hora): 
        print("Marcar disponibilidad")
    
    def obtener_citas_dia(self, fecha): 
        print("Obtener citas del día")
        