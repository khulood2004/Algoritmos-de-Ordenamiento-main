# algoritmos/stats_manager.py
import csv
from typing import List, Dict

class StatsManager:
    def __init__(self):
        self.records: List[Dict] = []  # lista de dicts: {'alg': 'quicksort', 'n': 1000, 'ms': 12.3, 'timestamp': ...}

    def add(self, alg: str, n: int, ms: float):
        from datetime import datetime
        self.records.append({
            'alg': alg,
            'n': n,
            'ms': ms,
            'timestamp': datetime.now().isoformat()
        })

    def to_list(self):
        return list(self.records)

    def export_csv(self, path: str):
        if not self.records:
            return
        keys = self.records[0].keys()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.records)
