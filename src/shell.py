#El Shell Interactivo (REPL) para el Sistema Operativo Simulado.

#Este módulo proporciona la interfaz de usuario principal para interactuar con el simulador.
#Utiliza la biblioteca `rich` para una presentación de texto enriquecida y amigable.



from scheduler import Scheduler
from memory import MemoryManager
from filesystem import FileSystem
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel

# Instancia global de la consola de rich para una salida estilizada.
console = Console()

# ===============================
# ASCII art con gradiente
# ===============================
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
    """Imprime el ASCII art con un gradiente de color horizontal."""
    lines = ascii_art.splitlines()
    for line in lines:
        gradient = Text()
        length = len(line)
        for i, char in enumerate(line):
            if char.strip() == "":
                gradient.append(char)
                continue

            # Interpola linealmente entre el color de inicio y el de fin.
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / length))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / length))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / length))

            gradient.append(char, style=f"rgb({r},{g},{b})")

        console.print(gradient)

# ===============================
# HELP en formato tabla
# ===============================
def help_text():
    """Genera y retorna un panel de ayuda con una tabla de comandos."""
    print("\n")
    table = Table(title="Comandos disponibles", show_header=True, header_style="bold cyan")
    table.add_column("Comando", style="bold green")
    table.add_column("Descripción", style="white")

    # Comandos de Procesos y Planificador
    table.add_row("newproc <pid> <cpu> <mem>", "Crea un nuevo proceso")
    table.add_row("ps", "Lista los procesos y su estado")
    table.add_row("kill <pid>", "Termina un proceso")
    table.add_row("run", "Ejecuta el planificador Round-Robin")

    # Comandos de Sincronización
    table.add_row("lock <pid> <res>", "Un proceso adquiere un cerrojo (mutex)")
    table.add_row("unlock <pid> <res>", "Un proceso libera un cerrojo")

    # Comandos de Memoria
    table.add_row("alloc <pid> <size>", "Asigna memoria a un proceso")
    table.add_row("free <pid>", "Libera la memoria de un proceso")
    table.add_row("memmap", "Muestra el mapa de memoria actual")
    table.add_row("defrag", "Compacta la memoria para unir bloques libres")

    # Comandos de Sistema de Archivos
    table.add_row("ls", "Lista el contenido del directorio actual")
    table.add_row("mkdir <dirname>", "Crea un nuevo directorio")
    table.add_row("touch <filename>", "Crea un nuevo archivo vacío")
    table.add_row("write <file> <content>", "Escribe contenido en un archivo")
    table.add_row("cat <file>", "Muestra el contenido de un archivo")

    # Comandos Generales
    table.add_row("demo", "Ejecuta un escenario de demostración")
    table.add_row("help", "Muestra esta ayuda")
    table.add_row("exit", "Sale del simulador")

    return Panel.fit(table, border_style="cyan", title="Ayuda", title_align="left")

