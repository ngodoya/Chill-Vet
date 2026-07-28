import re

class ValidadorDatos:
    @staticmethod
    def validar_id_unico(id_valor: str, coleccion: list) -> bool:
        """Comprueba que no exista un objeto en la colección con el mismo ID."""
        for item in coleccion:
            # Revisa id_dueno, id_mascota, id_veterinario, id_cita según corresponda
            val_id = getattr(item, 'id_persona', None) or getattr(item, 'id_mascota', None) or \
                     getattr(item, 'id_veterinario', None) or getattr(item, 'id_cita', None)
            if val_id == id_valor.strip():
                return False
        return True

    @staticmethod
    def validar_email(email: str) -> bool:
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(patron, email.strip()))

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        return telefono.strip().isdigit() and len(telefono.strip()) >= 7

    @staticmethod
    def validar_referencias(id_mascota: str, id_veterinario: str, mascotas: list, veterinarios: list) -> bool:
        mascota_existe = any(m.id_mascota == id_mascota for m in mascotas)
        vet_existe = any(v.id_veterinario == id_veterinario for v in veterinarios)
        return mascota_existe and vet_existe