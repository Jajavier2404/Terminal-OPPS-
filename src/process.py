"""SimProcess - proceso simulado (sin hilos reales)"""
from typing import Optional
from dataclasses import dataclass

@dataclass
class SimProcess:
    pid: str
    cpu_units: int
    mem_req: int = 0
    state: str = 'READY'   # READY, RUNNING, BLOCKED, FINISHED
    addr: Optional[int] = None

    def run_one_unit(self):
        """Simula 1 unidad de CPU. Cambia el estado si termina."""
        if self.state == 'FINISHED':
            return
        if self.cpu_units <= 0:
            self.state = 'FINISHED'
            return
        # Simula trabajo consumiendo 1 unidad
        self.cpu_units -= 1
        if self.cpu_units <= 0:
            self.state = 'FINISHED'
