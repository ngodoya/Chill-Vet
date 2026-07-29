from models.dueno import Dueno
from models.mascota import Mascota
from models.cita import Cita
from services.gestor_citas import GestorCitas
from persistence.gestor_datos_base import GestorDatos
from datetime import datetime
import uuid


class SistemaVeterinaria:
    """
    Orquestador central del sistema (pseudo-CRUD).
    """

    def __init__(self):
        self.gestor_datos = GestorDatos()
        self.duenos = []
        self.mascotas = []
        self.gestor_citas = GestorCitas()
        self._cargar_datos()

    def _cargar_datos(self):
        for d in self.gestor_datos.cargar_duenos():
            self.duenos.append(
                Dueno(
                    d["id_persona"],
                    d["nombre"],
                    d["telefono"],
                    d["email"],
                    d.get("direccion", ""),
                )
            )
        for m in self.gestor_datos.cargar_mascotas():
            self.mascotas.append(
                Mascota(
                    m["id_mascota"],
                    m["nombre"],
                    m["especie"],
                    m["raza"],
                    m["edad"],
                    m["sexo"],
                    m["peso"],
                    m["id_dueno"],
                )
            )
        for c in self.gestor_datos.cargar_citas():
            # absGestorDatos normalizes to "%Y-%m-%d %H:%M"
            fecha_dt = (
                datetime.strptime(c["fecha_hora"], GestorDatos.FORMATO_FECHA)
                if isinstance(c["fecha_hora"], str)
                else c["fecha_hora"]
            )
            cita = Cita(
                c["id_cita"],
                fecha_dt,
                c["motivo"],
                c["estado"],
                c["id_mascota"],
                c["id_veterinario"],
            )
            self.gestor_citas.citas.append(cita)

    # Dueños
    def crear_dueno(self, dueno: Dueno) -> bool:
        if any(d.id_persona == dueno.id_persona for d in self.duenos):
            return False
        self.duenos.append(dueno)
        self.gestor_datos.guardar_duenos(self.duenos)
        return True

    def buscar_dueno(self, id_dueno: str):
        return next((d for d in self.duenos if d.id_persona == id_dueno), None)

    def listar_duenos(self):
        return list(self.duenos)

    # Mascotas
    def crear_mascota(self, mascota: Mascota) -> bool:
        if any(m.id_mascota == mascota.id_mascota for m in self.mascotas):
            return False
        if self.buscar_dueno(mascota.id_dueno) is None:
            return False
        self.mascotas.append(mascota)
        self.gestor_datos.guardar_mascotas(self.mascotas)
        return True

    def buscar_mascota(self, id_mascota: str):
        return next((m for m in self.mascotas if m.id_mascota == id_mascota), None)

    def listar_mascotas(self):
        return list(self.mascotas)

    def listar_mascotas_por_dueno(self, id_dueno: str):
        return [m for m in self.mascotas if m.id_dueno == id_dueno]

    # Citas
    def agendar_cita(self, cita: Cita) -> bool:
        mascota = self.buscar_mascota(cita.id_mascota)
        if mascota is None:
            return False
        exito = self.gestor_citas.agendar_cita(cita)
        if exito:
            self.gestor_datos.guardar_citas(self.gestor_citas.listar_citas())
        return exito

    def cancelar_cita(self, id_cita: str) -> bool:
        exito = self.gestor_citas.cancelar_cita(id_cita)
        if exito:
            self.gestor_datos.guardar_citas(self.gestor_citas.listar_citas())
        return exito

    def modificar_cita(self, id_cita: str, **cambios) -> bool:
        cita = self.gestor_citas.buscar_cita(id_cita)
        if not cita:
            return False
        if "motivo" in cambios:
            cita.motivo = cambios["motivo"]
        if "fecha_hora" in cambios:
            cita.fecha_hora = cambios["fecha_hora"]
        if "id_veterinario" in cambios:
            cita.id_veterinario = cambios["id_veterinario"]
        self.gestor_datos.guardar_citas(self.gestor_citas.listar_citas())
        return True

    def eliminar_cita(self, id_cita: str) -> bool:
        exito = self.gestor_citas.eliminar_cita(id_cita)
        if exito:
            self.gestor_datos.guardar_citas(self.gestor_citas.listar_citas())
        return exito

    def listar_citas(self):
        return self.gestor_citas.listar_citas()

    # Helpers para la GUI
    def obtener_o_crear_dueno(self, nombre: str) -> Dueno:
        for d in self.duenos:
            if d.nombre.lower() == nombre.lower():
                return d
        nuevo_dueno = Dueno(
            id_persona=str(uuid.uuid4())[:8], nombre=nombre, telefono="", email=""
        )
        self.crear_dueno(nuevo_dueno)
        return nuevo_dueno

    def obtener_o_crear_mascota(self, nombre: str, dueno: Dueno) -> Mascota:
        for m in self.mascotas:
            if m.nombre.lower() == nombre.lower() and m.id_dueno == dueno.id_persona:
                return m
        nueva_mascota = Mascota(
            id_mascota=str(uuid.uuid4())[:8],
            nombre=nombre,
            especie="Desconocida",
            raza="Desconocida",
            edad=0,
            sexo="Desconocido",
            peso=0.0,
            id_dueno=dueno.id_persona,
        )
        self.crear_mascota(nueva_mascota)
        return nueva_mascota
