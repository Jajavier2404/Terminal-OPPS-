"""
Entrada principal para el Simulador de Sistema Operativo.

Este script inicializa todos los componentes clave del sistema operativo simulado:
- Gestor de Memoria (MemoryManager)
- Planificador de Procesos (Scheduler)
- Sistema de Archivos (FileSystem)

Y luego lanza el shell interactivo para que el usuario pueda interactuar con el sistema.
"""

# Importación de los componentes principales del sistema operativo simulado.
from memory import MemoryManager
from scheduler import Scheduler
from shell import run_shell
from filesystem import FileSystem

def main():
    """Función principal que configura e inicia el simulador."""
    # Inicializa el gestor de memoria con un tamaño total de 100 unidades.
    mm = MemoryManager(total_size=100)
    
    # Inicializa el planificador Round-Robin con un quantum de 2 unidades de tiempo.
    sched = Scheduler(quantum=2)
    
    # Inicializa el sistema de archivos. Cargará el estado desde 'fs_state.json' si existe.
    fs = FileSystem()
    
    # Lanza el shell interactivo, pasando los componentes del SO para su manipulación.
    run_shell(sched, mm, fs)

# Punto de entrada estándar de Python: asegura que main() se ejecute solo cuando el script es ejecutado directamente.
if __name__ == '__main__':
    main()