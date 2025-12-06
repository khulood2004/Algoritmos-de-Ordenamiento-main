# gui/sorters.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import math

from algoritmos.data_manager import DataManager
from algoritmos.stats_manager import StatsManager
import algoritmos.sorts as sorts


# helper para mostrar muestras
def format_array_for_display(arr, head=10, tail=10):
    n = len(arr)
    if n <= head + tail + 2:
        return str(arr)
    head_part = arr[:head]
    tail_part = arr[-tail:]
    return f"{head_part} ... {tail_part}  (total: {n})"


class SortersScreen(tk.Toplevel):
    def __init__(self, master=None, data_manager: DataManager=None):
        super().__init__(master)
        self.title("Ordenamientos")
        self.geometry("900x700")
        self.configure(bg="#0b0b0b")
        self.resizable(True, True)

        self.dm = data_manager if data_manager else DataManager()
        self.stats = StatsManager()

        self.result_queue = queue.Queue()

        self._create_widgets()

    def _create_widgets(self):
        top_frame = tk.Frame(self, bg="#0b0b0b")
        top_frame.pack(fill="x", padx=12, pady=10)

        left = tk.Frame(top_frame, bg="#0b0b0b")
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(top_frame, bg="#0b0b0b")
        right.pack(side="right", fill="y")

        # Algoritmos disponibles
        tk.Label(right, text="Algoritmo", bg="#0b0b0b", fg="white").pack(pady=(0,5))
        self.alg_var = tk.StringVar(value="quicksort_iterative")
        algs = [
            ("Bubble (mejorado)", "bubble_improved"),
            ("Insertion", "insertion_sort"),
            ("Selection", "selection_sort"),
            ("Shell", "shell_sort"),
            ("Quicksort (iter)", "quicksort_iterative"),
            ("Quicksort (rec)", "quicksort_recursive"),
            ("Mergesort (iter)", "mergesort_iterative"),
            ("Mergesort (rec)", "mergesort_recursive"),
            ("Python sorted() (fast)", "python_sorted"),
        ]
        for text, val in algs:
            ttk.Radiobutton(right, text=text, variable=self.alg_var, value=val).pack(anchor="w", padx=4, pady=2)

        ttk.Button(right, text="Ejecutar", command=self._on_run).pack(pady=8, fill="x", padx=6)
        ttk.Button(right, text="Exportar estadísticas", command=self._export_stats).pack(pady=4, fill="x", padx=6)

        # Muestras de arreglo
        info_frame = tk.Frame(left, bg="#0b0b0b")
        info_frame.pack(fill="both", expand=False, pady=4)

        tk.Label(info_frame, text="Arreglo original (muestra):", bg="#0b0b0b", fg="white").grid(row=0, column=0, sticky="w")
        self.orig_text = tk.Text(info_frame, height=3, width=80, bg="#111", fg="white", wrap="none")
        self.orig_text.grid(row=1, column=0, padx=4, pady=2)

        tk.Label(info_frame, text="Arreglo ordenado (muestra):", bg="#0b0b0b", fg="white").grid(row=2, column=0, sticky="w")
        self.sorted_text = tk.Text(info_frame, height=3, width=80, bg="#111", fg="white", wrap="none")
        self.sorted_text.grid(row=3, column=0, padx=4, pady=2)

        self.time_label = tk.Label(info_frame, text="Tiempo: -- ms", bg="#0b0b0b", fg="white", font=("Helvetica", 12, "bold"))
        self.time_label.grid(row=4, column=0, sticky="w", pady=(6,0))

        # Tabla comparativa
        table_frame = tk.Frame(self, bg="#0b0b0b")
        table_frame.pack(fill="both", expand=True, padx=12, pady=6)

        self.tree = ttk.Treeview(table_frame, columns=("alg", "n", "ms", "ts"), show="headings", height=6)
        self.tree.heading("alg", text="Algoritmo")
        self.tree.heading("n", text="n")
        self.tree.heading("ms", text="ms")
        self.tree.heading("ts", text="timestamp")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _on_run(self):
        arr = self.dm.get_data_copy()
        if not arr:
            messagebox.showerror("Error", "No hay datos cargados.")
            return

        alg_key = self.alg_var.get()

        # Advertencia para arreglos grandes
        n = len(arr)
        if n > 200_000 and alg_key in ("quicksort_recursive", "mergesort_recursive", "insertion_sort", "selection_sort", "bubble_improved"):
            msg = (
                f"El algoritmo seleccionado puede ser muy lento o agotar recursión con n = {n}.\n"
                f"Recomiendo usar 'Python sorted()' o quicksort/merge iterativo.\n"
                f"¿Deseas continuar?"
            )
            if not messagebox.askyesno("Advertencia", msg):
                return

        thread = threading.Thread(target=self._run_sort_in_thread, args=(alg_key, arr), daemon=True)
        thread.start()

        self.time_label.config(text="Ejecutando...")

        self.after(100, self._check_result_queue)

    def _run_sort_in_thread(self, alg_key, arr):
        try:
            if alg_key == "python_sorted":
                start = __import__("time").perf_counter()
                sorted_arr = sorted(arr)
                elapsed = (__import__("time").perf_counter() - start) * 1000.0
            else:
                func = getattr(sorts, alg_key)
                sorted_arr, elapsed = func(arr)

            self.result_queue.put({
                'alg': alg_key,
                'n': len(arr),
                'ms': elapsed,
                'sorted': sorted_arr
            })

        except Exception as e:
            self.result_queue.put({'error': str(e)})

    def _check_result_queue(self):
        try:
            item = self.result_queue.get_nowait()
        except queue.Empty:
            self.after(100, self._check_result_queue)
            return

        if 'error' in item:
            messagebox.showerror("Error en ordenamiento", item['error'])
            self.time_label.config(text="Error")
            return

        alg = item['alg']
        n = item['n']
        ms = item['ms']
        sorted_arr = item['sorted']

        self.stats.add(alg, n, ms)

        self.orig_text.delete("1.0", "end")
        self.orig_text.insert("end", format_array_for_display(self.dm.base_data))

        self.sorted_text.delete("1.0", "end")
        self.sorted_text.insert("end", format_array_for_display(sorted_arr))

        self.time_label.config(text=f"Tiempo: {ms:.3f} ms  |  Alg: {alg}  |  n: {n}")

        from datetime import datetime
        ts = datetime.now().isoformat(timespec='seconds')
        self.tree.insert("", "end", values=(alg, n, f"{ms:.3f}", ts))

    def _export_stats(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            self.stats.export_csv(path)
            messagebox.showinfo("Exportado", f"Estadísticas exportadas a {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

