import tkinter as tk
from core.sistema import SistemaVeterinaria
from gui.ventana_mascotas_duenos import VentanaMascotasDuenos

def main():
    root = tk.Tk()
    root.withdraw()  # ocultar ventana raíz
    sistema = SistemaVeterinaria()
    VentanaMascotasDuenos(root, sistema)
    root.mainloop()

if __name__ == "__main__":
    main()