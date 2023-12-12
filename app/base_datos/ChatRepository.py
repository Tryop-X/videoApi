from app.models import Chat as models_chat
from bson.objectid import ObjectId
from app.base_datos.date_base_conection import DataBaseConnection
from datetime import datetime


def get_date():
    fecha_actual = datetime.now()
    return fecha_actual.strftime('%d/%m/%Y %H:%M')


class ChatRepository:
    def __init__(self):
        self.connection = DataBaseConnection()
        self.collection = self.connection.get_chat_collection()

    def get_chat_id_mongo(self, chat_id) -> models_chat.Chat:
        document_temario = self.collection.find_one({"_id": ObjectId(chat_id)})
        return models_chat.get_chat_from_mongo(document_temario)

    def get_chat_usuario(self, idUsuario: str, idTemario: str) -> models_chat.Chat:
        query = {"$and": [{"idUsuario": idUsuario}, {"idTemario": idTemario}]}
        chat_mongo = self.collection.find_one(query)
        return models_chat.get_chat_from_mongo(chat_mongo)

    def update_conversation(self, conv: models_chat.ResQues,  idChat: str) -> models_chat.Chat:
        chat = self.get_chat_id_mongo(idChat)
        conv.date = get_date()
        chat.conversation.append(conv)
        chat_updated = self.update_chat(chat)
        return chat_updated

    def update_chat_usuario(self, idChat: str, pregunta: str, respuesta: str) -> models_chat.Chat:
        chat = self.get_chat_id_mongo(idChat)
        myquery = {"_id": ObjectId(chat.idChat)}
        chat.conversation.append(models_chat.ResQues(response=respuesta, question=pregunta, date=get_date()))
        new_values = {"$set": {
            'conversation': [con.to_dict() for con in chat.conversation] if chat.conversation else [],
        }}
        self.collection.update_one(myquery, new_values)
        return self.get_chat_id_mongo(chat.idChat)

    def save_get_chat(self, idUsuario: str, idTemario: str) -> models_chat.Chat:
        query = {"$and": [{"idUsuario": idUsuario}, {"idTemario": idTemario}]}
        chat_mongo = self.collection.find_one(query)
        if chat_mongo is not None:
            return models_chat.get_chat_from_mongo(chat_mongo)
        else:
            chat = models_chat.Chat('', idTemario, idUsuario, get_date(), [])
            chat_saved = self.save_chat(chat)
            return chat_saved

    def update_chat(self, chat: models_chat.Chat) -> models_chat.Chat:
        myquery = {"_id": ObjectId(chat.idChat)}
        new_values = {"$set": {
            'conversation': [con.to_dict() for con in chat.conversation] if chat.conversation else [],
        }}
        self.collection.update_one(myquery, new_values)
        chat_updated = self.get_chat_id_mongo(chat.idChat)
        return chat_updated

    def save_chat(self, chat: models_chat.Chat) -> models_chat.Chat:
        chat.date = get_date()
        chat_mongo = self.collection.insert_one(chat.to_dict_mongo())
        usuario_id = str(chat_mongo.inserted_id)
        chat_updated = self.get_chat_id_mongo(usuario_id)
        return chat_updated
