import os
import pandas as pd  # type: ignore
from models.mascota import Mascota
from models.cita import Cita

RUTA_MASCOTAS = os.path.join("data", "mascotas.csv")
RUTA_CITAS = os.path.join("data", "citas.csv")

COLUMNAS_MASCOTAS = [
    "id_mascota",
    "nombre",
    "especie",
    "raza",
    "edad",
    "sexo",
    "peso",
    "id_dueno",
]
COLUMNAS_CITAS = [
    "id_cita",
    "fecha_hora",
    "motivo",
    "estado",
    "id_mascota",
    "id_veterinario",
]
FORMATO_FECHA_HORA = "%Y-%m-%d %H:%M"


def cargar_mascotas():
    if not os.path.exists(RUTA_MASCOTAS):
        return []
    df = pd.read_csv(RUTA_MASCOTAS)
    return [
        Mascota(
            id_mascota=fila["id_mascota"],
            nombre=fila["nombre"],
            especie=fila["especie"],
            raza=fila["raza"],
            edad=fila["edad"],
            sexo=fila["sexo"],
            peso=fila["peso"],
            id_dueno=fila["id_dueno"],
        )
        for i, fila in df.iterrows()
    ]


def guardar_mascotas(lista_mascotas):
    df = pd.DataFrame([i.to_dict() for i in lista_mascotas], columns=COLUMNAS_MASCOTAS)
    os.makedirs(os.path.dirname(RUTA_MASCOTAS), exist_ok=True)
    df.to_csv(RUTA_MASCOTAS, index=False)


def _leer_citas_df():
    if not os.path.exists(RUTA_CITAS):
        return pd.DataFrame(columns=COLUMNAS_CITAS)
    df = pd.read_csv(RUTA_CITAS)
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], format=FORMATO_FECHA_HORA)
    return df


def _df_a_citas(df):
    return [
        Cita(
            id_cita=fila["id_cita"],
            fecha_hora=fila["fecha_hora"].to_pydatetime(),
            motivo=fila["motivo"],
            estado=fila["estado"],
            id_mascota=fila["id_mascota"],
            id_veterinario=fila["id_veterinario"],
        )
        for _, fila in df.iterrows()
    ]


def cargar_citas():
    return _df_a_citas(_leer_citas_df())


def guardar_citas(lista_citas):
    df = pd.DataFrame(
        [i.to_dict(FORMATO_FECHA_HORA) for i in lista_citas], columns=COLUMNAS_CITAS
    )
    os.makedirs(os.path.dirname(RUTA_CITAS), exist_ok=True)
    df.to_csv(RUTA_CITAS, index=False)


def agregar_cita(cita: Cita):
    df = _leer_citas_df()
    nueva_fila = pd.DataFrame(
        [
            {
                "id_cita": cita.id_cita,
                "fecha_hora": cita.fecha_hora.strftime(FORMATO_FECHA_HORA),
                "motivo": cita.motivo,
                "estado": cita.estado,
                "id_mascota": cita.id_mascota,
                "id_veterinario": cita.id_veterinario,
            }
        ]
    )
    nueva_fila["fecha_hora"] = pd.to_datetime(
        nueva_fila["fecha_hora"], format=FORMATO_FECHA_HORA
    )
    df = pd.concat([df, nueva_fila], ignore_index=True)
    guardar_citas(_df_a_citas(df))


def eliminar_cita(id_cita):
    df = _leer_citas_df()
    existe = (df["id_cita"] == id_cita).any()
    df = df[df["id_cita"] != id_cita].reset_index(drop=True)
    guardar_citas(_df_a_citas(df))
    return bool(existe)


def modificar_cita(id_cita, **cambios):
    df = _leer_citas_df()
    mascara = df["id_cita"] == id_cita
    if not mascara.any():
        return False
    for campo, valor in cambios.items():
        if campo not in COLUMNAS_CITAS:
            raise ValueError("Campo inválido para Cita:", campo)
        df.loc[mascara, campo] = valor
    guardar_citas(_df_a_citas(df))
    return True


def buscar_citas_por_mascota(id_mascota):
    df = _leer_citas_df()
    df_filtrado = df[df["id_mascota"] == id_mascota].sort_values("fecha_hora")
    return _df_a_citas(df_filtrado)
