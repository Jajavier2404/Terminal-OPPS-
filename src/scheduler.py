"""Scheduler Round-Robin (simulado, sin hilos reales)."""
from collections import deque
from typing import List, Tuple, Optional
from process import SimProcess
import time

class Scheduler:
    def __init__(self, quantum: int = 2):
        self.quantum = quantum
        self.processes: List[SimProcess] = []
        self.timeline: List[Tuple[int, str]] = []  # (time_unit, pid)
        self._time = 0

    def create_process(self, pid: str, cpu_units: int, mem_req: int, memory_manager) -> Tuple[bool, Optional[str]]:
        # intentar reservar memoria primero (si se pide)
        addr = None
        if mem_req > 0:
            addr = memory_manager.alloc(pid, mem_req)
            if addr is None:
                return False, 'NO_MEMORY'
        p = SimProcess(pid=pid, cpu_units=cpu_units, mem_req=mem_req, state='READY', addr=addr)
        self.processes.append(p)
        return True, None

    def kill_process(self, pid: str, memory_manager) -> bool:
        for p in self.processes:
            if p.pid == pid:
                p.state = 'FINISHED'
                # liberar memoria si tenía
                memory_manager.free_mem(pid)
                return True
        return False

    def list_processes(self) -> List[dict]:
        return [
            {
                'pid': p.pid,
                'cpu_units': p.cpu_units,
                'state': p.state,
                'mem_req': p.mem_req,
                'addr': p.addr
            } for p in self.processes
        ]

    def run(self, verbose: bool = True, sleep_per_unit: float = 0.0):
        """Corre el scheduler en Round-Robin hasta que todos los procesos estén FINISHED."""
        q = deque(self.processes)
        # si no hay procesos, regresar
        if not q:
            if verbose:
                print("[scheduler] No hay procesos para ejecutar.")
            return
        while any(p.state != 'FINISHED' for p in q):
            p = q.popleft()
            if p.state == 'FINISHED':
                continue
            p.state = 'RUNNING'
            # ejecutar hasta quantum o hasta que termine
            for _ in range(self.quantum):
                if p.state == 'FINISHED':
                    break
                # ejecutar 1 unidad
                p.run_one_unit()
                self._time += 1
                self.timeline.append((self._time, p.pid))
                if verbose:
                    print(f"[t={self._time}] Ejecutando {p.pid} (restan {p.cpu_units})")
                if sleep_per_unit:
                    time.sleep(sleep_per_unit)
            if p.state != 'FINISHED':
                p.state = 'READY'
                q.append(p)
            else:
                if verbose:
                    print(f"[t={self._time}] Proceso {p.pid} ha terminado.")
        if verbose:
            print("[scheduler] Todos los procesos finalizaron.")

    def get_timeline(self):
        return list(self.timeline)
