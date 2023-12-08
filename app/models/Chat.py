from typing import List
from bson.objectid import ObjectId


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
    def __init__(self, idChat: str, date: str, conversation: List[ResQues]):
        self.idChat = idChat
        self.date = date
        self.conversation = conversation

    def to_dict(self):
        return {
            'date': self.date,
            'aspectos': [con.to_dict() for con in self.conversation] if self.conversation else None,
        }

def get_resques_from_mongo(resques) -> ResQues:
    return ResQues(
        resques['response'],
        resques['question'],
        resques['date']
    )

def get_chat_from_mongo(chat) -> Chat:
    return Chat(
        str(chat['_id']),
        chat['date'],
        [get_resques_from_mongo(conv) for conv in chat['conversation']] if chat['conversation'] else []
    )
