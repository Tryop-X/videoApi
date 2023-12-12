from app.models import Models as models, datos as dt
from openai import OpenAI
import json


class OpenAIService:
    def __init__(self):
        self.client_open_ai = OpenAI(api_key=dt.API_KEY_OPENAI)

    def get_resumen(self, tema, sub_temas, transcription):

        completion = self.client_open_ai.chat.completions.create(
            model=dt.model_resumen,
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": dt.get_contenido(tema, sub_temas)},
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

    def get_temario(self, peticion) -> models.Temario:
        try:
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
            json_data = json.loads(completion.choices[0].message.content
                                   .replace('```json', '')
                                   .replace('```', '')
                                   .strip())
            aspectos_list = [models.Aspecto(aspecto['aspecto'], aspecto['temas'], []) for aspecto in
                             json_data['aspectos']]
            temario_object = models.Temario("", json_data['temaCentral'], aspectos_list, peticion)
            return temario_object
        except Exception as e:
            print(f"Error consultado Temario: {e}")

    def get_pdf_content(self, tema_central: str, sub_temas: str, content: str):
        completion = self.client_open_ai.chat.completions.create(
            model=dt.model_pdf,
            stop=["END"],
            messages=[
                {"role": "system",
                 "content": dt.get_pdf_text(tema_central, sub_temas)},
                {"role": "user",
                 "content": content}
            ]
        )
        return completion.choices[0].message.content