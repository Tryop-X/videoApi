from pymongo import MongoClient


class DataBaseConnection:
    def __init__(self, database_name="my_database", collection_name="my_collection"):
        self.MONGO_URI = "mongodb+srv://hveras1:GlDC38DAX913ZSIv@videoai.mkgw6wh.mongodb.net/?retryWrites=true&w=majority"
        self.DATABASE_NAME = database_name
        self.COLLECTION_NAME = collection_name
        try:
            self.client = MongoClient(self.MONGO_URI)
            self.db = self.client[self.DATABASE_NAME]
            self.collection = self.db[self.COLLECTION_NAME]
        except Exception as e:
            print(f"Error connecting to database: {e}")

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
