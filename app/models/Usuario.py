from typing import List
from bson.objectid import ObjectId


class Usuario:
    def __init__(self, idUsuario: str, usuario: str, contrasegna: str, nombreCompleto: str, temarios: List[str]):
        self.idUsuario = idUsuario
        self.usuario = usuario
        self.nombreCompleto = nombreCompleto
        self.contrasegna = contrasegna
        self.temarios = temarios
    def to_dict(self):
        return {
            'idUsuario': self.idUsuario,
            'usuario': self.usuario,
            'contrasegna': self.contrasegna,
            'temarios': self.temarios
        }

    def to_dict_mongo(self):
        return {
            'usuario': self.usuario,
            'contrasegna': self.contrasegna,
            'temarios': self.temarios
        }


def get_usuario_from_mongo(usuario) -> Usuario:
    return Usuario(
        str(usuario['_id']),
        usuario['usuario'],
        usuario['contrasegna'],
        usuario['nombreCompleto'],
        usuario['temarios'] if usuario['temarios'] else []
    )
