from pymongo import MongoClient
from app.models import Models as models_temario, Usuario as models_usuario, datos as dt
import app.models.Models as mod
from app.emb.EmbeddingService import EmbeddingService
import numpy as np
from scipy.spatial.distance import cosine
from bson.objectid import ObjectId

embeddings_service = EmbeddingService()

class VideoRepository:
    def __init__(self):
        self.similarity_threshold = 0.7
        try:
            self.client_mongo = MongoClient(dt.MONGO_URI)
            self.db = self.client_mongo[dt.DATABASE_NAME]
            self.collection_tamerio = self.db[dt.COLLECTION_NAME_TEMARIO]
            self.collection_usuario = self.db[dt.COLLECTION_NAME_USUARIO]
            self.collection_chat = self.db[dt.COLLECTION_NAME_CHAT]
        except Exception as e:
            print(f"Error connecting to database: {e}")


    def get_temario_by_embedding(self, consulta: str):

        embedding1_flat = np.ravel(embeddings_service.get_embedding(consulta))
        temarios = list(self.collection_tamerio.find())
        hay_temario = False
        tems = list()
        for tem in temarios:
            tem_embedding = np.array(tem['temEmbedding'])
            cons_embedding = np.array(tem['cosEmbedding'])
            similarity_score_1 = 1 - cosine(tem_embedding, embedding1_flat)
            similarity_score_2 = 1 - cosine(cons_embedding, embedding1_flat)
            if similarity_score_1 >= self.similarity_threshold or similarity_score_2 >= self.similarity_threshold:
                hay_temario = True
                tems.append({'temario': tem, 'sim': (similarity_score_1 + similarity_score_2)})

        if len(tems) > 0:
            tem = max(tems, key=lambda x: x['sim'])['temario']
            return hay_temario, mod.get_temario_from_mongo(tem)
        else:
            return hay_temario, None

    def get_temario_id_mongo(self, temario_id) -> models_temario.TemarioObject:
        document_temario = self.collection_tamerio.find_one({"_id": ObjectId(temario_id)})
        return mod.get_temario_from_mongo(document_temario)


    def close(self):
        if self.client_mongo:
            self.client_mongo.close()



    def get_usuario_id_mongo(self, usuarioo_id) -> models_temario.TemarioObject:
        document_temario = self.collection_usuario.find_one({"_id": ObjectId(usuarioo_id)})
        return mod.get_temario_from_mongo(document_temario)

    def save_usuario(self, usuario: models_usuario.Usuario) -> models_temario.TemarioObject:
        tem_mongo = self.collection_tamerio.insert_one(usuario.to_dict_mongo())
        temario_id = str(tem_mongo.inserted_id)
        temario_saved = self.get_temario_id_mongo(temario_id)
        return temario_saved

    def get_chat_id_mongo(self, chat_id) -> models_temario.TemarioObject:
        document_temario = self.collection_chat.find_one({"_id": ObjectId(chat_id)})
        return mod.get_temario_from_mongo(document_temario)

    def save_temario(self, temario: models_temario.TemarioObject) -> models_temario.TemarioObject:
        emb_tem = np.ravel(embeddings_service.get_embedding(temario.temaCentral)).tolist()
        emb_cons = np.ravel(embeddings_service.get_embedding(temario.consulta)).tolist()
        tem_mongo = self.collection_tamerio.insert_one(temario.to_dict_mongo(emb_tem, emb_cons))

        temario_id = str(tem_mongo.inserted_id)
        temario_saved = self.get_temario_id_mongo(temario_id)
        return temario_saved

    def update_aspectos(self, temario: models_temario.TemarioObject):

        myquery = {"_id": ObjectId(temario.id_temario)}
        new_values = {"$set": {
            "aspectos": [asp.to_dict() for asp in temario.aspectos] if temario.aspectos else []
        }}
        tem_mongo = self.collection_tamerio.update_one(myquery, new_values)
        return tem_mongo

    def update_content_pdf(self, temario: models_temario.TemarioObject, contend_pdf: str):

        myquery = {"_id": ObjectId(temario.id_temario)}
        new_values = {"$set": {
            "contend_pdf": contend_pdf
        }}
        tem_mongo = self.collection_tamerio.update_one(myquery, new_values)
        return tem_mongo
