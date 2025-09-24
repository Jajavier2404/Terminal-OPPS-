"""
Gestor de Memoria (MemoryManager) para el sistema operativo simulado.

Implementa una estrategia de asignación de memoria contigua simple utilizando el algoritmo First-Fit.
También proporciona funcionalidades para liberar memoria, mostrar el mapa de memoria y defragmentar.
"""

from typing import List, Tuple, Optional

# Se utiliza una referencia hacia adelante (forward reference) para el type hint de 'SimProcess'.
# Esto evita un problema de dependencia circular, ya que scheduler.py importa tanto memory.py como process.py.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from process import SimProcess

class MemoryManager:
    """
    Gestiona un espacio de memoria simulado.
    
    Atributos:
        total (int): El tamaño total de la memoria simulada.
        free (List[Tuple[int, int]]): Una lista de tuplas que representan los bloques de memoria libre.
                                     Cada tupla contiene (dirección_inicio, tamaño).
        allocations (dict): Un diccionario que mapea PIDs de procesos a sus bloques de memoria asignados.
                            El formato es {pid: (dirección_inicio, tamaño)}.
    """
    def __init__(self, total_size: int):
        """Inicializa el MemoryManager con un tamaño de memoria total."""
        self.total = total_size
        # La memoria comienza como un único gran bloque libre.
        self.free: List[Tuple[int, int]] = [(0, total_size)]
        self.allocations = {}

    def alloc(self, pid: str, size: int) -> Optional[int]:
        """
        Intenta asignar un bloque de memoria de un tamaño (`size`) dado a un proceso (`pid`) usando First-Fit.
        
        First-Fit: Recorre la lista de bloques libres y elige el primero que sea lo suficientemente grande.
        
        Retorna:
            La dirección de inicio del bloque asignado, o None si no se encontró espacio.
        """
        if size <= 0:
            # Un proceso que no requiere memoria se le asigna una dirección simbólica 0 y tamaño 0.
            self.allocations[pid] = (0, 0)
            return 0

        # Recorrer la lista de bloques libres para encontrar el primero que se ajuste.
        for i, (start, sz) in enumerate(self.free):
            if sz >= size:
                addr = start
                self.allocations[pid] = (addr, size)
                
                # Si el bloque se ajusta exactamente, se elimina de la lista de libres.
                if sz == size:
                    self.free.pop(i)
                # Si el bloque es más grande, se reduce su tamaño.
                else:
                    self.free[i] = (start + size, sz - size)
                return addr
        # Si no se encuentra un bloque adecuado, se retorna None.
        return None

    def free_mem(self, pid: str) -> bool:
        """
        Libera la memoria asignada a un proceso (`pid`).
        
        El bloque liberado se añade de nuevo a la lista de bloques libres y se intenta fusionar
        con bloques libres adyacentes para reducir la fragmentación externa.
        
        Retorna:
            True si la memoria fue liberada exitosamente, False en caso contrario.
        """
        if pid not in self.allocations:
            return False
        
        addr, size = self.allocations.pop(pid)
        
        # Añadir el bloque liberado a la lista de libres y ordenarla por dirección.
        self.free.append((addr, size))
        self.free.sort(key=lambda x: x[0])
        
        # Fusionar bloques libres adyacentes.
        merged = []
        for s, sz in self.free:
            if not merged:
                merged.append([s, sz])
            else:
                last_s, last_sz = merged[-1]
                # Si el bloque actual comienza donde terminó el anterior, se fusionan.
                if last_s + last_sz == s:
                    merged[-1][1] = last_sz + sz
                else:
                    merged.append([s, sz])
        self.free = [(s, sz) for s, sz in merged]
        return True

    def mem_map(self):
        """
        Retorna una representación del estado actual de la memoria.
        Útil para que el shell muestre el mapa de memoria.
        """
        occupied = []
        for pid, (addr, size) in self.allocations.items():
            occupied.append((pid, addr, size))
        return {
            'total': self.total,
            'free': list(self.free),
            'allocations': occupied
        }

    def defrag(self, processes: List['SimProcess']):
        """
        Compacta la memoria moviendo todos los bloques asignados al principio.
        
        Esto elimina la fragmentación externa, consolidando todo el espacio libre en un
        único bloque contiguo al final de la memoria.
        Requiere actualizar las direcciones de memoria en los PCBs (SimProcess) correspondientes.
        """
        # Ordenar los bloques asignados por su dirección de memoria actual.
        sorted_allocations = sorted(self.allocations.items(), key=lambda item: item[1][0])
        
        new_allocations = {}
        current_address = 0
        
        # Reubicar cada bloque uno después del otro.
        for pid, (old_addr, size) in sorted_allocations:
            # Actualizar la dirección en el PCB del proceso.
            for p in processes:
                if p.pid == pid:
                    p.addr = current_address
                    break
            
            # Actualizar el mapa de asignaciones con la nueva dirección.
            new_allocations[pid] = (current_address, size)
            
            current_address += size
            
        self.allocations = new_allocations
        
        # Crear un único bloque libre con todo el espacio restante.
        self.free = [(current_address, self.total - current_address)]
