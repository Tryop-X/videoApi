from app.models import Models as models_temario, Usuario as models_usuario, datos as dt
import app.models.Models as mod
from app.emb.EmbeddingService import EmbeddingService
import numpy as np
from scipy.spatial.distance import cosine
from bson.objectid import ObjectId
from app.base_datos.date_base_conection import DataBaseConnection

embeddings_service = EmbeddingService()


class TemarioRepository:
    def __init__(self):
        self.similarity_threshold = 0.85
        self.connection = DataBaseConnection()
        self.collection = self.connection.get_temario_collection()

    def get_temario_by_embedding(self, consulta: str):

        embedding1_flat = np.ravel(embeddings_service.get_embedding(consulta))
        temarios = list(self.collection.find())
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

    def get_temario_id_mongo(self, temario_id) -> models_temario.Temario:
        document_temario = self.collection.find_one({"_id": ObjectId(temario_id)})
        return mod.get_temario_from_mongo(document_temario)

    def save_temario(self, temario: models_temario.Temario) -> models_temario.Temario:
        emb_tem = np.ravel(embeddings_service.get_embedding(temario.temaCentral)).tolist()
        emb_cons = np.ravel(embeddings_service.get_embedding(temario.consulta)).tolist()
        tem_mongo = self.collection.insert_one(temario.to_dict_mongo(emb_tem, emb_cons))

        temario_id = str(tem_mongo.inserted_id)
        temario_saved = self.get_temario_id_mongo(temario_id)
        return temario_saved

    def update_aspectos(self, temario: models_temario.Temario) -> models_temario.Temario:
        myquery = {"_id": ObjectId(temario.idTemario)}
        new_values = {"$set": {
            "aspectos": [asp.to_dict() for asp in temario.aspectos] if temario.aspectos else []
        }}
        self.collection.update_one(myquery, new_values)
        temario_saved = self.get_temario_id_mongo(temario.idTemario)
        return temario_saved

    def update_content_pdf(self, temario: models_temario.Temario, contendPdf: str) -> models_temario.Temario:
        myquery = {"_id": ObjectId(temario.idTemario)}
        new_values = {"$set": {
            "contendPdf": contendPdf
        }}
        self.collection.update_one(myquery, new_values)
        temario_saved = self.get_temario_id_mongo(temario.idTemario)
        return temario_saved

    def get_content_pdf(self, idTemario: str) -> str:
        document_temario = self.collection.find_one({"_id": ObjectId(idTemario)}, {"contendPdf": 1})
        return document_temario["contendPdf"] if document_temario["contendPdf"] else ""
