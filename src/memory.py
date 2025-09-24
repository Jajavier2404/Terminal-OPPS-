"""MemoryManager simple - First-Fit"""
from typing import List, Tuple, Optional

class MemoryManager:
    def __init__(self, total_size: int):
        self.total = total_size
        # free list: list of (start, size)
        self.free: List[Tuple[int,int]] = [(0, total_size)]
        # allocations: pid -> (start,size)
        self.allocations = {}  

    def alloc(self, pid: str, size: int) -> Optional[int]:
        """Intenta asignar 'size' bytes al proceso pid.
        Devuelve la dirección (start) o None si no hay espacio contiguo."""
        if size <= 0:
            # tamaño 0 -> asignar dirección 0 simbólica
            self.allocations[pid] = (0, 0)
            return 0
        for i, (start, sz) in enumerate(self.free):
            if sz >= size:
                addr = start
                self.allocations[pid] = (addr, size)
                if sz == size:
                    # exact fit: eliminar bloque libre
                    self.free.pop(i)
                else:
                    # reducir bloque libre
                    self.free[i] = (start + size, sz - size)
                return addr
        return None

    def free_mem(self, pid: str) -> bool:
        """Libera la memoria asignada al pid. Devuelve True si se liberó."""
        if pid not in self.allocations:
            return False
        addr, size = self.allocations.pop(pid)
        # añadir bloque libre y hacer merge
        self.free.append((addr, size))
        self.free.sort(key=lambda x: x[0])
        # merge adyacentes
        merged = []
        for s, sz in self.free:
            if not merged:
                merged.append([s, sz])
            else:
                last_s, last_sz = merged[-1]
                if last_s + last_sz == s:
                    merged[-1][1] = last_sz + sz
                else:
                    merged.append([s, sz])
        self.free = [(s, sz) for s, sz in merged]
        return True

    def mem_map(self):
        """Retorna una representación simple del mapa de memoria (ocupado + libre)."""
        occupied = []
        for pid, (addr, size) in self.allocations.items():
            occupied.append((pid, addr, size))
        return {
            'total': self.total,
            'free': list(self.free),
            'allocations': occupied
        }
