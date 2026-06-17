from datetime import date
class Calendario():
    def __init__(self):
        self._citas_por_fecha = {}
    def mostrar_mes(self, mes:int , año:int):
        citas_fecha = {}
        for i, citas in self._citas_por_fecha.items():
            fecha = date.fromisoformat(i)
            if fecha.month == mes and fecha.year == año:
                citas_fecha[i] = citas
        return citas_fecha
    def marcar_disponibilidad(self, fecha:str, hora:str):
        if fecha not in self._citas_por_fecha:
            self._citas_por_fecha[fecha] = {}
        else:
            self._citas_por_fecha[fecha][hora] = "ocupado"
    def obtener_citas_dia(self, fecha: str):
        return self._citas_por_fecha.get(fecha, {})
