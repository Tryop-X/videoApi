from typing import List

class Thumbnail:
    def __init__(self, url: str, width: int, height: int):
        self.url = url
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            'url': self.url,
            'width': self.width,
            'height': self.height
        }

class Thumbnails:
    def __init__(self, default: Thumbnail, medium: Thumbnail, high: Thumbnail):
        self.default = default
        self.medium = medium
        self.high = high

    def to_dict(self):
        return {
            'default': self.default.to_dict(),
            'medium': self.medium.to_dict(),
            'high': self.high.to_dict()
        }

class Snippet:
    def __init__(self, publishedAt: str, channelId: str, title: str, description: str, thumbnails: Thumbnails, channelTitle: str, liveBroadcastContent: str, publishTime: str):
        self.publishedAt = publishedAt
        self.channelId = channelId
        self.title = title
        self.description = description
        self.thumbnails = thumbnails
        self.channelTitle = channelTitle
        self.liveBroadcastContent = liveBroadcastContent
        self.publishTime = publishTime

    def to_dict(self):
        return {
            'publishedAt': self.publishedAt,
            'channelId': self.channelId,
            'title': self.title,
            'description': self.description,
            'thumbnails': self.thumbnails.to_dict(),
            'channelTitle': self.channelTitle,
            'liveBroadcastContent': self.liveBroadcastContent,
            'publishTime': self.publishTime
        }

class Id:
    def __init__(self, kind: str, videoId: str):
        self.kind = kind
        self.videoId = videoId

    def to_dict(self):
        return {
            'kind': self.kind,
            'videoId': self.videoId
        }

class Item:
    def __init__(self, kind: str, etag: str, id: Id, snippet: Snippet):
        self.kind = kind
        self.etag = etag
        self.id = id
        self.snippet = snippet

    def to_dict(self):
        return {
            'kind': self.kind,
            'etag': self.etag,
            'id': self.id.to_dict(),
            'snippet': self.snippet.to_dict()
        }

class PageInfo:
    def __init__(self, totalResults: int, resultsPerPage: int):
        self.totalResults = totalResults
        self.resultsPerPage = resultsPerPage

    def to_dict(self):
        return {
            'totalResults': self.totalResults,
            'resultsPerPage': self.resultsPerPage
        }

class YoutubeObject:
    def __init__(self, kind: str, etag: str, nextPageToken: str, regionCode: str, pageInfo: PageInfo, items: List[Item]):
        self.kind = kind
        self.etag = etag
        self.nextPageToken = nextPageToken
        self.regionCode = regionCode
        self.pageInfo = pageInfo
        self.items = items

    def to_dict(self):
        return {
            'kind': self.kind,
            'etag': self.etag,
            'nextPageToken': self.nextPageToken,
            'regionCode': self.regionCode,
            'pageInfo': self.pageInfo.to_dict(),
            'items': [item.to_dict() for item in self.items] if self.items else None
        }

class Aspecto:
    def __init__(self, aspecto: str, temas: List[str]):
        self.aspecto = aspecto
        self.temas = temas

    def to_dict(self):
        return {
            'aspecto': self.aspecto,
            'temas': self.temas
        }

class TemarioObject:
    def __init__(self, temaCentral: str, aspectos: List[Aspecto], items: List[Item]):
        self.temaCentral = temaCentral
        self.aspectos = aspectos
        self.items = items

    def to_dict(self):
        return {
            'temaCentral': self.temaCentral,
            'aspectos': [aspecto.to_dict() for aspecto in self.aspectos] if self.aspectos else None,
            'items': [item.to_dict() for item in self.items] if self.items else None
        }


