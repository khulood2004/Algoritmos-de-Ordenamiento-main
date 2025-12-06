
import tkinter as tk
from gui.welcome import WelcomeScreen
from gui.input import InputOptionsScreen
from gui.sorters import SortersScreen
from algoritmos.data_manager import DataManager

class AppController:
    def __init__(self, master):
        self.master = master
        self.dm = DataManager()
        self.master.withdraw()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        WelcomeScreen(self.master, next_callback=self.show_input_screen)

    def show_input_screen(self, master=None, data_manager=None):
        InputOptionsScreen(
            master if master else self.master,
            data_manager=self.dm,
            next_callback=self.show_sorters_screen
        )

    def show_sorters_screen(self, master=None, data_manager=None):
        SortersScreen(
            master if master else self.master,
            data_manager=self.dm
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = AppController(root)
    root.mainloop()
