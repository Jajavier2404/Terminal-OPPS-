"""
Planificador de Procesos (Scheduler) para el Sistema Operativo Simulado.

Implementa un planificador Round-Robin que gestiona el ciclo de vida de los procesos.
También se integra con el LockManager para manejar la sincronización y el bloqueo de procesos.
"""

from collections import deque
from typing import List, Tuple, Optional
from process import SimProcess
from synchronization import LockManager
import time

class Scheduler:
    """
    Implementa un planificador Round-Robin.
    
    Atributos:
        quantum (int): El número de unidades de tiempo que cada proceso puede ejecutar antes de ser interrumpido.
        processes (List[SimProcess]): La lista de todos los procesos en el sistema (PCB table).
        timeline (List[Tuple[int, str]]): Un registro histórico de qué proceso se ejecutó en cada unidad de tiempo.
        _time (int): El reloj interno del sistema (tiempo simulado).
        lock_manager (LockManager): El gestor de cerrojos para la sincronización.
    """
    def __init__(self, quantum: int = 2):
        """Inicializa el planificador con un quantum dado."""
        self.quantum = quantum
        self.processes = []
        self.timeline = []
        self._time = 0
        self.lock_manager = LockManager()

    def create_process(self, pid: str, cpu_units: int, mem_req: int, memory_manager) -> Tuple[bool, Optional[str]]:
        """Crea un nuevo proceso, asignándole memoria si es necesario."""
        # Intenta asignar memoria antes de crear el proceso.
        addr = None
        if mem_req > 0:
            addr = memory_manager.alloc(pid, mem_req)
            # Si la asignación de memoria falla, el proceso no se puede crear.
            if addr is None:
                return False, 'NO_MEMORY'
        
        p = SimProcess(pid=pid, cpu_units=cpu_units, mem_req=mem_req, state='READY', addr=addr)
        self.processes.append(p)
        return True, None

    def kill_process(self, pid: str, memory_manager) -> bool:
        """Marca un proceso como FINISHED y libera su memoria."""
        for p in self.processes:
            if p.pid == pid:
                p.state = 'FINISHED'
                # Es crucial liberar la memoria para que otros procesos puedan usarla.
                memory_manager.free_mem(pid)
                return True
        return False

    def list_processes(self) -> List[dict]:
        """Retorna una lista con el estado de todos los procesos."""
        return [
            {
                'pid': p.pid,
                'cpu_units': p.cpu_units,
                'state': p.state,
                'mem_req': p.mem_req,
                'addr': p.addr
            } for p in self.processes
        ]

    def lock(self, pid: str, resource_id: str) -> str:
        """Maneja una solicitud de un proceso para adquirir un cerrojo."""
        process = next((p for p in self.processes if p.pid == pid), None)
        if not process:
            return f"Error: Proceso '{pid}' no encontrado."

        # Intenta adquirir el cerrojo a través del LockManager.
        if self.lock_manager.lock(pid, resource_id, process):
            return f"Proceso '{pid}' adquirió el cerrojo para '{resource_id}'."
        # Si no se puede adquirir, el proceso pasa a estado BLOCKED.
        else:
            process.state = 'BLOCKED'
            return f"Proceso '{pid}' bloqueado esperando por '{resource_id}'."

    def unlock(self, pid: str, resource_id: str) -> str:
        """Maneja una solicitud de un proceso para liberar un cerrojo."""
        # Intenta liberar el cerrojo.
        unblocked_process = self.lock_manager.unlock(pid, resource_id)
        
        # Si al liberar el cerrojo otro proceso estaba esperando, se desbloquea.
        if unblocked_process:
            unblocked_process.state = 'READY'
            return f"Proceso '{pid}' liberó el cerrojo para '{resource_id}'. Proceso '{unblocked_process.pid}' ha sido desbloqueado."
        else:
            # Verifica si el cerrojo fue liberado correctamente aunque nadie esperara.
            mutex = self.lock_manager.get_mutex(resource_id)
            if not mutex.locked_by:
                 return f"Proceso '{pid}' liberó el cerrojo para '{resource_id}'. No había procesos en espera."
            # Si el cerrojo sigue bloqueado, significa que el proceso no era el dueño.
            else:
                 return f"Error: El proceso '{pid}' no posee el cerrojo para '{resource_id}'."

    def run(self, verbose: bool = True, sleep_per_unit: float = 0.0):
        """Ejecuta un ciclo de planificación Round-Robin sobre los procesos en estado READY."""
        # La cola de listos solo contiene procesos que pueden ejecutarse.
        ready_queue = deque([p for p in self.processes if p.state == 'READY'])

        if not ready_queue:
            if verbose:
                print("[scheduler] No hay procesos listos para ejecutar.")
            return

        temp_timeline = []
        # El ciclo se ejecuta mientras haya procesos en la cola de listos.
        while ready_queue:
            process = ready_queue.popleft()
            
            process.state = 'RUNNING'
            
            # Ejecutar el proceso por la duración del quantum o hasta que termine.
            for _ in range(self.quantum):
                if process.state == 'FINISHED':
                    break
                process.run_one_unit()
                self._time += 1
                temp_timeline.append((self._time, process.pid))
                if verbose:
                    print(f"[t={self._time}] Ejecutando {process.pid} (restan {process.cpu_units})")
                if sleep_per_unit:
                    time.sleep(sleep_per_unit)

            # Si el proceso no ha terminado, vuelve al estado READY.
            if process.state != 'FINISHED':
                process.state = 'READY'
            else:
                if verbose:
                    print(f"[t={self._time}] Proceso {process.pid} ha terminado.")
        
        self.timeline.extend(temp_timeline)
        if verbose:
            print("[scheduler] Ciclo de planificación completado.")

    def get_timeline(self):
        """Retorna el timeline histórico de la ejecución."""
        return list(self.timeline)
