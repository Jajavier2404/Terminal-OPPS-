"""Punto de entrada: crea MemoryManager y Scheduler y lanza shell."""
from memory import MemoryManager
from scheduler import Scheduler
from shell import run_shell

def main():
    mm = MemoryManager(total_size=100)
    sched = Scheduler(quantum=2)
    run_shell(sched, mm)

if __name__ == '__main__':
    main()
