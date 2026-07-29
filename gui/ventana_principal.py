import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
from core.sistema import SistemaVeterinaria
from models.cita import Cita

CANVAS = "#eef2f7"
WINDOW = "#ffffff"
BORDER = "#d9dee6"
TITLEBAR = "#f1f4f9"
TITLEBAR_FG = "#4b5563"
MENUBAR = "#f6f8fb"
STATUSBAR = "#e2e6ee"
STATUSBAR_FG = "#4b5563"
THEAD = "#eef1f6"
ROW_ALT = "#fafbfd"
ROW_HOVER = "#e8effb"
ROW_SEL = "#2f66d9"
ROW_SEL_FG = "#ffffff"
TEXT = "#111827"
MUTED = "#6b7280"
PRIMARY = "#2563eb"
PRIMARY_HOVER = "#1d4ed8"
WARN = "#d97706"
WARN_HOVER = "#b45309"
DANGER = "#dc2626"
DANGER_HOVER = "#b91c1c"
GHOST = "#e5e7eb"
GHOST_HOVER = "#d1d5db"
GHOST_FG = "#111827"
DOT_RED = "#ef4444"
DOT_YELLOW = "#f5c451"
DOT_GREEN = "#4ade80"

FONT = ("Segoe UI", 10)
FONT_B = ("Segoe UI", 10, "bold")
FONT_H1 = ("Segoe UI", 16, "bold")
FONT_SM = ("Segoe UI", 9)


class FlatButton(tk.Label):
    def __init__(self, parent, text, bg, fg, hover_bg, command, padx=12, pady=6):
        super().__init__(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=FONT,
            padx=padx,
            pady=pady,
            cursor="hand2",
        )
        self._bg, self._hover = bg, hover_bg
        self._cmd = command
        self.bind("<Enter>", lambda _e: self.configure(bg=self._hover))
        self.bind("<Leave>", lambda _e: self.configure(bg=self._bg))
        self.bind("<Button-1>", lambda _e: self._cmd() if self._cmd else None)


