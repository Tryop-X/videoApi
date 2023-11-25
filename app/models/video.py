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
            'resume': self.resume
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
            'videos': [item.to_dict() for item in self.videos] if self.videos else None
        }

class TemarioObject:
    def __init__(self, temaCentral: str, aspectos: List[Aspecto]):
        self.temaCentral = temaCentral
        self.aspectos = aspectos

    def to_dict(self):
        return {
            'temaCentral': self.temaCentral,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else None,
        }


