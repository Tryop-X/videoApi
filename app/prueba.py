from pymongo import MongoClient
from app.models import Models as models, datos as dt
from app.emb.EmbeddingService import EmbeddingService
import numpy as np
from bson.objectid import ObjectId
from scipy.spatial.distance import cosine

embeddings_service = EmbeddingService()


client_mongo = MongoClient(dt.MONGO_URI)
db = client_mongo[dt.DATABASE_NAME]
collection = db[dt.COLLECTION_NAME]

temario = models.TemarioObject("id", "enfermedades cardios basculares", [], [], "enfermedades cardios basculares")

emb_tem = np.ravel(embeddings_service.get_embedding(temario.temaCentral)).tolist()
emb_cons = np.ravel(embeddings_service.get_embedding(temario.consulta)).tolist()
tem_mongo = collection.insert_one(temario.to_dict_mongo(emb_tem, emb_cons))

temario_id = str(tem_mongo.inserted_id)

# Realiza la búsqueda
document = collection.find_one({"_id": ObjectId(temario_id)})

# Convierte el ObjectId a un string
print(document)

tem_embedding = np.array(document['temEmbedding'])
cons_embedding = np.array(document['cosEmbedding'])
similarity_score_1 = 1 - cosine(tem_embedding, cons_embedding)
print(similarity_score_1)