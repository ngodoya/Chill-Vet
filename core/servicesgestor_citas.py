class GestorCitas():
    def __init__(self):
        self.citas = {}
    def agendar_cita(self, cita: dict):
        cita_id = cita.get("id")
        if cita_id is None:
            raise ValueError("La cita debe tener un campo 'id'")
        if cita_id in self.citas:
            raise ValueError("Ya existe una cita con id ", cita_id)
        self.citas[cita_id] = cita
    def cancelar_cita(self, id: str):
        if id not in self.citas:
            raise ValueError("Intente denuevo, no existe una cita con id", id)
        else: 
            del self.citas[id]
    def obtener_cita(self, fecha: str):
        fecha_cita = []
        for i in self.citas.values():
            if i.get("fecha") == fecha:
                fecha_cita.append(i)
        return fecha_cita
    def obtener_todas(self):
        return list(self.citas.values())