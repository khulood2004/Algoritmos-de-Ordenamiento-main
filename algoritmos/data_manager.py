# algoritmos/data_manager.py
import random
from typing import List

class DataManager:
    def __init__(self):
        self._base_data: List[int] = []

    @property
    def base_data(self) -> List[int]:
        return self._base_data

    def get_data_copy(self) -> List[int]:
        # Devuelve copia para ordenar sin modificar base_data
        return list(self._base_data)

    def set_data_manual(self, input_string: str):
        try:
            data_list = [int(item.strip()) for item in input_string.split(',') if item.strip()]
            if not data_list:
                raise ValueError("No se detectaron números válidos en el texto ingresado.")
            self._base_data = data_list
        except ValueError:
            raise ValueError("El ingreso contiene caracteres no válidos. Use solo números enteros separados por comas.")

    def set_data_random(self, count: int):
        if count <= 0:
            raise ValueError("La cantidad de datos debe ser mayor a cero.")
        # Para escalabilidad: generamos en rango [1, 1_000_000] por ejemplo
        self._base_data = [random.randint(1, 1_000_000) for _ in range(count)]
