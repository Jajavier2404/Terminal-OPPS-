from scheduler import Scheduler
from memory import MemoryManager

def help_text():
    return """Comandos disponibles:
    - newproc <pid> <cpu_units> <mem_req>   : crea proceso (mem_req puede ser 0)
    - ps                                    : lista procesos
    - kill <pid>                            : mata proceso y libera memoria
    - alloc <pid> <size>                    : asigna memoria a pid (si no la tiene)
    - free <pid>                            : libera memoria del pid
    - memmap                                : muestra mapa de memoria
    - run                                   : ejecuta el scheduler (RR) hasta terminar
    - demo                                  : corre demo automática (caso de prueba)
    - help                                  : muestra esta ayuda
    - exit                                  : sale del shell
    """

from rich.console import Console
from rich.text import Text

console = Console()

ascii_art = """
 ███             ███████    ███████████  ███████████   █████████ 
▒▒▒███         ███▒▒▒▒▒███ ▒▒███▒▒▒▒▒███▒▒███▒▒▒▒▒███ ███▒▒▒▒▒███
  ▒▒▒███      ███     ▒▒███ ▒███    ▒███ ▒███    ▒███▒███    ▒▒▒ 
    ▒▒▒███   ▒███      ▒███ ▒██████████  ▒██████████ ▒▒█████████ 
     ███▒    ▒███      ▒███ ▒███▒▒▒▒▒▒   ▒███▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒███
   ███▒      ▒▒███     ███  ▒███         ▒███         ███    ▒███
 ███▒         ▒▒▒███████▒   █████        █████       ▒▒█████████ 
▒▒▒             ▒▒▒▒▒▒▒    ▒▒▒▒▒        ▒▒▒▒▒         ▒▒▒▒▒▒▒▒▒  

"""

def print_horizontal_gradient(ascii_art, start_color=(0, 255, 0), end_color=(0, 255, 255)):
    lines = ascii_art.splitlines()
    for line in lines:
        gradient = Text()
        length = len(line)
        for i, char in enumerate(line):
            if char.strip() == "":  
                gradient.append(char)  # espacios en blanco sin color
                continue

            # interpolación horizontal (verde -> cyan)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / length))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / length))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / length))

            gradient.append(char, style=f"rgb({r},{g},{b})")

        console.print(gradient)

def run_shell(scheduler: Scheduler, memory: MemoryManager):
    print_horizontal_gradient(ascii_art)
    print(">>> Escribe 'help' para conocer los comandos...")
    while True:
        try:
            line = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nSaliendo...')
            break

        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == 'help':
            print(help_text())
        elif cmd == 'newproc':
            if len(args) < 3:
                print('Uso: newproc <pid> <cpu_units> <mem_req>')
                continue
            pid, cpu_s, mem_s = args[0], args[1], args[2]
            try:
                cpu = int(cpu_s); mem = int(mem_s)
            except ValueError:
                print('cpu_units y mem_req deben ser enteros')
                continue
            ok, err = scheduler.create_process(pid, cpu, mem, memory)
            if not ok:
                print(f'Error creando proceso: {err}')
            else:
                print(f'Proceso {pid} creado (cpu={cpu}, mem={mem})')
        elif cmd == 'ps':
            rows = scheduler.list_processes()
            if not rows:
                print('No hay procesos.')
            else:
                for r in rows:
                    print(r)
        elif cmd == 'kill':
            if len(args) < 1:
                print('Uso: kill <pid>')
                continue
            pid = args[0]
            ok = scheduler.kill_process(pid, memory)
            print('ok' if ok else 'pid no encontrado')
        elif cmd == 'alloc':
            if len(args) < 2:
                print('Uso: alloc <pid> <size>')
                continue
            pid, sz_s = args[0], args[1]
            try:
                sz = int(sz_s)
            except ValueError:
                print('size debe ser entero')
                continue
            addr = memory.alloc(pid, sz)
            if addr is None:
                print('alloc fallo: memoria insuficiente')
            else:
                for p in scheduler.processes:
                    if p.pid == pid:
                        p.addr = addr
                        p.mem_req = sz
                print(f'alloc ok: pid={pid} addr={addr}')
        elif cmd == 'free':
            if len(args) < 1:
                print('Uso: free <pid>')
                continue
            pid = args[0]
            ok = memory.free_mem(pid)
            if ok:
                for p in scheduler.processes:
                    if p.pid == pid:
                        p.addr = None
                        p.mem_req = 0
                print('free ok')
            else:
                print('free fallo: pid no encontrado o sin memoria')
        elif cmd == 'memmap':
            mm = memory.mem_map()
            print('TOTAL:', mm['total'])
            print('FREE:', mm['free'])
            print('ALLOC:', mm['allocations'])
        elif cmd == 'run':
            scheduler.run(verbose=True, sleep_per_unit=0.0)
            print('Timeline:', scheduler.get_timeline())
        elif cmd == 'demo':
            print('Creando demo: P1(5U,30), P2(3U,50), P3(7U,20)')
            scheduler.create_process('P1', 5, 30, memory)
            scheduler.create_process('P2', 3, 50, memory)
            scheduler.create_process('P3', 7, 20, memory)
            print('Mapa memoria antes run:')
            print(memory.mem_map())
            scheduler.run(verbose=True, sleep_per_unit=0.0)
            print('Mapa memoria despues run:')
            print(memory.mem_map())
            print('Timeline:', scheduler.get_timeline())
        elif cmd == 'exit':
            print('Saliendo...')
            break
        else:
            print('Comando no reconocido. Escribe help.')
