from dataclasses import dataclass


@dataclass
class EstadoCanje:
    usuario: str
    coleccion: str

    repetidas: set[int]
    faltantes: set[int]
