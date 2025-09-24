|**INSTITUCIÓN UNIVESITARIA DE COLOMBIA**||
| :-: | :- |
|**SISTEMAS OPERATIVOS**||
|I. **DATOS GENERALES** ||
|<p>**Nombre del estudiante:**</p><p>**Nombre del profesor:**</p><p>**Fecha inicio/ Fecha fin:**</p><p>**Horarios:**</p><p>**Duración en Horas:**</p><p>**Carrera:**</p><p>**Tema:**</p><p>**Taller:** </p>|<p></p><p>**: José Antonio Martínez J**</p><p>**: 23-09-2025**</p><p>**: 10am – 12m**</p><p>**: 4 horas**</p><p>**: Ing Software y Sistemas**</p><p>**: Prototipo de un Sistema Operativo Básico:**</p><p>**TALLER 008**</p>|

Estos son solo algunos de los comandos básicos en Linux. Hay muchos más comandos y opciones disponibles, pero estos deberían ser suficientes para comenzar a trabajar en la línea de comandos de Linux.

Aquí tienes una lista de algunos comandos básicos de Linux junto con una breve descripción de su funcionalidad:

**Ejercicio: Prototipo de un Sistema Operativo Básico**

**Descripción General del Ejercicio**

Este ejercicio está diseñado para estudiantes de 5° semestre de Ingeniería de Sistemas en la asignatura de Sistemas Operativos.

**El objetivo principal** : Utilizando sus habilidades en el uso de herramientas de programación tales como:

- **Lenguajes de Programación**:
  - **C/C++ (Recomendado principal)**: Ideal para simular kernels y bajo nivel. Usa bibliotecas estándar como <pthread.h> para hilos (procesos) y <stdlib.h> para memoria.
  - **Assembly (x86 o ARM, opcional)**: Para partes críticas como interrupciones o boot loader simple, si el grupo quiere emular hardware.
  - **Python (Para prototipos rápidos)**: Útil para simular alto nivel (e.g., con threading para procesos, mmap para memoria). Menos "auténtico", pero acelera el desarrollo; justifiquen su uso.

Deberá realizar la implementación de un **PROTOTIPO**, simple de un sistema operativo (OS).

- **Aclaraciones:** El prototipo no busca ser un OS completo y funcional en hardware real, sino una simulación o emulación que demuestre el funcionamiento de  3 o 4  componentes tradicionales de un OS.
- Esto fomentará la comprensión de la arquitectura de un OS, la gestión de recursos y la interacción con el hardware a nivel abstracto.

El proyecto se desarrollará en grupos de 2  estudiantes, con una duración estimada de 8 horas. Cada grupo elegirá o implementará al menos **dos a tres  apartados tradicionales** de un OS, y opcionalmente un cuarta si el tiempo lo permite. El prototipo debe ser ejecutable en un entorno de simulación o emulación, y debe incluir una interfaz básica (por ejemplo, un shell de comandos o una consola simulada) para interactuar con los componentes.

**Objetivos Específicos**

- Comprender y simular el rol de componentes clave en un OS (gestión de procesos, memoria o archivos).
- Analizar desafíos como concurrencia, sincronización y eficiencia en la gestión de recursos.
- Documentar el diseño, implementación y pruebas del prototipo.

**Apartados Tradicionales a Desarrollar**

Los estudiantes deben seleccionar y implementar **al menos tres**  de los siguientes apartados tradicionales de un sistema operativo. Se recomienda enfocarse en componentes interrelacionados para mayor coherencia (por ejemplo, gestión de procesos con memoria). El cuarto apartado es opcional para grupos avanzados.

Cada apartado debe incluir:

- Una explicación teórica breve en el informe (basada en conceptos del curso, como los descritos en Tanenbaum o Silberschatz).
- Implementación funcional en código.
- Pruebas que demuestren su operación (e.g., escenarios de uso).
1. **Gestión de Procesos (Obligatorio para al menos un grupo por selección)**:
   1. Implementar un planificador (scheduler) simple, como Round-Robin o FCFS (First-Come-First-Served).
   1. Simular la creación, ejecución y terminación de procesos (usando hilos o procesos simulados).
   1. Incluir mecanismos básicos de sincronización (e.g., semáforos o mutex para evitar deadlocks).
   1. Ejemplo de funcionalidad: Un shell que permita crear "procesos" (tareas) y alternar entre ellas.
