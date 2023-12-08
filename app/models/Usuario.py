from typing import List
from bson.objectid import ObjectId


class Usuario:
    def __init__(self, idUsuario: str, usuario: str, contrasegna: str, temarios: List[str], chats: List[str]):
        self.idUsuario = idUsuario
        self.usuario = usuario
        self.contrasegna = contrasegna
        self.temarios = temarios
        self.chats = chats
    def to_dict(self):
        return {
            'idUsuario': self.idUsuario,
            'usuario': self.usuario,
            'contrasegna': self.contrasegna,
            'temarios': self.temarios,
            'chats': self.chats
        }

    def to_dict_mongo(self):
        return {
            'usuario': self.usuario,
            'contrasegna': self.contrasegna,
            'temarios': self.temarios,
            'chats': self.chats
        }

def get_chat_from_mongo(usuario) -> Usuario:
    return Usuario(
        str(usuario['_id']),
        usuario['usuario'],
        usuario['contrasegna'],
        usuario['temarios'],
        usuario['chats'],
    )
