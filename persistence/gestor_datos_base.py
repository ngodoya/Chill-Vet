from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, cast

try:
    import pandas as pd  # type: ignore
except Exception as e:
    raise RuntimeError(
        "Pandas es necesario para GestorDatos. Instala con 'pip install pandas'."
    ) from e


class GestorDatos:
    """
    Persistencia CSV usando pandas para CHILL-VET.
    - Carga y guarda dueños, mascotas y citas.
    - Si archivo no existe, retorna lista vacía.
    - Estandariza fecha_hora de citas: %Y-%m-%d %H:%M
    """

    FORMATO_FECHA = "%Y-%m-%d %H:%M"

    def __init__(self, carpeta_data: str = "data") -> None:
        self.carpeta_data = Path(carpeta_data)
        self.carpeta_data.mkdir(parents=True, exist_ok=True)

        self.archivo_duenos = self.carpeta_data / "duenos.csv"
        self.archivo_mascotas = self.carpeta_data / "mascotas.csv"
        self.archivo_citas = self.carpeta_data / "citas.csv"

    def cargar_citas_csv(self, archivo: str | Path) -> list[dict[str, Any]]:
        return self._leer_csv(
            Path(archivo),
            columnas_esperadas=[
                "id_cita",
                "fecha_hora",
                "motivo",
                "estado",
                "id_mascota",
                "id_veterinario",
            ],
        )

    def guardar_citas_csv(self, archivo: str | Path, citas: Iterable[Any]) -> None:
        filas = [self._obj_a_dict(c) for c in citas]
        for f in filas:
            if "fecha_hora" in f:
                f["fecha_hora"] = self._normalizar_fecha_hora(f["fecha_hora"])
        self._escribir_csv(
            Path(archivo),
            filas,
            columnas=[
                "id_cita",
                "fecha_hora",
                "motivo",
                "estado",
                "id_mascota",
                "id_veterinario",
            ],
        )

    def cargar_duenos(self) -> list[dict[str, Any]]:
        return self._leer_csv(
            self.archivo_duenos,
            columnas_esperadas=[
                "id_persona",
                "nombre",
                "telefono",
                "email",
                "direccion",
            ],
        )

    def guardar_duenos(self, duenos: Iterable[Any]) -> None:
        filas = [self._obj_a_dict(d) for d in duenos]
        self._escribir_csv(
            self.archivo_duenos,
            filas,
            columnas=["id_persona", "nombre", "telefono", "email", "direccion"],
        )

    def cargar_mascotas(self) -> list[dict[str, Any]]:
        filas = self._leer_csv(
            self.archivo_mascotas,
            columnas_esperadas=[
                "id_mascota",
                "nombre",
                "especie",
                "raza",
                "edad",
                "sexo",
                "peso",
                "id_dueno",
            ],
        )
        for f in filas:
            if "edad" in f and str(f["edad"]).strip() != "":
                try:
                    f["edad"] = int(f["edad"])
                except (ValueError, TypeError):
                    f["edad"] = 0

            if "peso" in f and str(f["peso"]).strip() != "":
                try:
                    f["peso"] = float(f["peso"])
                except (ValueError, TypeError):
                    f["peso"] = 0.0

        return filas

    def guardar_mascotas(self, mascotas: Iterable[Any]) -> None:
        filas = [self._obj_a_dict(m) for m in mascotas]
        self._escribir_csv(
            self.archivo_mascotas,
            filas,
            columnas=[
                "id_mascota",
                "nombre",
                "especie",
                "raza",
                "edad",
                "sexo",
                "peso",
                "id_dueno",
            ],
        )

    def cargar_citas(self) -> list[dict[str, Any]]:
        filas = self._leer_csv(
            self.archivo_citas,
            columnas_esperadas=[
                "id_cita",
                "fecha_hora",
                "motivo",
                "estado",
                "id_mascota",
                "id_veterinario",
            ],
        )
        for f in filas:
            if "fecha_hora" in f:
                f["fecha_hora"] = self._normalizar_fecha_hora(f["fecha_hora"])
        return filas

    def guardar_citas(self, citas: Iterable[Any]) -> None:
        filas = [self._obj_a_dict(c) for c in citas]
        for f in filas:
            if "fecha_hora" in f:
                f["fecha_hora"] = self._normalizar_fecha_hora(f["fecha_hora"])
        self._escribir_csv(
            self.archivo_citas,
            filas,
            columnas=[
                "id_cita",
                "fecha_hora",
                "motivo",
                "estado",
                "id_mascota",
                "id_veterinario",
            ],
        )

    def _leer_csv(
        self, ruta: Path, columnas_esperadas: list[str]
    ) -> list[dict[str, Any]]:
        if not ruta.exists():
            return []

        try:
            df = pd.read_csv(ruta)
        except Exception as e:
            raise RuntimeError(f"Error leyendo CSV {ruta}: {e}") from e

        for col in columnas_esperadas:
            if col not in df.columns:
                df[col] = ""

        df = df[columnas_esperadas]
        df = df.fillna("")
        return df.to_dict(orient="records")

    def _escribir_csv(
        self, ruta: Path, filas: list[dict[str, Any]], columnas: list[str]
    ) -> None:
        if not filas:
            # Guardar archivo vacío con headers
            df = pd.DataFrame(columns=columnas)
            df.to_csv(ruta, index=False, encoding="utf-8")
            return

        df = pd.DataFrame(filas)

        for col in columnas:
            if col not in df.columns:
                df[col] = ""

        df = df[columnas]
        df.to_csv(ruta, index=False, encoding="utf-8")

    def _obj_a_dict(self, obj: Any) -> dict[str, Any]:
        if isinstance(obj, dict):
            return dict(obj)
        if is_dataclass(obj):
            return asdict(cast(Any, obj))
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}

    def _normalizar_fecha_hora(self, valor: Any) -> str:
        if isinstance(valor, datetime):
            return valor.strftime(self.FORMATO_FECHA)

        s = str(valor).strip()
        if not s:
            return ""

        for fmt in (self.FORMATO_FECHA, "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.strptime(s, fmt)
                return dt.strftime(self.FORMATO_FECHA)
            except ValueError:
                continue

        return s
