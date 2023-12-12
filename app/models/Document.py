from typing import List


class Document:
    def __init__(self, idDocument: str, idUsuario: str,
                 idTemario: str, date: str, contendPdf: str,
                 temaCentral: str, qualification: int, citas: List[str]):
        self.idDocument = idDocument
        self.idUsuario = idUsuario
        self.idTemario = idTemario
        self.contendPdf = contendPdf
        self.date = date
        self.qualification = qualification
        self.citas = citas
        self.temaCentral = temaCentral

    def to_dict(self):
        return {
            'idDocument': self.idDocument,
            'idUsuario': self.idUsuario,
            'idTemario': self.idTemario,
            'temaCentral': self.temaCentral,
            'contendPdf': self.contendPdf,
            'qualification': self.qualification,
            'citas': self.citas,
            'date': self.date,
        }

    def to_dict_mongo(self):
        return {
            'idUsuario': self.idUsuario,
            'idTemario': self.idTemario,
            'date': self.date,
            'contendPdf': self.contendPdf,
            'temaCentral': self.temaCentral,
            'qualification': self.qualification,
            'citas': self.citas,
        }


def get_document_from_mongo(document) -> Document:
    return Document(
        str(document['_id']),
        document['idUsuario'],
        document['idTemario'],
        document['date'],
        document['contendPdf'],
        document['temaCentral'],
        document['qualification'],
        document['citas']
    )

