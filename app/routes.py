from flask import Blueprint, jsonify, request
from app.services import videoRepository as videoDb
from app.models import Models as models
import json

bp = Blueprint('routes', __name__)

vid = videoDb.VideoRepository()


@bp.route('/get_temario', methods=['POST'])
def get_temario():

    datos = request.get_json()
    if not datos or 'consulta' not in datos:
        return jsonify({'error': 'No se proporcionó consulta'}), 400
    consulta = datos['consulta']

    hay_video, temario_data = vid.get_temario(consulta)

    if hay_video:
        temario_response = temario_data
    else:
        temario_response = vid.get_temario_videos(temario_data, hay_video)

    return temario_response.to_dict(), 200, {'ContentType': 'application/json'}


@bp.route('/get_resumen', methods=['POST'])
def get_resumen():

    data = request.get_json()

    # Asegúrate de que el JSON contenga la clave 'consulta'
    if not data or 'video' not in data:
        return jsonify({'error': 'No se proporcionó consulta'}), 400

    video = data['video']

    video_model = models.VideoYoutube(
        video.get('etag'),
        video.get('videoId'),
        video.get('channelId'),
        video.get('title'),
        video.get('description'),
        video.get('channelTitle'),
        video.get('publishTime'),
        video.get('urlMiniatura')
    )

    datos = vid.get_video_with_trans_resume(video_model)

    return datos.to_dict(), 200, {'ContentType': 'application/json'}


@bp.route('/chatear', methods=['POST'])
def get_chatear():

    json_temario = request.get_json()

    pregunta = json_temario['pregunta']
    temario = json_temario['temario']

    aspectos_list = [models.Aspecto(aspecto['aspecto'], aspecto['temas'],
                                    [models.VideoYoutube(
                                        video.get('etag'),
                                        video.get('videoId'),
                                        video.get('channelId'),
                                        video.get('title'),
                                        video.get('description'),
                                        video.get('channelTitle'),
                                        video.get('publishTime'),
                                        video.get('urlMiniatura'),
                                        video.get('transcription'),
                                        video.get('resume'),
                                    ) for video in aspecto.get('videos')]

                                    ) for aspecto in temario['aspectos']]

    temario_object = models.TemarioObject("", temario['temaCentral'], aspectos_list, [], temario['consulta'])

    contenido = temario_object.temaCentral + "\n"

    hayResumenTotal = False

    for asp in temario_object.aspectos:

        hayResumen = False
        resumen = ""
        for vide in asp.videos:
            if vide.resume != "":
                hayResumen = True
                hayResumenTotal = True
                resumen += "TÍTULO: " + vide.title + "\n"
                resumen += vide.resume + "\n"
        if hayResumen:
            contenido += asp.aspecto + "\n"
            contenido += resumen + "\n"

    rpta = ""
    if hayResumenTotal:
        print(contenido)
        rpta = vid.get_chat(contenido, pregunta)

    respuesta = {
        'respuesta': rpta
    }

    return respuesta, 200, {'ContentType': 'application/json'}


