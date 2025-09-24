"""
Sistema de Archivos Simulado en Memoria.

Este módulo implementa un sistema de archivos jerárquico simple que reside en memoria.
Utiliza una estructura de "inodos" para representar archivos y directorios.
Proporciona persistencia básica al guardar y cargar su estado en un archivo JSON.
"""

import json
from typing import Dict, Any, Optional

# Constantes para los tipos de nodos en el sistema de archivos.
FS_FILE = 'file'
FS_DIR = 'dir'

class Inode:
    """
    Representa un "inodo" en el sistema de archivos, que puede ser un archivo o un directorio.
    
    Atributos:
        name (str): Nombre del archivo o directorio.
        type (str): Tipo de nodo ('file' o 'dir').
        parent (Optional[Inode]): Referencia al inodo padre (directorio contenedor).
        children (Dict[str, Inode]): Si es un directorio, un diccionario de sus hijos.
        content (str): Si es un archivo, su contenido.
    """
    def __init__(self, name: str, node_type: str, parent: Optional['Inode'] = None):
        """Inicializa un nuevo inodo."""
        self.name = name
        self.type = node_type
        self.parent = parent
        # Un directorio tiene hijos, un archivo no.
        self.children: Dict[str, 'Inode'] = {} if node_type == FS_DIR else None
        # Un archivo tiene contenido, un directorio no.
        self.content: str = "" if node_type == FS_FILE else None

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el inodo y toda su descendencia a un diccionario para la persistencia en JSON."""
        data = {
            'name': self.name,
            'type': self.type,
            'content': self.content,
            # Serializa recursivamente a los hijos.
            'children': {name: child.to_dict() for name, child in self.children.items()} if self.children is not None else None
        }
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any], parent: Optional['Inode'] = None) -> 'Inode':
        """Deserializa un diccionario (de JSON) a una estructura de inodos."""
        node = Inode(data['name'], data['type'], parent)
        if data['type'] == FS_FILE:
            node.content = data.get('content', '')
        else:
            # Deserializa recursivamente a los hijos.
            node.children = {name: Inode.from_dict(child_data, node) for name, child_data in data.get('children', {}).items()}
        return node

class FileSystem:
    """
    Gestiona la estructura del sistema de archivos, el estado y las operaciones.
    """
    def __init__(self, persistence_path: str = 'fs_state.json'):
        """Inicializa el FS, cargando el estado desde un archivo si existe."""
        self.persistence_path = persistence_path
        try:
            # Intenta cargar un estado previo del sistema de archivos.
            with open(self.persistence_path, 'r') as f:
                data = json.load(f)
                self.root = Inode.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si no hay estado previo o está corrupto, crea un FS nuevo con un directorio raíz.
            self.root = Inode('/', FS_DIR)
        self.cwd = self.root  # El directorio de trabajo actual comienza en la raíz.

    def save_state(self):
        """Guarda el estado actual del FS en un archivo JSON para persistencia."""
        with open(self.persistence_path, 'w') as f:
            json.dump(self.root.to_dict(), f, indent=4)

    def _get_path(self, path: str) -> Optional[Inode]:
        """Resuelve una ruta (absoluta o relativa) a un inodo."""
        if path.startswith('/'):
            # Ruta absoluta: empezar desde la raíz.
            current_node = self.root
            parts = path.strip('/').split('/')
        else:
            # Ruta relativa: empezar desde el directorio de trabajo actual.
            current_node = self.cwd
            parts = path.split('/')
        
        if parts == ['']:
            return current_node

        for part in parts:
            if part == '.':
                continue
            if part == '..':
                if current_node.parent:
                    current_node = current_node.parent
                continue
            
            if current_node.type == FS_DIR and part in current_node.children:
                current_node = current_node.children[part]
            else:
                # Parte de la ruta no encontrada.
                return None
        return current_node

    def mkdir(self, dirname: str) -> str:
        """Crea un nuevo directorio en el directorio de trabajo actual."""
        if '/' in dirname:
            return "Error: El nombre del directorio no puede contener '/'."
        if dirname in self.cwd.children:
            return f"Error: '{dirname}' ya existe."
        
        new_dir = Inode(dirname, FS_DIR, self.cwd)
        self.cwd.children[dirname] = new_dir
        return f"Directorio '{dirname}' creado."

    def touch(self, filename: str) -> str:
        """Crea un nuevo archivo vacío en el directorio de trabajo actual."""
        if '/' in filename:
            return "Error: El nombre del archivo no puede contener '/'."
        if filename in self.cwd.children:
            return f"Error: '{filename}' ya existe."

        new_file = Inode(filename, FS_FILE, self.cwd)
        self.cwd.children[filename] = new_file
        return f"Archivo '{filename}' creado."

    def ls(self) -> str:
        """Lista el contenido del directorio de trabajo actual."""
        if self.cwd.type != FS_DIR:
            return "Error: No es un directorio."
        
        content = []
        for name, node in self.cwd.children.items():
            suffix = '/' if node.type == FS_DIR else ''
            content.append(f"{name}{suffix}")
        return "\n".join(content) if content else "(vacío)"

    def write(self, filename: str, content: str) -> str:
        """Escribe (o sobrescribe) contenido en un archivo."""
        node = self._get_path(filename)
        if not node:
            return f"Error: Archivo '{filename}' no encontrado."
        if node.type != FS_FILE:
            return f"Error: '{filename}' no es un archivo."
        
        node.content = content
        return f"Contenido escrito en '{filename}'."

    def cat(self, filename: str) -> str:
        """Muestra el contenido de un archivo."""
        node = self._get_path(filename)
        if not node:
            return f"Error: Archivo '{filename}' no encontrado."
        if node.type != FS_FILE:
            return f"Error: '{filename}' no es un archivo."
        
        return node.content