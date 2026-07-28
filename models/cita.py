from datetime import datetime


class Cita:
    def __init__(
        self,
        id_cita: str,
        fecha_hora: datetime | str,
        motivo: str,
        estado: str,
        id_mascota: str,
        id_veterinario: str,
    ):
        self.id_cita = id_cita.strip()
        # Normalice fecha_hora a objeto datetime internamente
        if isinstance(fecha_hora, str):
            self.fecha_hora = datetime.strptime(fecha_hora.strip(), "%Y-%m-%d %H:%M:%S")
        else:
            self.fecha_hora = fecha_hora

        self.motivo = motivo.strip()
        self.estado = estado.strip().upper()
        self.id_mascota = id_mascota.strip()
        self.id_veterinario = id_veterinario.strip()

    def cancelar(self) -> None:
        self.estado = "CANCELADA"

    def confirmar(self) -> None:
        self.estado = "CONFIRMADA"

    def reprogramar(self, nueva_fecha_hora: datetime | str) -> None:
        if isinstance(nueva_fecha_hora, str):
            self.fecha_hora = datetime.strptime(
                nueva_fecha_hora.strip(), "%Y-%m-%d %H:%M:%S"
            )
        else:
            self.fecha_hora = nueva_fecha_hora

    def fecha_hora_str(self) -> str:
        """Retorna la fecha en string para persistencia CSV/Pandas"""
        return self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
