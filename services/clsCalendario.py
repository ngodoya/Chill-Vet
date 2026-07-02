from datetime import datetime
from typing import List


class Calendario:
    """
    Gestiona disponibilidad y conflictos de horario para citas.
    Supone bloques de 1 hora por cita.
    """

    DURACION_CITA_MIN = 60

    @staticmethod
    def hay_conflicto(citas: List, id_veterinario: str, fecha_hora_nueva: datetime) -> bool:
        for cita in citas:
            if cita.id_veterinario != id_veterinario:
                continue
            if str(cita.estado).upper() == "CANCELADA":
                continue

            diferencia = abs((cita.fecha_hora - fecha_hora_nueva).total_seconds()) / 60
            if diferencia < Calendario.DURACION_CITA_MIN:
                return True
        return False

    @staticmethod
    def citas_por_dia(citas: List, fecha_objetivo: datetime) -> List:
        return [
            c for c in citas
            if c.fecha_hora.date() == fecha_objetivo.date() and str(c.estado).upper() != "CANCELADA"
        ]

    @staticmethod
    def citas_por_mes(citas: List, anio: int, mes: int) -> List:
        return [
            c for c in citas
            if c.fecha_hora.year == anio and c.fecha_hora.month == mes and str(c.estado).upper() != "CANCELADA"
        ]