from models.clsDueno import Dueno
from models.clsMascota import Mascota
from models.clsCita import Cita
from services.clsGestor_citas import GestorCitas

class SistemaVeterinaria:
    """
    Orquestador central del sistema (pseudo-CRUD).
    """
    def __init__(self):
        self.duenos = []    
        self.mascotas = []    
        self.gestor_citas = GestorCitas()

    # Dueños
    def crear_dueno(self, dueno: Dueno) -> bool:
        if any(d.id_persona == dueno.id_persona for d in self.duenos):
            return False
        self.duenos.append(dueno)
        return True

    def buscar_dueno(self, id_dueno: str):
        return next((d for d in self.duenos if d.id_persona == id_dueno), None)

    def listar_duenos(self):
        return self.duenos

    # Mascotas
    def crear_mascota(self, mascota: Mascota) -> bool:
        if any(m.id_mascota == mascota.id_mascota for m in self.mascotas):
            return False
        if self.buscar_dueno(mascota.id_dueno) is None:
            return False
        self.mascotas.append(mascota)
        return True

    def buscar_mascota(self, id_mascota: str):
        return next((m for m in self.mascotas if m.id_mascota == id_mascota), None)

    def listar_mascotas(self):
        return self.mascotas

    def listar_mascotas_por_dueno(self, id_dueno: str):
        return [m for m in self.mascotas if m.id_dueno == id_dueno]

    # Citas
    def agendar_cita(self, cita: Cita) -> bool:
        mascota = self.buscar_mascota(cita.id_mascota)
        if mascota is None:
            return False
        return self.gestor_citas.agendar_cita(cita)

    def cancelar_cita(self, id_cita: str) -> bool:
        return self.gestor_citas.cancelar_cita(id_cita)

    def listar_citas(self):
        return self.gestor_citas.listar_citas()