1. **Gestión de Memoria**:
   1. Desarrollar un allocador de memoria simple (e.g., First-Fit o Best-Fit para particionamiento contiguo o paginación básica).
   1. Simular la asignación y liberación de memoria para múltiples procesos.
   1. Manejar fragmentación interna/externa y virtualización básica (e.g., mapeo de direcciones virtuales a físicas).
   1. Ejemplo de funcionalidad: Solicitudes de memoria desde el shell y reporte de uso actual.
1. **Sistema de Archivos (Opcional o como tercero)**:
   1. Crear una estructura de archivos básica (e.g., árbol de directorios con FAT-like o inodos simples).
   1. Implementar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para archivos simulados.
   1. Simular persistencia en disco (usando archivos en el host OS como "disco virtual").
   1. Ejemplo de funcionalidad: Comandos para crear directorios, escribir/leer archivos y listar contenidos.

Si el grupo elige solo dos, justifiquen en el informe por qué no incluyeron el tercero

Instalación sugerida: Usa un entorno Linux (Ubuntu o WSL en Windows) para mayor compatibilidad con herramientas de OS dev. Eviten frameworks high-level como Unity o Electron, ya que diluyen los conceptos de OS.

**Cómo Sustentar el Proyecto**

La sustentación (presentación y defensa) es obligatoria y debe demostrar el funcionamiento del prototipo. Se realizará en una sesión de 15, minutos por grupo al final del plazo.

Criterios de evaluación: Funcionalidad (40%), Correctitud conceptual (30%), Innovación/integración (20%), Claridad en demo (10%).

**Entrega del Informe**

- El informe final debe entregarse en formato PDF (máximo 15-20 páginas, Arial 11, interlineado 1.5) vía plataforma LMS (e.g., Moodle) o email, junto con el código fuente y archivos ejecutables.
- Plazo: EL 29 de sep deberá realizar la entrega antes de la sustentación.
- **Estructura del Informe**:
  - **Portada**: Título, nombres de integrantes, semestre, asignatura, fecha.
  - **Resumen Ejecutivo** (1 página): Descripción breve del prototipo, apartados implementados y resultados clave.
  - **Introducción** (1-2 páginas): Contexto teórico de OS, objetivos y justificación de apartados seleccionados.
  - **Diseño y Arquitectura** (3-5 páginas): Diagramas (UML o flujo) de los componentes, pseudocódigo y explicación de interacciones.
  - **Implementación** (4-6 páginas): Descripción del código por apartado, con snippets clave (no todo el código). Incluya desafíos enfrentados (e.g., bugs en memoria) y soluciones.
  - **Pruebas y Resultados** (2-3 páginas): Tabla de casos de prueba, capturas de pantalla/ejecución, métricas (e.g., tiempo de scheduling).
  - **Conclusiones y Mejoras** (1 página): Lecciones aprendidas, limitaciones y sugerencias futuras.
  - **Referencias**: Libros del curso, tutoriales OSDev, etc. (APA o IEEE).
  - **Anexos**: Código fuente completo (en ZIP), scripts de build, diagrama de Gantt del proyecto.
- **Requisitos Adicionales**:
  - Código: Limpio, comentado (al menos 20% comentarios), con README.md explicando cómo compilar/ejecutar.
  - Originalidad: Use herramientas antiplagio; citen cualquier código base (e.g., de GitHub).
  - Formato de entrega: ZIP con informe.pdf, src/ (código), bin/ (ejecutables), y slides.pptx.

**Criterios de Evaluación General**

- Funcionalidad y cobertura de apartados: 40%.
- Calidad del código y documentación: 30%.
- Informe y sustentación: 20%.
- Trabajo en equipo y originalidad: 10%.
