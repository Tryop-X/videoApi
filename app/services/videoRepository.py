from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from app.models import Models as models, datos as dt, Document as doc
import app.models.Models as mod
from app.emb.EmbeddingService import EmbeddingService
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from app.base_datos.TemarioRepository import TemarioRepository
from app.base_datos.ChatRepository import ChatRepository
from app.base_datos.UsuarioRepository import UsuarioRepository
from app.base_datos.DocumentRepository import DocumentRepository
from app.services.OpenAI_service import OpenAIService
from datetime import datetime

embeddings_service = EmbeddingService()


def get_transcription_list(videoId: str):
    return YouTubeTranscriptApi.list_transcripts(videoId)


def get_date():
    fecha_actual = datetime.now()
    return fecha_actual.strftime('%d/%m/%Y %H:%M:%S')


class VideoRepository:
    def __init__(self):
        self.openAIService = OpenAIService()
        self.temarioRepository = TemarioRepository()
        self.chatRepository = ChatRepository()
        self.usuarioRepository = UsuarioRepository()
        self.documentRepository = DocumentRepository()

    def get_video_with_trans_resume(self, id_temario: str, videoId: str):
        try:
            transcription = get_transcription_list(videoId)
            transcript = None
            for t in transcription:
                transcript = t.fetch()
                break
            trans = ""
            for entry in transcript:
                trans = trans + entry['text'] + " "
            temario = self.temarioRepository.get_temario_id_mongo(id_temario)
            video = self.update_video_obj(temario=temario, idVideo=videoId, transcription=trans)
            return video
        except Exception as e:
            raise ValueError(e)

    def get_temario(self, peticion: str, token: str):
        hay_video, temario = self.temarioRepository.get_temario_by_embedding(peticion)
        if hay_video:
            self.usuarioRepository.update_temarios(token, temario.idTemario)
            return temario
        else:
            temario_object = self.openAIService.get_temario(peticion)
            temario_object = self.get_temario_videos(temario_object)
            self.usuarioRepository.update_temarios(token, temario_object.idTemario)
            return temario_object

    def buscar_videos(self, consulta, max_resultados=6):
        youtube = build(dt.YOUTUBE_API_SERVICE_NAME, dt.YOUTUBE_API_VERSION, developerKey=dt.API_KEY_YOUTUBE)
        request = youtube.search().list(q=consulta, part='id,snippet', maxResults=max_resultados, type='video')
        response = request.execute()
        return response.get("items", [])

    def update_video_obj(self, temario: models.Temario, idVideo: str, transcription: str):
        for asp in temario.aspectos:
            for vid in asp.videos:
                if vid.videoId == idVideo:
                    if vid.resume == "":
                        vid.transcription = transcription
                        vid.resume = self.openAIService.get_resumen(temario.temaCentral, asp.aspecto, transcription)
                        self.temarioRepository.update_aspectos(temario)
                    return vid
        return None

    def get_temario_videos(self, temario: models.Temario) -> models.Temario:
        for asp in temario.aspectos:
            lista_items = list()
            items = self.buscar_videos(temario.temaCentral + " " + asp.aspecto)
            for item in items:
                video_youtube = mod.get_video_yout_by_item(item)
                lista_items.append(video_youtube)
            asp.videos = lista_items
        temario_saved = self.temarioRepository.save_temario(temario)
        return temario_saved

    def get_sub_temas(self, temario: models.Temario, videoSelected: List[str]):
        contenido = ""
        sub_temas = ""
        for aspec in temario.aspectos:
            content_tema = ""
            sub_temas += aspec.aspecto
            for video in aspec.videos:
                if video.videoId in videoSelected:
                    content_tema += "Autor: " + video.channelTitle + " | fecha publicación: " + video.publishTime + "\n"
                    content_tema += f"Fuente: https://www.youtube.com/watch?v={video.videoId}" + "\n"
                    content_tema += f"Título: {video.title}" + "\n"

                    if len(video.resume) <= 0:
                        vid_new = self.get_video_with_trans_resume(id_temario=temario.idTemario, videoId=video.videoId)
                        content_tema += vid_new.resume + "\n"
                    else:
                        content_tema += video.resume + "\n\n"
            if len(content_tema) > 0:
                content_tema = "subtema: " + aspec.aspecto + "\n" + content_tema
            contenido = contenido + content_tema
        return sub_temas, contenido

    def set_pdf_document(self, id_temario: str, videoSelected: List[str], token: str):
        temario = self.temarioRepository.get_temario_id_mongo(id_temario)
        sub_temas, contenido = self.get_sub_temas(temario, videoSelected)
        content_pdf = self.get_pdf_content(temario.temaCentral, sub_temas, contenido)
        # content_pdf = "contenido de prueba"
        self.documentRepository.save_document_values(
            idUsuario=token,
            idTemario=temario.idTemario,
            contend_pdf=content_pdf,
            temaCentral=temario.temaCentral,
            citas=videoSelected
        )
        usuario = self.usuarioRepository.get_usuario_id_mongo(token)
        self.build_document(temario.temaCentral, content_pdf, usuario.nombreCompleto)

    def get_documents(self, token: str, idTemario: str):
        return self.documentRepository.get_document_by_user(token, idTemario)

    def get_document(self, document: doc.Document):
        document_mongo = self.documentRepository.get_document_id_mongo(document.idDocument)
        if document_mongo.qualification != document.qualification:
            self.documentRepository.update_qualification(document)
        usuario = self.usuarioRepository.get_usuario_id_mongo(document_mongo.idUsuario)
        self.build_document(document.temaCentral, document_mongo.contendPdf, usuario.nombreCompleto)

    def build_document(self, temaCentral: str, content_pdf: str, nombre_usuario: str):
        doc = SimpleDocTemplate("temporal.pdf", pagesize=letter)
        styles = getSampleStyleSheet()

        centered_bold_style = ParagraphStyle(
            'CenteredBold',
            parent=styles['BodyText'],
            fontName='Helvetica-Bold',
            fontSize=12,
            alignment=TA_CENTER,
        )

        centered_style = ParagraphStyle(
            'Centered',
            parent=styles['BodyText'],
            fontSize=10,
            alignment=TA_CENTER,
        )

        flow_ables = []
        line = dt.title_tema + " " + temaCentral.upper()
        para = Paragraph(line.strip(), centered_bold_style)
        flow_ables.append(para)

        info = dt.label_info + nombre_usuario + '.'
        labels = info.split('\n')
        for line in labels:
            para = Paragraph(line.strip(), centered_style)
            flow_ables.append(para)

        lines = content_pdf.split('\n')
        for line in lines:
            para = Paragraph(line.strip(), styles["BodyText"])
            flow_ables.append(para)

        flow_ables.append(PageBreak())
        doc.build(flow_ables)

    def get_pdf_content(self, temaCentral: str, sub_temas: str, contenido: str):
        if len(contenido) > 0:
            contenido = "Tema Central: " + temaCentral.upper() + "\n" + contenido
            content_pdf = self.openAIService.get_pdf_content(
                tema_central=temaCentral,
                sub_temas=sub_temas,
                content=contenido
            )
        else:
            content_pdf = ""
        return content_pdf

    def login(self, usuario: str, contrasegna: str):
        try:
            usuario = self.usuarioRepository.login_usuario(usuario, contrasegna)
            temarios = list()
            for idTemario in usuario.temarios:
                tem = self.temarioRepository.get_temario_id_mongo(idTemario)
                temarios.append(tem.to_dict())
            response = {"token": usuario.idUsuario, "temarios": temarios if temarios else []}
            return response
        except Exception as e:
            raise ValueError(e)

    def get_chat(self, id_temario: str, videoSelected: List[str], token: str, pregunta: str, idChat: str):
        temario = self.temarioRepository.get_temario_id_mongo(id_temario)
        sub_temas, contenido = self.get_sub_temas(temario, videoSelected)
        print(contenido)
        respuesta = self.openAIService.get_chat(contenido=contenido, pregunta=pregunta)
        self.chatRepository.update_chat_usuario(idChat, pregunta, respuesta)
        return respuesta

    def get_chat_conversation(self, id_temario: str, token: str):
        chat = self.chatRepository.save_get_chat(token, id_temario)
        return chat.to_dict()
