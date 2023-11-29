from typing import List
from bson.objectid import ObjectId


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


class ResQues:
    def __init__(self, response: str, question: str, date: str):
        self.response = response
        self.question = question
        self.date = date

    def to_dict(self):
        return {
            'response': self.response,
            'question': self.question,
            'date': self.date,
        }



class Chat:
    def __init__(self, date: str, conversation: List[ResQues]):
        self.date = date
        self.conversation = conversation

    def to_dict(self):
        return {
            'date': self.date,
            'aspectos': [con.to_dict() for con in self.conversation] if self.conversation else None,
        }

class TemarioObject:
    def __init__(self, _id_temario: str, temaCentral: str, aspectos: List[Aspecto], chats: List[Chat], consulta: str):
        self._id_temario = _id_temario
        self.temaCentral = temaCentral
        self.aspectos = aspectos
        self.chats = chats
        self.consulta = consulta

    def to_dict(self):
        return {
            '_id_temario': self._id_temario,
            'temaCentral': self.temaCentral,
            'consulta': self.consulta,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else [],
            'chats': [chat.to_dict() for chat in self.chats] if self.chats else [],
        }

    def to_dict_mongo(self, emb_tem, emb_cos):
        return {
            'temaCentral': self.temaCentral,
            'consulta': self.consulta,
            'temEmbedding': emb_tem,
            'cosEmbedding': emb_cos,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else [],
            'chats': [chat.to_dict() for chat in self.chats] if self.chats else [],
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


def get_resques_from_mongo(resques) -> ResQues:
    return ResQues(
        resques['response'],
        resques['question'],
        resques['date']
    )


def get_chat_from_mongo(chat) -> Chat:
    return Chat(
        chat['date'],
        [get_resques_from_mongo(conv) for conv in chat['conversation']] if chat['conversation'] else []
    )


def get_temario_from_mongo(tem) -> TemarioObject:
    return TemarioObject(
        str(tem['_id']),
        tem['temaCentral'],
        [get_aspecto_from_mongo(asp) for asp in tem['aspectos']] if tem['aspectos'] else [],
        [get_chat_from_mongo(chat) for chat in tem['chats']] if tem['chats'] else [],
        tem['consulta']
    )
