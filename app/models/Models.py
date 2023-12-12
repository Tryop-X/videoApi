from typing import List


class VideoYoutube:
    def __init__(self, etag: str, videoId: str, channelId: str, title: str, description: str, channelTitle: str,
                 publishTime: str, urlMiniatura: str, transcription="", resume=""):
        self.etag = etag
        self.videoId = videoId
        self.channelId = channelId
        self.title = title
        self.description = description
        self.channelTitle = channelTitle
        self.publishTime = publishTime
        self.urlMiniatura = urlMiniatura
        self.transcription = transcription
        self.resume = resume

    def to_dict(self):
        return {
            'etag': self.etag,
            'title': self.title,
            'videoId': self.videoId,
            'channelId': self.channelId,
            'publishTime': self.publishTime,
            'description': self.description,
            'channelTitle': self.channelTitle,
            'urlMiniatura': self.urlMiniatura,
            'transcription': self.transcription,
            'resume': self.resume,
        }


class Aspecto:
    def __init__(self, aspecto: str, temas: List[str], items: List[VideoYoutube]):
        self.aspecto = aspecto
        self.temas = temas
        self.videos = items

    def to_dict(self):
        return {
            'aspecto': self.aspecto,
            'temas': self.temas,
            'videos': [item.to_dict() for item in self.videos] if self.videos else []
        }


class Temario:
    def __init__(self, idTemario: str, temaCentral: str, aspectos: List[Aspecto], consulta: str):
        self.idTemario = idTemario
        self.temaCentral = temaCentral
        self.aspectos = aspectos
        self.consulta = consulta

    def to_dict(self):
        return {
            'idTemario': self.idTemario,
            'temaCentral': self.temaCentral,
            'consulta': self.consulta,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else [],
        }

    def to_dict_mongo(self, emb_tem, emb_cos):
        return {
            'temaCentral': self.temaCentral,
            'consulta': self.consulta,
            'temEmbedding': emb_tem,
            'cosEmbedding': emb_cos,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else [],
        }


def get_video_yout_by_item(item) -> VideoYoutube:
    etag = item['etag']
    videoId = item['id']['videoId']
    channelId = item['snippet']['channelId']
    title = item['snippet']['title']
    description = item['snippet']['description']
    channelTitle = item['snippet']['channelTitle']
    publishTime = item['snippet']['publishTime']
    urlMiniatura = item['snippet']['thumbnails']['high']['url']
    return VideoYoutube(etag, videoId, channelId, title, description, channelTitle,
                        publishTime, urlMiniatura, transcription="", resume="")


def get_video_from_mongo(video) -> VideoYoutube:
    return VideoYoutube(
        video['etag'],
        video['videoId'],
        video['channelId'],
        video['title'],
        video['description'],
        video['channelTitle'],
        video['publishTime'],
        video['urlMiniatura'],
        video['transcription'],
        video['resume']
    )


def get_aspecto_from_mongo(aspecto) -> Aspecto:
    return Aspecto(
        aspecto['aspecto'],
        aspecto['temas'],
        [get_video_from_mongo(video) for video in aspecto['videos']] if aspecto['videos'] else []
    )


def get_temario_from_mongo(tem) -> Temario:
    return Temario(
        str(tem['_id']),
        tem['temaCentral'],
        [get_aspecto_from_mongo(asp) for asp in tem['aspectos']] if tem['aspectos'] else [],
        tem['consulta']
    )
