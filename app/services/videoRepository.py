from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
from googleapiclient.discovery import build
from app.models import Models as models, datos as dt
import app.models.Models as mod
from openai import OpenAI
import json
from app.emb.EmbeddingService import EmbeddingService
import numpy as np
from scipy.spatial.distance import cosine
from typing import List
from bson.objectid import ObjectId


embeddings_service = EmbeddingService()


def get_transcription_list(videoId: str):
    return YouTubeTranscriptApi.list_transcripts(videoId)


def append_video(video_youtube: models.VideoYoutube, lista_items) -> bool:
    for it in lista_items:
        if video_youtube.videoId != it.videoId:
            return True
    if len(lista_items) == 0:
        return True
    return False

class VideoRepository:
    def __init__(self):

        self.client_open_ai = OpenAI(api_key=dt.API_KEY_OPENAI)
        self.similarity_threshold = 0.80
        try:
            self.client_mongo = MongoClient(dt.MONGO_URI)
            self.db = self.client_mongo[dt.DATABASE_NAME]
            self.collection = self.db[dt.COLLECTION_NAME]
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_resumen(self, transcription):
        completion = self.client_open_ai.chat.completions.create(
            model=dt.model_resumen,
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": dt.content_resumen},
                {"role": "user",
                 "content": transcription}
            ]
        )
        return completion.choices[0].message.content

    def get_chat(self, contenido, pregunta):
        completion = self.client_open_ai.chat.completions.create(
            model=dt.model_chat,
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": dt.content_chat + " Contenido: " + contenido},
                {"role": "user",
                 "content": pregunta}
            ]
        )
        return completion.choices[0].message.content

    def get_video_with_trans_resume(self, video: models.VideoYoutube):

        try:
            transcription = get_transcription_list(video.videoId)

            transcript = None

            for t in transcription:
                transcript = t.fetch()
                break

            trans = ""

            for entry in transcript:
                trans = trans + entry['text'] + " "

            video.transcription = trans
            video.resume = self.get_resumen(trans)

            return video

        except Exception as e:
            print(f"Error in search_video: {e}")

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

    def get_temario(self, peticion):

        hay_video, temario = self.get_temario_by_embedding(peticion)

        if hay_video:
            return hay_video, temario
        else:

            completion = self.client_open_ai.chat.completions.create(
                model=dt.model_temario,
                stop=["END"],
                messages=[
                    {"role": "system",
                     "content": dt.content_temario
                     },
                    {"role": "user",
                     "content": peticion}
                ]
            )

            print(completion.choices[0].message.content)

            json_data = json.loads(completion.choices[0].message.content
                                   .replace('```json', '')
                                   .replace('```', '')
                                   .strip())
            aspectos_list = [models.Aspecto(aspecto['aspecto'], aspecto['temas'], []) for aspecto in
                             json_data['aspectos']]
            temario_object = models.TemarioObject("", json_data['temaCentral'], aspectos_list, [], peticion)

            return hay_video, temario_object

    def close(self):
        if self.client_mongo:
            self.client_mongo.close()

    def buscar_videos(self, consulta, max_resultados=6):

        youtube = build(dt.YOUTUBE_API_SERVICE_NAME, dt.YOUTUBE_API_VERSION, developerKey=dt.API_KEY_YOUTUBE)
        request = youtube.search().list(q=consulta, part='id,snippet', maxResults=max_resultados, type='video')
        response = request.execute()

        return response.get("items", [])

    def get_temario_id_mongo(self, tem_mongo):
        temario_id = str(tem_mongo.inserted_id)
        document_temario = self.collection.find_one({"_id": ObjectId(temario_id)})
        return mod.get_temario_from_mongo(document_temario)

    def save_temario(self, temario: models.TemarioObject) -> models.TemarioObject:
        emb_tem = np.ravel(embeddings_service.get_embedding(temario.temaCentral)).tolist()
        emb_cons = np.ravel(embeddings_service.get_embedding(temario.consulta)).tolist()
        tem_mongo = self.collection.insert_one(temario.to_dict_mongo(emb_tem, emb_cons))

        temario_saved = self.get_temario_id_mongo(tem_mongo)
        return temario_saved

    def get_temario_videos(self, temario: models.TemarioObject, hay_video: bool) -> models.TemarioObject:

        if hay_video:
            return temario
        else:
            for asp in temario.aspectos:
                lista_items = list()
                for tema in asp.temas:
                    items = self.buscar_videos(tema + " " + temario.temaCentral + " " + asp.aspecto)
                    video_puntero = 0
                    for item in items:
                        if video_puntero >= 2:
                            break

                        video_youtube = mod.get_video_yout_by_item(item)
                        is_unique = append_video(video_youtube, lista_items)
                        if is_unique:
                            video_puntero += 1
                            lista_items.append(video_youtube)
                            print("SE HA AGREGADO UN VÍDEO")

                asp.videos = lista_items

            temario_saved = self.save_temario(temario)

            return temario_saved
