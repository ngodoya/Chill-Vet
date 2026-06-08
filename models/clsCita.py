from datetime import date, time

class Cita:
    def __init__(self, id:str, fecha: date, hora: time, mascota_id: str, veterinario_id: str, motivo: str, estado: str):
        
        self.fecha = fecha
        self.hora = hora
        self.id = id
        self.mascota_id = mascota_id
        self.veterinario_id = veterinario_id
        self.motivo = motivo
        self.estado = estado