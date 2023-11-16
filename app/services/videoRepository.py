from pymongo import MongoClient
from app.Emb.EmbeddingService import EmbeddingService
import numpy as np
from scipy.spatial.distance import cosine

embeddingService = EmbeddingService()


class DataBaseConnection:
    def __init__(self, database_name="my_database", collection_name="my_collection"):
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

    def search_video_embedding(self, query):
        try:
            emb = embeddingService.get_embedding(query)
            return self.search_videos_by_embedding(emb)
        except Exception as e:
            print(f"Error in search_video: {e}")

    def search_video(self, palabra):
        try:
            pipeline = self.consulta(palabra)
            result = list(self.collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"Error inserting videos: {e}")

    def close(self):
        if self.client:
            self.client.close()

    # def search_videos_by_embeddiang(self, query_embedding):
    #     try:
    #
    #                 # Calcular la similitud coseno entre los dos embeddings aplanados
    #                 similarity_score = 1 - cosine(embedding1_flat, embedding2_flat)
    #
    #                 sim = cosine_similarity(query_embedding, transcript_embedding)[0][0]
    #                 if sim > similarity_threshold:
    #                     similarities.append((video, sim))
    #
    #
    #             all_embeddings = [np.array(transcript['embedding']) for transcript in video['transcription']]
    #
    #
    #
    #             if all_embeddings:
    #                 # Calcular el promedio de los embeddings
    #                 avg_embedding = np.mean(all_embeddings, axis=0)
    #                 avg_embedding = avg_embedding.reshape(1, -1)  # Reformar a dos dimensiones
    #
    #                 sim = cosine_similarity([query_embedding], [avg_embedding])[0][0]
    #                 if sim > similarity_threshold:
    #                     similarities.append((video, sim))
    #
    #         # Ordenar por similitud
    #         sorted_videos = sorted(similarities, key=lambda x: x[1], reverse=True)
    #         return [video for video, sim in sorted_videos]
    #
    #     except Exception as e:
    #         print(f"Error searching videos: {e}")
    #         return []

    def search_videos_by_embedding(self, data):

        videos = list(self.collection.find({}, {"cod": 1, "title": 1, "url": 1, "transcription": 1}))
        similarity_threshold = 0.5  # Umbral de similitud

        for temas in data:

            pregunta1 = temas["preguntas"][0]["pregunta"]
            pregunta2 = temas["preguntas"][1]["pregunta"]
            pregunta3 = temas["preguntas"][2]["pregunta"]

            for video in videos:

                embedding1_flat = np.ravel(embeddingService.get_embedding(pregunta1))
                embedding2_flat = np.ravel(embeddingService.get_embedding(pregunta2))
                embedding3_flat = np.ravel(embeddingService.get_embedding(pregunta3))

                s1 = 0
                s2 = 0
                s3 = 0

                for transcript in video['transcription']:

                    if transcript.get('embedding') is not None:

                        transcript_embedding = np.ravel(transcript['embedding'])
                        similarity_score1 = 1 - cosine(transcript_embedding, embedding1_flat)
                        similarity_score2 = 1 - cosine(transcript_embedding, embedding2_flat)
                        similarity_score3 = 1 - cosine(transcript_embedding, embedding3_flat)

                        if (s1 < similarity_score1):
                            s1 = similarity_score1
                        if (s2 < similarity_score2):
                            s1 = similarity_score1
                        if (s3 < similarity_score3):
                            s1 = similarity_score1

                video["s1"] = s1
                video["s2"] = s2
                video["s3"] = s3

            vidtema1 = max(videos, key=lambda x: x["s1"])
            vidtema2 = max(videos, key=lambda x: x["s2"])
            vidtema3 = max(videos, key=lambda x: x["s3"])

            temas["videos"] = [
                {
                    'url': vidtema1["url"],
                    'cod': vidtema1["cod"],
                    'title': vidtema1["title"],
                    'similarity': vidtema1["s1"]
                },
                {
                    'url': vidtema2["url"],
                    'cod': vidtema2["cod"],
                    'title': vidtema2["title"],
                    'similarity': vidtema2["s1"]
                },
                {
                    'url': vidtema3["url"],
                    'cod': vidtema3["cod"],
                    'title': vidtema3["title"],
                    'similarity': vidtema3["s1"]
                },
            ]

        return data

    def consulta(self, palabra):
        pipeline = [
            {
                "$match": {
                    "transcription": {
                        "$elemMatch": {
                            "content": {
                                "$regex": palabra,
                                "$options": 'i'
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "url": 1,
                    "transcription": {
                        "$filter": {
                            "input": "$transcription",
                            "as": "transcript",
                            "cond": {
                                "$regexMatch": {
                                    "input": "$$transcript.content",
                                    "regex": palabra,
                                    "options": "i"
                                }
                            }
                        }
                    },
                    "description": 1,
                    "resume": 1,
                    "cod": 1,
                    "category": 1,
                    "title": 1
                }
            }
        ]
        return pipeline
