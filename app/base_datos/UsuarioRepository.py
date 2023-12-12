from app.models import Usuario as models_usuario
from bson.objectid import ObjectId
from app.base_datos.date_base_conection import DataBaseConnection
from typing import List


class UsuarioRepository:
    def __init__(self):
        self.connection = DataBaseConnection()
        self.collection = self.connection.get_usuario_collection()

    def get_usuario_id_mongo(self, usuario_id) -> models_usuario.Usuario:
        document_temario = self.collection.find_one({"_id": ObjectId(usuario_id)})
        return models_usuario.get_usuario_from_mongo(document_temario)

    def save_usuario(self, usuario: models_usuario.Usuario) -> models_usuario.Usuario:
        tem_mongo = self.collection.insert_one(usuario.to_dict_mongo())
        usuario_id = str(tem_mongo.inserted_id)
        temario_saved = self.get_usuario_id_mongo(usuario_id)
        return temario_saved

    def login_usuario(self, usuario: str, contrasegna: str) -> models_usuario.Usuario:
        query = {"$and": [{"usuario": usuario}, {"contrasegna": contrasegna}]}
        usuario_mongo = self.collection.find_one(query)
        if usuario_mongo:
            return models_usuario.get_usuario_from_mongo(usuario_mongo)
        else:
            raise ValueError("Credenciales de usuario incorrectas")

    def update_temarios(self, idUser: str, idTemario: str):
        usuario_consulta = self.get_usuario_id_mongo(idUser)

        if idTemario in usuario_consulta.temarios:
            return usuario_consulta

        usuario_consulta.temarios.append(idTemario)
        myquery = {"_id": ObjectId(idUser)}
        new_values = {"$set": {
            'temarios': usuario_consulta.temarios,
        }}
        self.collection.update_one(myquery, new_values)
        temario_updated = self.get_usuario_id_mongo(idUser)
        return temario_updated

