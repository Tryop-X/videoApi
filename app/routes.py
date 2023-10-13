from flask import Blueprint, jsonify, request
from app.services import videoRepository as videoDb
from bson import json_util

bp = Blueprint('routes', __name__)


@bp.route('/get_video', methods=['GET'])
def get_video():
    consulta = request.args.get('consulta')
    vid = videoDb.DataBaseConnection(database_name="videoCollection", collection_name="video")
    video = vid.search_video(consulta)
    print(video, '<-----')
    video_json = json_util.dumps(video)

    return video_json, 200, {'ContentType': 'application/json'}