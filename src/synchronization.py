"""
Primitivas de Sincronización para el Sistema Operativo Simulado.

Este archivo define las clases `Mutex` y `LockManager`, que proporcionan una funcionalidad
de exclusión mutua básica para gestionar el acceso a recursos compartidos entre procesos.
"""

from typing import Dict, Optional, Deque
from collections import deque
from process import SimProcess

class Mutex:
    """
    Representa un Mutex (Mutual Exclusion) o cerrojo simple.
    
    Un mutex puede ser adquirido por un solo proceso a la vez. Si otros procesos intentan
    adquirirlo mientras está bloqueado, se encolan en una cola de espera.
    
    Atributos:
        resource_id (str): El identificador del recurso que este mutex protege.
        locked_by (Optional[str]): El PID del proceso que actualmente posee el cerrojo. None si está libre.
        waiting_queue (Deque[SimProcess]): Una cola de procesos que están esperando para adquirir el cerrojo.
    """
    def __init__(self, resource_id: str):
        """Inicializa un Mutex para un recurso específico."""
        self.resource_id = resource_id
        self.locked_by = None
        self.waiting_queue = deque()

class LockManager:
    """
    Gestiona todos los mutex del sistema.
    
    Actúa como una factoría y un registro central para todos los cerrojos, 
    evitando la necesidad de instanciar mutex manualmente en otras partes del código.
    """
    def __init__(self):
        """Inicializa el LockManager."""
        # Un diccionario para almacenar todos los mutex, usando el ID del recurso como clave.
        self.mutexes: Dict[str, Mutex] = {}

    def get_mutex(self, resource_id: str) -> Mutex:
        """Obtiene (o crea si no existe) un mutex para un ID de recurso dado."""
        if resource_id not in self.mutexes:
            self.mutexes[resource_id] = Mutex(resource_id)
        return self.mutexes[resource_id]

    def lock(self, pid: str, resource_id: str, process: SimProcess) -> bool:
        """
        Intenta adquirir un cerrojo para un proceso.
        
        Si el cerrojo está libre, el proceso lo adquiere inmediatamente.
        Si está ocupado, el proceso se añade a la cola de espera del mutex.
        
        Retorna:
            True si el cerrojo fue adquirido, False si el proceso fue encolado para esperar.
        """
        mutex = self.get_mutex(resource_id)
        
        # Si el cerrojo no está bloqueado, lo adquiere el proceso actual.
        if not mutex.locked_by:
            mutex.locked_by = pid
            return True
        # Si el cerrojo está bloqueado, se añade el proceso a la cola de espera (si no está ya).
        else:
            if pid not in [p.pid for p in mutex.waiting_queue]:
                mutex.waiting_queue.append(process)
            return False

    def unlock(self, pid: str, resource_id: str) -> Optional[SimProcess]:
        """
        Libera un cerrojo que posee un proceso.
        
        Si hay procesos esperando en la cola, el primero de ellos adquiere el cerrojo
        y es devuelto para que el planificador pueda cambiar su estado a READY.
        
        Retorna:
            El siguiente proceso en la cola que ha sido desbloqueado, o None si no había nadie esperando.
        """
        mutex = self.get_mutex(resource_id)
        
        # Solo el proceso que posee el cerrojo puede liberarlo.
        if mutex.locked_by == pid:
            # Si hay procesos esperando, el siguiente en la cola adquiere el cerrojo.
            if mutex.waiting_queue:
                next_process = mutex.waiting_queue.popleft()
                mutex.locked_by = next_process.pid
                return next_process
            # Si no hay nadie esperando, el cerrojo simplemente se marca como libre.
            else:
                mutex.locked_by = None
        return None