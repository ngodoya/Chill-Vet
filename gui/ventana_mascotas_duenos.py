import tkinter as tk
from tkinter import ttk, messagebox

from core.sistema import SistemaVeterinaria
from models.clsDueno import Dueno
from models.clsMascota import Mascota


class VentanaMascotasDuenos(tk.Toplevel):
    def __init__(self, master, sistema: SistemaVeterinaria):
        super().__init__(master)
        self.sistema = sistema
        self.title("Gestión de Mascotas y Dueños")
        self.geometry("900x520")
        self.resizable(False, False)

        self._build_ui()
        self._refrescar_tablas()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_duenos = ttk.Frame(notebook)
        self.tab_mascotas = ttk.Frame(notebook)
        notebook.add(self.tab_duenos, text="Dueños")
        notebook.add(self.tab_mascotas, text="Mascotas")

        self._build_tab_duenos()
        self._build_tab_mascotas()

    # DUeños
    def _build_tab_duenos(self):
        form = ttk.LabelFrame(self.tab_duenos, text="Registrar dueño")
        form.pack(fill="x", padx=10, pady=10)

        self.dueno_id = tk.StringVar()
        self.dueno_nombre = tk.StringVar()
        self.dueno_tel = tk.StringVar()
        self.dueno_email = tk.StringVar()
        self.dueno_dir = tk.StringVar()

        fields = [
            ("ID", self.dueno_id),
            ("Nombre", self.dueno_nombre),
            ("Teléfono", self.dueno_tel),
            ("Email", self.dueno_email),
            ("Dirección", self.dueno_dir),
        ]
        for i, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=i * 2, padx=4, pady=6, sticky="w")
            ttk.Entry(form, textvariable=var, width=18).grid(row=0, column=i * 2 + 1, padx=4, pady=6)

        ttk.Button(form, text="Guardar dueño", command=self._guardar_dueno).grid(
            row=1, column=0, columnspan=10, pady=6
        )

        list_frame = ttk.LabelFrame(self.tab_duenos, text="Lista de dueños")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree_duenos = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "telefono", "email", "direccion"),
            show="headings",
            height=12,
        )
        for col, txt, w in [
            ("id", "ID", 90),
            ("nombre", "Nombre", 170),
            ("telefono", "Teléfono", 110),
            ("email", "Email", 200),
            ("direccion", "Dirección", 220),
        ]:
            self.tree_duenos.heading(col, text=txt)
            self.tree_duenos.column(col, width=w, anchor="center")
        self.tree_duenos.pack(fill="both", expand=True, padx=8, pady=8)

    def _guardar_dueno(self):
        if not self.dueno_id.get().strip() or not self.dueno_nombre.get().strip():
            messagebox.showwarning("Validación", "ID y Nombre del dueño son obligatorios.")
            return

        dueno = Dueno(
            id_persona=self.dueno_id.get(),
            nombre=self.dueno_nombre.get(),
            telefono=self.dueno_tel.get(),
            email=self.dueno_email.get(),
            direccion=self.dueno_dir.get(),
        )

        ok = self.sistema.crear_dueno(dueno)
        if not ok:
            messagebox.showerror("Error", "No se pudo crear dueño (ID duplicado).")
            return

        messagebox.showinfo("OK", "Dueño registrado.")
        self.dueno_id.set("")
        self.dueno_nombre.set("")
        self.dueno_tel.set("")
        self.dueno_email.set("")
        self.dueno_dir.set("")
        self._refrescar_duenos()

    # Mascotas
    def _build_tab_mascotas(self):
        form = ttk.LabelFrame(self.tab_mascotas, text="Registrar mascota")
        form.pack(fill="x", padx=10, pady=10)

        self.m_id = tk.StringVar()
        self.m_nombre = tk.StringVar()
        self.m_especie = tk.StringVar()
        self.m_raza = tk.StringVar()
        self.m_edad = tk.StringVar()
        self.m_sexo = tk.StringVar()
        self.m_peso = tk.StringVar()
        self.m_id_dueno = tk.StringVar()

        fields_row1 = [
            ("ID", self.m_id),
            ("Nombre", self.m_nombre),
            ("Especie", self.m_especie),
            ("Raza", self.m_raza),
        ]
        for i, (label, var) in enumerate(fields_row1):
            ttk.Label(form, text=label).grid(row=0, column=i * 2, padx=4, pady=6, sticky="w")
            ttk.Entry(form, textvariable=var, width=16).grid(row=0, column=i * 2 + 1, padx=4, pady=6)

        fields_row2 = [
            ("Edad", self.m_edad),
            ("Sexo", self.m_sexo),
            ("Peso", self.m_peso),
            ("ID Dueño", self.m_id_dueno),
        ]
        for i, (label, var) in enumerate(fields_row2):
            ttk.Label(form, text=label).grid(row=1, column=i * 2, padx=4, pady=6, sticky="w")
            ttk.Entry(form, textvariable=var, width=16).grid(row=1, column=i * 2 + 1, padx=4, pady=6)

        ttk.Button(form, text="Guardar mascota", command=self._guardar_mascota).grid(
            row=2, column=0, columnspan=8, pady=8
        )

        list_frame = ttk.LabelFrame(self.tab_mascotas, text="Lista de mascotas")
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree_mascotas = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "especie", "raza", "edad", "sexo", "peso", "id_dueno"),
            show="headings",
            height=12,
        )
        cols = [
            ("id", "ID", 70),
            ("nombre", "Nombre", 130),
            ("especie", "Especie", 90),
            ("raza", "Raza", 110),
            ("edad", "Edad", 60),
            ("sexo", "Sexo", 70),
            ("peso", "Peso", 70),
            ("id_dueno", "ID Dueño", 90),
        ]
        for col, txt, w in cols:
            self.tree_mascotas.heading(col, text=txt)
            self.tree_mascotas.column(col, width=w, anchor="center")
        self.tree_mascotas.pack(fill="both", expand=True, padx=8, pady=8)

    def _guardar_mascota(self):
        try:
            edad = int(self.m_edad.get())
            peso = float(self.m_peso.get())
        except ValueError:
            messagebox.showwarning("Validación", "Edad debe ser entero y peso numérico.")
            return

        if not self.m_id.get().strip() or not self.m_nombre.get().strip():
            messagebox.showwarning("Validación", "ID y Nombre de la mascota son obligatorios.")
            return

        mascota = Mascota(
            id_mascota=self.m_id.get(),
            nombre=self.m_nombre.get(),
            especie=self.m_especie.get(),
            raza=self.m_raza.get(),
            edad=edad,
            sexo=self.m_sexo.get(),
            peso=peso,
            id_dueno=self.m_id_dueno.get(),
        )

        ok = self.sistema.crear_mascota(mascota)
        if not ok:
            messagebox.showerror(
                "Error",
                "No se pudo crear mascota (ID duplicado o ID de dueño inexistente)."
            )
            return

        messagebox.showinfo("OK", "Mascota registrada.")
        self.m_id.set("")
        self.m_nombre.set("")
        self.m_especie.set("")
        self.m_raza.set("")
        self.m_edad.set("")
        self.m_sexo.set("")
        self.m_peso.set("")
        self.m_id_dueno.set("")
        self._refrescar_mascotas()

    # Refresh
    def _refrescar_tablas(self):
        self._refrescar_duenos()
        self._refrescar_mascotas()

    def _refrescar_duenos(self):
        for item in self.tree_duenos.get_children():
            self.tree_duenos.delete(item)

        for d in self.sistema.listar_duenos():
            self.tree_duenos.insert("", "end", values=(d.id_persona, d.nombre, d.telefono, d.email, d.direccion))

    def _refrescar_mascotas(self):
        for item in self.tree_mascotas.get_children():
            self.tree_mascotas.delete(item)

        for m in self.sistema.listar_mascotas():
            self.tree_mascotas.insert(
                "", "end",
                values=(m.id_mascota, m.nombre, m.especie, m.raza, m.edad, m.sexo, m.peso, m.id_dueno)
            )