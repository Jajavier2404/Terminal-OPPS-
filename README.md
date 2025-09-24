# OS Prototype (Simulación en Python)

Proyecto de prototipo para la asignatura — simulador simple de procesos, scheduler Round-Robin y Memory Manager (First-Fit).

## Contenido
- `src/process.py`  - definición de procesos simulados.
- `src/memory.py`   - MemoryManager (First-Fit).
- `src/scheduler.py`- Scheduler Round-Robin y utilidades.
- `src/shell.py`    - REPL sencillo para interactuar.
- `src/main.py`     - punto de entrada.
- `design.md`       - diseño y casos de prueba.

## Cómo ejecutar (rápido)
```bash
# desde la carpeta /mnt/data/os_prototype
python3 -m venv venv
source venv/bin/activate
python src/main.py
```

En el shell escribe `help` para ver comandos (newproc, ps, alloc, free, memmap, run, demo, exit).
