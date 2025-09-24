"""
Define la estructura de un proceso simulado (SimProcess).

Este archivo contiene la clase de datos `SimProcess`, que actúa como el Bloque de Control de Proceso (PCB) 
en nuestra simulación. Almacena toda la información esencial sobre un proceso.
"""

from typing import Optional
from dataclasses import dataclass

@dataclass
class SimProcess:
    """
    Representa un proceso simulado con sus atributos principales.
    
    Utilizamos un dataclass para una definición concisa y clara de la estructura de datos.
    """
    # Identificador único del proceso.
    pid: str
    
    # Unidades de CPU requeridas para que el proceso complete su "trabajo".
    cpu_units: int
    
    # Cantidad de memoria solicitada por el proceso.
    mem_req: int = 0
    
    # Estado actual del proceso en su ciclo de vida. Puede ser:
    # - READY: Listo para ser ejecutado por el planificador.
    # - RUNNING: Actualmente en ejecución.
    # - BLOCKED: Esperando por un recurso (ej. un mutex).
    # - FINISHED: Ha completado su ejecución.
    state: str = 'READY'
    
    # Dirección de inicio de la memoria asignada por el MemoryManager. None si no tiene memoria asignada.
    addr: Optional[int] = None

    def run_one_unit(self):
        """
        Simula la ejecución de una unidad de trabajo de CPU.
        
        Decrementa las unidades de CPU restantes y actualiza el estado a FINISHED si el trabajo se completa.
        Esto es llamado por el Scheduler durante el ciclo de planificación.
        """
        # Si el proceso ya terminó, no hacer nada.
        if self.state == 'FINISHED':
            return
            
        # Si el proceso no tiene unidades de CPU restantes, marcarlo como terminado.
        if self.cpu_units <= 0:
            self.state = 'FINISHED'
            return
            
        # Simula el "trabajo" consumiendo una unidad de CPU.
        self.cpu_units -= 1
        
        # Si después de decrementar, las unidades de CPU llegan a cero, el proceso ha terminado.
        if self.cpu_units <= 0:
            self.state = 'FINISHED'