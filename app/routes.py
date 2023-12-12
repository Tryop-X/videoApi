from flask import Blueprint, jsonify, request, send_file
from app.services import videoRepository as videoDb
from app.models import Models as models, Document as doc

bp = Blueprint('routes', __name__)
vid = videoDb.VideoRepository()


@bp.route('/get_temario', methods=['POST'])
def get_temario():
    datos = request.get_json()
    if not datos or 'consulta' not in datos:
        return jsonify({'message': 'No se proporcionó consulta'}), 400
    try:
        consulta = datos['consulta']
        token = datos['token']
        temario_data = vid.get_temario(consulta, token)
        return temario_data.to_dict(), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return {"message": str(e)}, 400, {'ContentType': 'application/json'}


@bp.route('/get_resumen', methods=['POST'])
def get_resumen():
    data = request.get_json()
    if not data or 'videoId' not in data:
        return jsonify({'message': 'No se proporcionó consulta'}), 400
    try:
        datos = vid.get_video_with_trans_resume(data['idTemario'], data['videoId'])
        return datos.to_dict(), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/chatear', methods=['POST'])
def get_chatear():

    data = request.get_json()
    if 'videoSelected' not in data or 'idTemario' not in data or 'token' not in data:
        return jsonify({'message': 'no se proporcionaron los datos necesarios para generar el documento'}), 400
    if len(data['videoSelected']) <= 0:
        return jsonify({'message': 'No se han seleccionado vídeos para generar el archivo'}), 400
    try:
        rpta = vid.get_chat(data['idTemario'], data['videoSelected'], data['token'], data['pregunta'], data['idChat'])
        respuesta = {
            'respuesta': rpta
        }
        return respuesta, 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/get_conversation', methods=['POST'])

def get_conversation():
    data_conv = request.get_json()
    if 'idTemario' not in data_conv or 'token' not in data_conv:
        return jsonify({'message': 'no se proporcionaron los datos necesarios para generar el documento'}), 400
    try:
        conversation = vid.get_chat_conversation(data_conv['idTemario'], data_conv['token'])
        return conversation, 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/generar_doc', methods=['POST'])
def generar_doc():
    json_data = request.get_json()
    if 'videoSelected' not in json_data or 'id_temario' not in json_data or 'token' not in json_data:
        return jsonify({'message': 'no se proporcionaron los datos necesarios para generar el documento'}), 400
    if len(json_data['videoSelected']) <= 0:
        return jsonify({'message': 'No se han seleccionado vídeos para generar el archivo'}), 400
    try:
        vid.set_pdf_document(json_data['id_temario'], json_data['videoSelected'], json_data['token'])
        return send_file('../temporal.pdf', as_attachment=True, download_name='systematic_review.pdf')
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    if 'usuario' not in datos or 'contrasegna' not in datos:
        return jsonify({'message': 'no se proporcionaron los datos de inicio de sesión'}), 400
    try:
        response = vid.login(datos['usuario'], datos['contrasegna'])
        return response, 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/get_documents', methods=['POST'])
def get_documents():
    datos = request.get_json()
    if 'token' not in datos or 'idTemario' not in datos:
        return jsonify({'message': 'no se proporcionaron los datos de inicio de sesión'}), 400
    try:
        response = vid.get_documents(datos['token'], datos['idTemario'])
        return response, 200, {'ContentType': 'application/json'}
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/get_document', methods=['POST'])
def get_document():
    datos = request.get_json()
    if 'idDocument' not in datos:
        return jsonify({'message': 'no se proporcionaron los datos de inicio de sesión'}), 400
    try:
        datos['_id'] = datos['idDocument']
        vid.get_document(doc.get_document_from_mongo(datos))
        return send_file('../temporal.pdf', as_attachment=True, download_name='systematic_review.pdf')
    except Exception as e:
        return jsonify({'message': str(e)}), 400