# ===============================
# SHELL PRINCIPAL (REPL)
# ===============================
def run_shell(scheduler: Scheduler, memory: MemoryManager, fs: FileSystem):
    """El bucle principal de lectura, evaluación e impresión (REPL) del shell."""
    print_horizontal_gradient(ascii_art)
    console.print("[bold cyan]>>> Escribe 'help' para conocer los comandos...[/bold cyan]\n")

    while True:
        try:
            line = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[red]Saliendo...[/red]")
            fs.save_state() # Guardar estado del FS antes de salir.
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        # --- Dispatch de Comandos ---
        if cmd == 'help':
            console.print(help_text())

        # --- Comandos de Proceso ---
        elif cmd == 'newproc':
            if len(args) < 3:
                console.print("[yellow]Uso: newproc <pid> <cpu_units> <mem_req>[/yellow]")
                continue
            pid, cpu_s, mem_s = args[0], args[1], args[2]
            try:
                cpu = int(cpu_s); mem = int(mem_s)
            except ValueError:
                console.print("[red]cpu_units y mem_req deben ser enteros[/red]")
                continue
            ok, err = scheduler.create_process(pid, cpu, mem, memory)
            if not ok:
                console.print(f"[red]Error creando proceso: {err}[/red]")
            else:
                console.print(f"[green]Proceso {pid} creado (cpu={cpu}, mem={mem})[/green]")

        elif cmd == 'ps':
            rows = scheduler.list_processes()
            if not rows:
                console.print("[yellow]No hay procesos.[/yellow]")
            else:
                table = Table(title="Procesos Activos", header_style="bold cyan")
                table.add_column("PID", style="bold green")
                table.add_column("CPU Units", justify="right")
                table.add_column("State", style="bold yellow")
                table.add_column("Mem Req", justify="right")
                table.add_column("Addr", justify="right")
                for r in rows:
                    table.add_row(str(r['pid']), str(r['cpu_units']), str(r['state']), str(r['mem_req']), str(r['addr']))
                console.print(table)

        elif cmd == 'kill':
            if len(args) < 1:
                console.print("[yellow]Uso: kill <pid>[/yellow]")
                continue
            pid = args[0]
            ok = scheduler.kill_process(pid, memory)
            console.print("[green]Proceso terminado.[/green]" if ok else "[red]PID no encontrado.[/red]")

        # --- Comandos de Sincronización ---
        elif cmd == 'lock':
            if len(args) < 2:
                console.print("[yellow]Uso: lock <pid> <resource_id>[/yellow]")
                continue
            pid, resource_id = args[0], args[1]
            console.print(scheduler.lock(pid, resource_id))

        elif cmd == 'unlock':
            if len(args) < 2:
                console.print("[yellow]Uso: unlock <pid> <resource_id>[/yellow]")
                continue
            pid, resource_id = args[0], args[1]
            console.print(scheduler.unlock(pid, resource_id))

        # --- Comandos de Memoria ---
        elif cmd == 'alloc':
            if len(args) < 2:
                console.print("[yellow]Uso: alloc <pid> <size>[/yellow]")
                continue
            pid, sz_s = args[0], args[1]
            try:
                sz = int(sz_s)
            except ValueError:
                console.print("[red]El tamaño debe ser un entero.[/red]")
                continue
            addr = memory.alloc(pid, sz)
            if addr is None:
                console.print("[red]Fallo en alloc: memoria insuficiente.[/red]")
            else:
                for p in scheduler.processes:
                    if p.pid == pid:
                        p.addr = addr
                        p.mem_req = sz
                console.print(f"[green]Alloc OK: pid={pid} en addr={addr}[/green]")

        elif cmd == 'free':
            if len(args) < 1:
                console.print("[yellow]Uso: free <pid>[/yellow]")
                continue
            pid = args[0]
            ok = memory.free_mem(pid)
            if ok:
                for p in scheduler.processes:
                    if p.pid == pid:
                        p.addr = None
                        p.mem_req = 0
                console.print("[green]Free OK.[/green]")
            else:
                console.print("[red]Fallo en free: PID no encontrado o sin memoria asignada.[/red]")

        elif cmd == 'memmap':
            mm = memory.mem_map()
            table = Table(title="Mapa de Memoria", header_style="bold cyan")
            table.add_column("Total", justify="right")
            table.add_column("Libre", justify="right")
            table.add_column("Asignado", style="bold green")
            table.add_row(str(mm['total']), str(mm['free']), str(mm['allocations']))
            console.print(table)

        elif cmd == 'defrag':
            memory.defrag(scheduler.processes)
            console.print("[green]Memoria defragmentada.[/green]")

        # --- Comandos de Planificador y Demo ---
        elif cmd == 'run':
            scheduler.run(verbose=True, sleep_per_unit=0.1)
            console.print(f"[cyan]Timeline:[/cyan] {scheduler.get_timeline()}")

        elif cmd == 'demo':
            console.print("[cyan]Creando escenario demo: P1(5U,30), P2(3U,50), P3(7U,20)[/cyan]")
            scheduler.create_process('P1', 5, 30, memory)
            scheduler.create_process('P2', 3, 50, memory)
            scheduler.create_process('P3', 7, 20, memory)
            console.print("[cyan]Mapa de memoria antes de ejecutar:[/cyan]")
            console.print(memory.mem_map())
            scheduler.run(verbose=True, sleep_per_unit=0.1)
            console.print("[cyan]Mapa de memoria después de ejecutar:[/cyan]")
            console.print(memory.mem_map())
            console.print(f"[cyan]Timeline:[/cyan] {scheduler.get_timeline()}")

        # --- Comandos de Sistema de Archivos ---
        elif cmd == 'mkdir':
            if len(args) < 1:
                console.print('[yellow]Uso: mkdir <dirname>[/yellow]')
                continue
            console.print(fs.mkdir(args[0]))
        elif cmd == 'touch':
            if len(args) < 1:
                console.print('[yellow]Uso: touch <filename>[/yellow]')
                continue
            console.print(fs.touch(args[0]))
        elif cmd == 'ls':
            console.print(fs.ls())
        elif cmd == 'write':
            if len(args) < 2:
                console.print('[yellow]Uso: write <filename> <content>[/yellow]')
                continue
            filename = args[0]
            content = " ".join(args[1:])
            console.print(fs.write(filename, content))
        elif cmd == 'cat':
            if len(args) < 1:
                console.print('[yellow]Uso: cat <filename>[/yellow]')
                continue
            console.print(fs.cat(args[0]))

        # --- Salida ---
        elif cmd == 'exit':
            console.print("[red]Saliendo...[/red]")
            fs.save_state()
            break

        else:
            console.print("[red]Comando no reconocido. Escribe 'help' para ver la lista.[/red]")
