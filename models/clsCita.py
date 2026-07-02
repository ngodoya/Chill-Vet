from datetime import datetime


class Cita:
    def __init__(self, id_cita: str, fecha_hora: datetime, motivo: str, estado: str, id_mascota: str, id_veterinario: str):
        self.id_cita = id_cita.strip()
        self.fecha_hora = fecha_hora
        self.motivo = motivo.strip()
        self.estado = estado.strip().upper()
        self.id_mascota = id_mascota.strip()
        self.id_veterinario = id_veterinario.strip()

    def cancelar(self):
        self.estado = "CANCELADA"

    def confirmar(self):
        self.estado = "CONFIRMADA"

    def reprogramar(self, nueva_fecha_hora: datetime):
        self.fecha_hora = nueva_fecha_hora