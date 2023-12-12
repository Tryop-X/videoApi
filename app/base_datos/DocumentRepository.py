from app.models import Document as models
from bson.objectid import ObjectId
from app.base_datos.date_base_conection import DataBaseConnection
from datetime import datetime
from typing import List


def get_date():
    fecha_actual = datetime.now()
    return fecha_actual.strftime('%d/%m/%Y %H:%M')


class DocumentRepository:
    def __init__(self):
        self.connection = DataBaseConnection()
        self.collection = self.connection.get_temario_document()

    def get_document_id_mongo(self, documentId) -> models.Document:
        document_mongo = self.collection.find_one({"_id": ObjectId(documentId)})
        return models.get_document_from_mongo(document_mongo)

    def get_document_by_user(self, idUsuario: str, idTemario: str):
        query = {"$and": [{"idUsuario": idUsuario}, {"idTemario": idTemario}]}
        documents_mongo = list(self.collection.find(query))
        documents = list()
        for doc in documents_mongo:
            d = models.get_document_from_mongo(doc)
            documents.append(d.to_dict())
        return documents

    def save_document(self, document: models.Document) -> models.Document:
        document.date = get_date()
        document_mongo = self.collection.insert_one(document.to_dict_mongo())
        document_mongo_id = str(document_mongo.inserted_id)
        document_updated = self.get_document_id_mongo(document_mongo_id)
        return document_updated

    def update_qualification(self, document: models.Document):
        myquery = {"_id": ObjectId(document.idDocument)}
        new_values = {"$set": {
            'qualification': document.qualification,
        }}
        self.collection.update_one(myquery, new_values)

    def save_document_values(
            self, idUsuario: str, idTemario: str, contend_pdf: str, temaCentral: str, citas: List[str]
    ) -> models.Document:
        document = models.Document(
            '',
            idUsuario=idUsuario,
            idTemario=idTemario,
            date=get_date(),
            contendPdf=contend_pdf,
            temaCentral=temaCentral,
            qualification=-1,
            citas=citas
        )
        document_mongo = self.collection.insert_one(document.to_dict_mongo())
        document_id = str(document_mongo.inserted_id)
        document_mongo = self.get_document_id_mongo(document_id)
        return document_mongo


