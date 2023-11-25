from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
from googleapiclient.discovery import build
from app.models import video as models
from openai import OpenAI
import json

content_temario = """
Responde con un investigador siempre sugiriendo temas de investigación. Parte de temas 
más simples a más complejos.
Responde siempre con el siguiente json (3 temas como máximo, 3 aspectos como máximo)
{
    temaCentral: "", 
    aspectos: [
        {
            aspecto: "",
            temas: ["", "", ...]
        }, ...
    ]
}
"""

content_resumen = """
Vas a generar un resumen usando lenguaje de un investigador experto. Vas a extraer el contenido y el resumen que generes
tendrá la información que la transcripción que se ha proporcionado
"""

content_chat = """
Responderás como un investigador experto respondiendo a la siguiente pregunta con el contenido proporcionado
"""

def get_transcription_list(videoId: str):
    return YouTubeTranscriptApi.list_transcripts(videoId)


class DataBaseConnection:
    def __init__(self, database_name="my_database", collection_name="my_collection"):

        self.API_KEY_YOUTUBE = "AIzaSyC_SSAcmJZgl_tBU4QuCnUpLCLikBOXkGI"
        self.API_KEY_OPENAI = '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'

        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.client_ = OpenAI(api_key=self.API_KEY_OPENAI)
        #################################################################################################################

        # self.MONGO_URI = "mongodb+srv://hveras1:GlDC38DAX913ZSIv@videoai.mkgw6wh.mongodb.net/?retryWrites=true&w=majority"
        self.MONGO_URI = "mongodb://127.0.0.1:27017/"
        self.DATABASE_NAME = database_name
        self.COLLECTION_NAME = collection_name
        self.similarity_threshold = 0.7
        try:
            self.client = MongoClient(self.MONGO_URI)
            self.db = self.client[self.DATABASE_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_resumen(self, transcription):

        completion = self.client_.chat.completions.create(
            model="gpt-3.5-turbo",
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": content_resumen},
                {"role": "user",
                 "content": transcription}
            ]
        )
        return completion.choices[0].message.content

    def get_chat(self, contenido, pregunta):

        completion = self.client_.chat.completions.create(
            model="gpt-3.5-turbo",
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": content_chat + " Contenido: " + contenido},
                {"role": "user",
                 "content": pregunta}
            ]
        )
        return completion.choices[0].message.content


    def get_full_video(self, video: models.VideoYoutube):

        # AGREGAR MÉTODO DE CONSULTA A LA BASE DE DATOS

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

    def search_video(self, palabra):
        try:
            pipeline = self.consulta(palabra)
            result = list(self.collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"Error inserting videos: {e}")

    def get_temario(self, peticion):
        completion = self.client_.chat.completions.create(
            model="gpt-3.5-turbo",
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": content_temario
                 },
                {"role": "user",
                 "content": peticion}
            ]
        )
        print(completion.choices[0].message.content)
        json_data = json.loads(completion.choices[0].message.content.replace('```json', '').replace('```', '').strip())
        print(json_data)
        return json_data

    def close(self):
        if self.client:
            self.client.close()

    def buscar_videos(self, palabra_clave, max_resultados=2):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.API_KEY_YOUTUBE)

        request = youtube.search().list(q=palabra_clave, part='id,snippet', maxResults=max_resultados)
        response = request.execute()

        return response.get("items", [])

    def get_temario_videos(self, temario: models.TemarioObject) -> models.TemarioObject:

        print(temario.aspectos[0].aspecto + "<----[aspecto]")

        for asp in temario.aspectos:

            lista_items = list()
            for tema in asp.temas:
                items = self.buscar_videos(tema + " " + temario.temaCentral + " " + asp.aspecto)

                for item in items:
                    etag = item['etag']
                    videoId = item['id']['videoId']
                    channelId = item['snippet']['channelId']
                    title = item['snippet']['title']
                    description = item['snippet']['description']
                    channelTitle = item['snippet']['channelTitle']
                    publishTime = item['snippet']['publishTime']
                    urlMiniatura = item['snippet']['thumbnails']['high']['url']

                    video_youtube = models.VideoYoutube(etag, videoId, channelId, title, description, channelTitle,
                                                        publishTime, urlMiniatura, transcription="", resume="")
                    lista_items.append(video_youtube)

            asp.videos = lista_items
            print(lista_items)

        return temario
