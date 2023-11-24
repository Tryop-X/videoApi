from typing import List

from pymongo import MongoClient
from googleapiclient.discovery import build
from app.models import video as models

class DataBaseConnection:
    def __init__(self, database_name="my_database", collection_name="my_collection"):

        self.API_KEY = "AIzaSyC_SSAcmJZgl_tBU4QuCnUpLCLikBOXkGI"
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'

        #################################################################################################################

        self.MONGO_URI = "mongodb+srv://hveras1:GlDC38DAX913ZSIv@videoai.mkgw6wh.mongodb.net/?retryWrites=true&w=majority"
        # self.MONGO_URI = "mongodb://127.0.0.1:27017/"
        self.DATABASE_NAME = database_name
        self.COLLECTION_NAME = collection_name
        self.similarity_threshold = 0.7
        try:
            self.client = MongoClient(self.MONGO_URI)
            self.db = self.client[self.DATABASE_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
        except Exception as e:
            print(f"Error connecting to database: {e}")

    # def search_video_embedding(self, query):
    #     try:
    #         emb = embeddingService.get_embedding(query)
    #         return self.search_videos_by_embedding(emb)
    #     except Exception as e:
    #         print(f"Error in search_video: {e}")
    #
    # def search_video(self, palabra):
    #     try:
    #         pipeline = self.consulta(palabra)
    #         result = list(self.collection.aggregate(pipeline))
    #         return result
    #     except Exception as e:
    #         print(f"Error inserting videos: {e}")

    def close(self):
        if self.client:
            self.client.close()

    def buscar_videos(self, palabra_clave, max_resultados=2) -> List[models.Item]:
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.API_KEY)

        # Hacer la solicitud para buscar videos por palabra clave
        request = youtube.search().list(q=palabra_clave, part='id,snippet', maxResults=max_resultados)
        response = request.execute()

        return response.items

    def get_temario_videos(self, temario: models.TemarioObject) -> models.TemarioObject:

        for asp in temario.aspectos:

            lista_items = list()
            for tema in asp.temas:
                items = self.buscar_videos(temario.temaCentral + " " + asp.aspecto + " " + tema)
                lista_items.append(items)

            asp.items = lista_items

        return temario
