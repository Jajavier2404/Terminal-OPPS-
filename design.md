# Diseño - Prototipo OS (Resumen)

Componentes:
- Shell (REPL)
- Scheduler (Round-Robin)
- MemoryManager (First-Fit)
- SimProcess (clase que guarda pid, cpu_units, estado y dirección de memoria)

Diagrama:

Shell <--> Scheduler <--> Processes
                 |
                 v
            MemoryManager

API mínima:
- scheduler.create_process(pid, cpu_units, mem_req)
- scheduler.kill_process(pid)
- scheduler.list_processes()
- scheduler.run()
- memory.alloc(pid, size)
- memory.free(pid)
- memory.mem_map()

Casos de prueba (resumen):
- Caso A: P1(5U), P2(3U), P3(7U) quantum=2 -> revisar timeline
- Caso B: Memoria total=100, alloc(P1,30), alloc(P2,50), free(P1), alloc(P3,25) -> comprobar first-fit
- Caso C: Mem insuficiente -> alloc debe fallar y devolver None

Roles sugeridos:
- Persona A: scheduler + process + pruebas de CPU/timeline
- Persona B: memory manager + shell + casos de memoria

