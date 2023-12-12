from pymongo import MongoClient
from app.models import datos as dt
from app.emb.EmbeddingService import EmbeddingService
embeddings_service = EmbeddingService()


class DataBaseConnection:
    def __init__(self):
        try:
            self.client_mongo = MongoClient(dt.MONGO_URI)
            self.db = self.client_mongo[dt.DATABASE_NAME]
            self.collection_temario = self.db[dt.COLLECTION_NAME_TEMARIO]
            self.collection_usuario = self.db[dt.COLLECTION_NAME_USUARIO]
            self.collection_chat = self.db[dt.COLLECTION_NAME_CHAT]
            self.collection_document = self.db[dt.COLLECTION_NAME_DOCUMENT]
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_chat_collection(self):
        return self.collection_chat

    def get_usuario_collection(self):
        return self.collection_usuario

    def get_temario_collection(self):
        return self.collection_temario

    def get_temario_document(self):
        return self.collection_document
