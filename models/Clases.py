class Mascota():
    def __init__(self, id_mascota : str, nombre : str, especie : str, raza : str, edad : int, sexo : str, peso : float, id_dueno : str):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.sexo = sexo
        self.peso = peso
        self.id_dueno = id_dueno
    def dict(self):
        return {
            "id_mascota": self.id_mascota,"nombre": self.nombre,"especie": self.especie,"raza": self.raza,"edad": self.edad,"sexo": self.sexo,
            "peso": self.peso,
            "id_dueno": self.id_dueno,
        }
class Cita():
    def __init__(self, id_cita: str, fecha_hora: str, motivo: str, estado: str, id_mascota: str, id_veterinario: str):
        self.id_cita = id_cita
        self.fecha_hora = fecha_hora 
        self.motivo = motivo
        self.estado = estado
        self.id_mascota = id_mascota
        self.id_veterinario = id_veterinario
 
    def to_dict(self, formato_fecha_hora):
        return {
            "id_cita": self.id_cita,"fecha_hora": self.fecha_hora.strftime(formato_fecha_hora),"motivo": self.motivo,"estado": self.estado,
            "id_mascota": self.id_mascota,"id_veterinario": self.id_veterinario,
        }    
