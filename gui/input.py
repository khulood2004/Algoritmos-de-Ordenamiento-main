import tkinter as tk
from tkinter import ttk, messagebox
import random 
from algoritmos.data_manager import DataManager 

class InputOptionsScreen(tk.Toplevel):
    def __init__(self, master=None, data_manager=None, next_callback=None):
        super().__init__(master)

        self.dm = data_manager if data_manager else DataManager()
        self.next_callback = next_callback

        self.title("Selección de Datos")
        self.WIDTH = 600
        self.HEIGHT = 400

        # ------ NUEVA PALETA DE COLORES ------
        self.bg_main = "#f6f1e7"        # beige suave
        self.bg_frame = "#e4efd9"       # verde pastel claro
        self.fg_text = "#2e3d2f"        # verde oscuro
        self.entry_bg = "#ffffff"
        self.btn_bg = "#b7d8a7"
        self.btn_bg_active = "#a3cc91"

        self.configure(bg=self.bg_main)
        self.resizable(False, False)
        self._center_window()
        
        if master:
            self.master = master
            self.protocol("WM_DELETE_WINDOW", self.on_closing_master) 
        
        self.create_widgets()

    def _center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.WIDTH // 2)
        y = (screen_height // 2) - (self.HEIGHT // 2)
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{x}+{y}')
        
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.bg_main)
        main_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # ---- TÍTULO ----
        title_label = tk.Label(
            main_frame,
            text="INGRESO DE DATOS", 
            bg=self.bg_main,
            fg=self.fg_text,
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=(0, 25))

        # ----------- SECCIÓN MANUAL -----------
        manual_frame = tk.LabelFrame(
            main_frame, 
            text="1. MANUAL", 
            fg=self.fg_text, 
            bg=self.bg_frame, 
            bd=2, 
            relief="solid",
            font=("Helvetica", 10, "bold")
        )
        manual_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(
            manual_frame,
            text="Ingrese los números separados por comas (ej: 5, 20, 15, 8)", 
            bg=self.bg_frame,
            fg=self.fg_text,
            font=("Helvetica", 9)
        ).pack(pady=5)
        
        self.manual_entry = tk.Entry(
            manual_frame,
            width=50,
            bg=self.entry_bg,
            fg=self.fg_text,
            insertbackground=self.fg_text,
            relief="flat"
        )
        self.manual_entry.pack(pady=5, ipady=3)
        
        ttk.Button(
            manual_frame,
            text="Procesar Manualmente", 
            command=self._process_manual_input,
            style='Minimal.TButton'
        ).pack(pady=10)

        # ----------- SECCIÓN ALEATORIA -----------
        random_frame = tk.LabelFrame(
            main_frame,
            text="2. ALEATORIO",
            fg=self.fg_text,
            bg=self.bg_frame,
            bd=2,
            relief="solid",
            font=("Helvetica", 10, "bold")
        )
        random_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(
            random_frame,
            text="Ingrese la CANTIDAD de datos a generar aleatoriamente (ej: 100, 1000)", 
            bg=self.bg_frame,
            fg=self.fg_text,
            font=("Helvetica", 9)
        ).pack(pady=5)
        
        self.random_entry = tk.Entry(
            random_frame,
            width=15,
            bg=self.entry_bg,
            fg=self.fg_text,
            insertbackground=self.fg_text,
            relief="flat"
        )
        self.random_entry.pack(pady=5, ipady=3)
        
        ttk.Button(
            random_frame,
            text="Generar Aleatoriamente", 
            command=self._process_random_input,
            style='Minimal.TButton'
        ).pack(pady=10)

        # ---- ESTILO DE BOTONES ----
        style = ttk.Style()
        style.configure(
            'Minimal.TButton', 
            font=('Helvetica', 10, 'bold'),
            foreground=self.fg_text,
            background=self.btn_bg,
            padding=6,
            relief='flat'
        )
        style.map('Minimal.TButton', background=[('active', self.btn_bg_active)])

    # ---------------- LÓGICA (NO SE TOCÓ NADA) ----------------
    def _process_manual_input(self):
        input_str = self.manual_entry.get().strip()
        
        if not input_str:
            messagebox.showerror("Error", "Por favor, ingrese los números separados por comas.")
            return

        try:
            self.dm.set_data_manual(input_str)
            messagebox.showinfo("Éxito", f"Datos cargados correctamente: {len(self.dm.base_data)} elementos.")
            self._advance_to_sorters()
        except ValueError as e:
            messagebox.showerror("Error de Datos", str(e))
            
    def _process_random_input(self):
        try:
            count = int(self.random_entry.get())
            if count <= 0:
                raise ValueError("La cantidad debe ser un número entero positivo.")
            
            self.dm.set_data_random(count)
            messagebox.showinfo("Éxito", f"Se generaron {count} datos aleatorios correctamente.")
            self._advance_to_sorters()
            
        except ValueError as e:
            messagebox.showerror("Error de Cantidad", str(e))

    def _advance_to_sorters(self):
        self.destroy() 
        if self.next_callback:
            self.next_callback() 

    def on_closing_master(self):
        if self.master:
            self.master.destroy()
        self.destroy()

