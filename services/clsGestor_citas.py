from __future__ import annotations
from datetime import datetime, date
from typing import List, Optional

from models.clsCita import Cita
from services.clsCalendario import Calendario


class GestorCitas:
    """
    Pseudo-CRUD de citas en memoria.
    """
    def __init__(self) -> None:
        self.citas: List[Cita] = []
        self.calendario = Calendario()

    def agendar_cita(self, cita: Cita) -> bool:
        # ID único
        if self.buscar_cita(cita.id_cita) is not None:
            return False

        # Conflicto horario por veterinario (ignora canceladas)
        if self.calendario.hay_conflicto(self.citas, cita.id_veterinario, cita.fecha_hora):
            return False

        self.citas.append(cita)
        return True

    def cancelar_cita(self, id_cita: str) -> bool:
        cita = self.buscar_cita(id_cita)
        if cita is None:
            return False
        cita.cancelar()
        return True

    def reprogramar_cita(self, id_cita: str, nueva_fecha_hora: datetime) -> bool:
        cita = self.buscar_cita(id_cita)
        if cita is None:
            return False

        # validar conflicto excluyendo la cita actual
        citas_sin_actual = [c for c in self.citas if c.id_cita != id_cita]
        if self.calendario.hay_conflicto(citas_sin_actual, cita.id_veterinario, nueva_fecha_hora):
            return False

        cita.reprogramar(nueva_fecha_hora)
        return True

    def obtener_citas_por_fecha(self, fecha: date) -> List[Cita]:
        return [c for c in self.citas if c.fecha_hora.date() == fecha]

    def listar_citas(self) -> List[Cita]:
        return list(self.citas)

    def buscar_cita(self, id_cita: str) -> Optional[Cita]:
        return next((c for c in self.citas if c.id_cita == id_cita), None)

    def eliminar_cita(self, id_cita: str) -> bool:
        cita = self.buscar_cita(id_cita)
        if cita is None:
            return False
        self.citas.remove(cita)
        return True