class AppVeterinaria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Veterinaria ChillVet")
        self.geometry("1040x640")
        self.configure(bg=CANVAS)
        self.minsize(940, 560)

        self.sistema = SistemaVeterinaria()
        self.seleccion_id = None

        self._configurar_estilos_tabla()
        self._construir_ui()
        self.refrescar()

    def _configurar_estilos_tabla(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Vet.Treeview",
            background=WINDOW,
            fieldbackground=WINDOW,
            foreground=TEXT,
            rowheight=28,
            font=FONT,
            bordercolor=BORDER,
            borderwidth=0,
        )
        style.configure(
            "Vet.Treeview.Heading",
            background=THEAD,
            foreground=TEXT,
            font=FONT_B,
            relief="flat",
            padding=6,
        )
        style.map(
            "Vet.Treeview",
            background=[("selected", ROW_SEL)],
            foreground=[("selected", ROW_SEL_FG)],
        )
        style.layout("Vet.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    def _construir_ui(self):
        wrap = tk.Frame(self, bg=CANVAS)
        wrap.pack(fill="both", expand=True, padx=18, pady=18)

        window = tk.Frame(
            wrap, bg=WINDOW, highlightbackground=BORDER, highlightthickness=1, bd=0
        )
        window.pack(fill="both", expand=True)

        body = tk.Frame(window, bg=WINDOW)
        body.pack(fill="both", expand=True, padx=22, pady=18)

        tk.Label(body, text="Gestión de Citas", bg=WINDOW, fg=TEXT, font=FONT_H1).pack(
            anchor="w"
        )
        tk.Label(
            body,
            text="Busca, crea, edita y elimina citas de tus pacientes, chill.",
            bg=WINDOW,
            fg=MUTED,
            font=FONT,
        ).pack(anchor="w", pady=(0, 12))

        panel = tk.Frame(
            body, bg=WINDOW, highlightbackground=BORDER, highlightthickness=1
        )
        panel.pack(fill="x", pady=(0, 12))
        tk.Label(panel, text="Buscar por ID:", bg=WINDOW, fg=TEXT, font=FONT_B).pack(
            side="left", padx=(12, 8), pady=10
        )
        self.var_busqueda = tk.StringVar()
        entry = tk.Entry(
            panel,
            textvariable=self.var_busqueda,
            width=18,
            font=FONT,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=PRIMARY,
        )
        entry.pack(side="left", pady=10)
        entry.bind("<Return>", lambda _e: self.buscar())
        FlatButton(panel, "Buscar", PRIMARY, "white", PRIMARY_HOVER, self.buscar).pack(
            side="left", padx=8
        )
        FlatButton(
            panel, "Mostrar todas", GHOST, GHOST_FG, GHOST_HOVER, self.mostrar_todas
        ).pack(side="left", padx=(0, 12))

        acc = tk.Frame(body, bg=WINDOW)
        acc.pack(fill="x", pady=(0, 10))
        FlatButton(
            acc, "+ Nueva cita", PRIMARY, "white", PRIMARY_HOVER, self.abrir_nuevo
        ).pack(side="left")
        FlatButton(
            acc, "Editar seleccionada", WARN, "white", WARN_HOVER, self.editar_sel
        ).pack(side="left", padx=8)
        FlatButton(
            acc,
            "Eliminar seleccionada",
            DANGER,
            "white",
            DANGER_HOVER,
            self.eliminar_sel,
        ).pack(side="left")

        # tabla
        tabla_wrap = tk.Frame(
            body, bg=WINDOW, highlightbackground=BORDER, highlightthickness=1
        )
        tabla_wrap.pack(fill="both", expand=True)

        cols = ("id", "mascota", "dueno", "motivo", "fecha", "hora", "vet")
        self.tabla = ttk.Treeview(
            tabla_wrap,
            columns=cols,
            show="headings",
            selectmode="browse",
            style="Vet.Treeview",
        )
        headers = {
            "id": ("ID", 60),
            "mascota": ("Mascota", 130),
            "dueno": ("Dueño", 150),
            "motivo": ("Motivo", 220),
            "fecha": ("Fecha", 110),
            "hora": ("Hora", 80),
            "vet": ("Veterinario", 160),
        }
        for c, (txt, w) in headers.items():
            self.tabla.heading(c, text=txt)
            self.tabla.column(c, width=w, anchor="w")
        self.tabla.tag_configure("odd", background=WINDOW)
        self.tabla.tag_configure("even", background=ROW_ALT)

        sb = ttk.Scrollbar(tabla_wrap, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=sb.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self._on_select)
        self.tabla.bind("<Double-1>", lambda _e: self.editar_sel())

        tk.Frame(window, bg=BORDER, height=1).pack(fill="x")
        status = tk.Frame(window, bg=STATUSBAR)
        status.pack(fill="x")
        self.var_estado = tk.StringVar(value="Listo.")
        self.var_contador = tk.StringVar(value="")
        tk.Label(
            status,
            textvariable=self.var_estado,
            bg=STATUSBAR,
            fg=STATUSBAR_FG,
            font=FONT_SM,
            anchor="w",
        ).pack(side="left", padx=12, pady=4)
        tk.Label(
            status,
            textvariable=self.var_contador,
            bg=STATUSBAR,
            fg=STATUSBAR_FG,
            font=FONT_SM,
            anchor="e",
        ).pack(side="right", padx=12, pady=4)

    def refrescar(self, items=None):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        datos = self.sistema.listar_citas() if items is None else list(items)
        for idx, c in enumerate(datos):
            tag = "even" if idx % 2 else "odd"
            mascota = self.sistema.buscar_mascota(c.id_mascota)
            nombre_mascota = mascota.nombre if mascota else "Desconocida"
            dueno = self.sistema.buscar_dueno(mascota.id_dueno) if mascota else None
            nombre_dueno = dueno.nombre if dueno else "Desconocido"

            self.tabla.insert(
                "",
                "end",
                iid=str(c.id_cita),
                values=(
                    c.id_cita,
                    nombre_mascota,
                    nombre_dueno,
                    c.motivo,
                    c.fecha_hora.strftime("%Y-%m-%d"),
                    c.fecha_hora.strftime("%H:%M"),
                    c.id_veterinario,
                ),
                tags=(tag,),
            )
        sel_txt = f" · Seleccionada: #{self.seleccion_id}" if self.seleccion_id else ""
        self.var_contador.set(
            f"{len(datos)} mostrada(s) · Total: {len(self.sistema.listar_citas())}{sel_txt}"
        )

    def _on_select(self, _e=None):
        sel = self.tabla.selection()
        self.seleccion_id = sel[0] if sel else None
        self.refrescar_contador()

    def refrescar_contador(self):
        n = len(self.tabla.get_children())
        sel_txt = f" · Seleccionada: #{self.seleccion_id}" if self.seleccion_id else ""
        self.var_contador.set(
            f"{n} mostrada(s) · Total: {len(self.sistema.listar_citas())}{sel_txt}"
        )

    def buscar(self):
        q = self.var_busqueda.get().strip()
        if not q:
            self.mostrar_todas()
            return
        cita = self.sistema.gestor_citas.buscar_cita(q)
        if cita:
            self.refrescar(items=[cita])
            self.tabla.selection_set(str(q))
            self.var_estado.set(f"1 resultado para ID {q}.")
        else:
            self.refrescar(items=[])
            self.var_estado.set(f"Sin coincidencias para ID {q}.")

    def mostrar_todas(self):
        self.var_busqueda.set("")
        self.refrescar()
        self.var_estado.set("Mostrando todas las citas.")

    def editar_sel(self):
        if self.seleccion_id is None:
            self.var_estado.set("Selecciona una cita primero.")
            return
        cita = self.sistema.gestor_citas.buscar_cita(self.seleccion_id)
        if cita:
            self._formulario(cita)

    def eliminar_sel(self):
        if self.seleccion_id is None:
            self.var_estado.set("Selecciona una cita primero.")
            return
        if messagebox.askyesno("Eliminar", f"¿Eliminar la cita #{self.seleccion_id}?"):
            exito = self.sistema.eliminar_cita(self.seleccion_id)
            if exito:
                self.seleccion_id = None
                self.refrescar()
                self.var_estado.set("Cita eliminada.")
            else:
                self.var_estado.set("Error al eliminar la cita.")

    def abrir_nuevo(self):
        self._formulario(None)

    def _formulario(self, cita: Cita):
        top = tk.Toplevel(self)
        top.title("Nueva cita" if cita is None else f"Editar cita #{cita.id_cita}")
        top.configure(bg=WINDOW)
        top.geometry("460x420")
        top.transient(self)
        top.grab_set()
        top.resizable(False, False)

        tb = tk.Frame(top, bg=TITLEBAR)
        tb.pack(fill="x")
        tk.Label(
            tb,
            text=("Nueva cita" if cita is None else f"Editar cita #{cita.id_cita}"),
            bg=TITLEBAR,
            fg=TITLEBAR_FG,
            font=FONT_SM,
            padx=12,
            pady=8,
        ).pack(side="left")
        tk.Frame(top, bg=BORDER, height=1).pack(fill="x")

        cont = tk.Frame(top, bg=WINDOW, padx=20, pady=18)
        cont.pack(fill="both", expand=True)

        mascota_obj = self.sistema.buscar_mascota(cita.id_mascota) if cita else None
        dueno_obj = (
            self.sistema.buscar_dueno(mascota_obj.id_dueno) if mascota_obj else None
        )

        campos = [
            ("Mascota", "mascota", mascota_obj.nombre if mascota_obj else ""),
            ("Dueño", "dueno", dueno_obj.nombre if dueno_obj else ""),
            ("Motivo", "motivo", cita.motivo if cita else ""),
            (
                "Fecha (YYYY-MM-DD)",
                "fecha",
                cita.fecha_hora.strftime("%Y-%m-%d") if cita else "",
            ),
            ("Hora (HH:MM)", "hora", cita.fecha_hora.strftime("%H:%M") if cita else ""),
            ("Veterinario", "veterinario", cita.id_veterinario if cita else ""),
        ]
        vars_ = {}
        for i, (label, key, val) in enumerate(campos):
            tk.Label(cont, text=label, bg=WINDOW, fg=TEXT, font=FONT).grid(
                row=i, column=0, sticky="w", pady=6
            )
            v = tk.StringVar(value=val)
            vars_[key] = v
            e = tk.Entry(
                cont,
                textvariable=v,
                font=FONT,
                width=32,
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=PRIMARY,
            )
            e.grid(row=i, column=1, sticky="ew", padx=(10, 0), pady=6)
            if not cita:
                e.insert(0, "")
                e.configure(fg=TEXT)
        cont.columnconfigure(1, weight=1)

        tk.Frame(top, bg=BORDER, height=1).pack(fill="x")
        footer = tk.Frame(top, bg=MENUBAR)
        footer.pack(fill="x")
        botones = tk.Frame(footer, bg=MENUBAR)
        botones.pack(side="right", padx=14, pady=10)
        FlatButton(botones, "Cancelar", GHOST, GHOST_FG, GHOST_HOVER, top.destroy).pack(
            side="left", padx=(0, 6)
        )

        def guardar():
            datos = {k: v.get().strip() for k, v in vars_.items()}
            if not all(datos.values()):
                messagebox.showwarning(
                    "Campos", "Completa todos los campos.", parent=top
                )
                return
            try:
                dt_fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d")
                dt_hora = datetime.strptime(datos["hora"], "%H:%M")
                fecha_hora_completa = dt_fecha.replace(
                    hour=dt_hora.hour, minute=dt_hora.minute
                )
            except ValueError:
                messagebox.showwarning(
                    "Formato", "Fecha: YYYY-MM-DD · Hora: HH:MM", parent=top
                )
                return

            dueno = self.sistema.obtener_o_crear_dueno(datos["dueno"])
            mascota = self.sistema.obtener_o_crear_mascota(datos["mascota"], dueno)

            if cita is None:
                cid = str(uuid.uuid4())[:8]
                nueva_cita = Cita(
                    cid,
                    fecha_hora_completa,
                    datos["motivo"],
                    "AGENDADA",
                    mascota.id_mascota,
                    datos["veterinario"],
                )
                exito = self.sistema.agendar_cita(nueva_cita)
                if exito:
                    self.var_estado.set(f"Cita #{cid} creada.")
                else:
                    messagebox.showwarning(
                        "Error",
                        "No se pudo agendar la cita (conflicto de horario).",
                        parent=top,
                    )
                    return
            else:
                exito = self.sistema.modificar_cita(
                    cita.id_cita,
                    motivo=datos["motivo"],
                    fecha_hora=fecha_hora_completa,
                    id_veterinario=datos["veterinario"],
                )
                if exito:
                    self.var_estado.set(f"Cita #{cita.id_cita} actualizada.")
                else:
                    messagebox.showwarning("Error", "Error al actualizar.", parent=top)
                    return
            self.refrescar()
            top.destroy()

        FlatButton(botones, "Guardar", PRIMARY, "white", PRIMARY_HOVER, guardar).pack(
            side="left"
        )


if __name__ == "__main__":
    AppVeterinaria().mainloop()
