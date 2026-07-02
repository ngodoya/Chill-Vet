class Mascota:
    def __init__(
        self,
        id_mascota: str,
        nombre: str,
        especie: str,
        raza: str,
        edad: int,
        sexo: str,
        peso: float,
        id_dueno: str
    ):
        self.id_mascota = id_mascota.strip()
        self.nombre = nombre.strip()
        self.especie = especie.strip()
        self.raza = raza.strip()
        self.edad = int(edad)
        self.sexo = sexo.strip()
        self.peso = float(peso)
        self.id_dueno = id_dueno.strip()

    def actualizar_datos(
        self,
        nombre: str | None = None,
        especie: str | None = None,
        raza: str | None = None,
        edad: int | None = None,
        sexo: str | None = None,
        peso: float | None = None,
        id_dueno: str | None = None
    ) -> None:
        if nombre is not None:
            self.nombre = nombre.strip()
        if especie is not None:
            self.especie = especie.strip()
        if raza is not None:
            self.raza = raza.strip()
        if edad is not None:
            self.edad = int(edad)
        if sexo is not None:
            self.sexo = sexo.strip()
        if peso is not None:
            self.peso = float(peso)
        if id_dueno is not None:
            self.id_dueno = id_dueno.strip()

    def __repr__(self):
        return f"Mascota(id={self.id_mascota}, nombre={self.nombre}, especie={self.especie}, raza={self.raza}, edad={self.edad}, sexo={self.sexo}, peso={self.peso}, id_dueno={self.id_dueno})"