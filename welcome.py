import tkinter as tk
from tkinter import ttk

class WelcomeScreen(tk.Toplevel):
    def __init__(self, master=None, next_callback=None):
        super().__init__(master)
        
        self.title("Algoritmos de Ordenamiento")
        self.WIDTH = 600
        self.HEIGHT = 400
        self.configure(bg="black")
        self.resizable(False, False)        
        self.center_window()
        
        if master:
            master.withdraw() 
            self.protocol("WM_DELETE_WINDOW", self.on_closing_master) 
        
        self.next_callback = next_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_widgets()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (self.WIDTH // 2)
        y = (screen_height // 2) - (self.HEIGHT // 2)

        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+{x}+{y}')
        
    def create_widgets(self):
        title_label = tk.Label(self, 
                            text="ALGORITMOS DE ORDENAMIENTO", 
                            bg="black", 
                            fg="white", 
                            font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(100, 10), sticky="s")

        group_label = tk.Label(self, 
                            text="Grupo 6", 
                            bg="black", 
                            fg="white", 
                            font=("Helvetica", 14, "italic")) 
        group_label.grid(row=1, column=0, pady=(0, 50), sticky="n")

        start_button = tk.Button(self,
                            text="➜",
                            command=self.go_to_next_screen,
                            font=("Helvetica", 18, "bold"),
                            bg="white",    
                            fg="black", 
                            activebackground="black",  
                            activeforeground="white",  
                            relief="flat",
                            bd=0,
                            cursor="hand2",
                            width=3)
        start_button.grid(row=2, column=0, pady=(50, 20), sticky="n")

    def go_to_next_screen(self):
        self.destroy() 
        if self.next_callback:
            self.next_callback() 

    def on_closing_master(self):
        if self.master:
            self.master.destroy()
        self.destroy()
