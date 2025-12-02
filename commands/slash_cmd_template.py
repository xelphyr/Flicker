from flask import Blueprint, request, Response

bp = Blueprint("bp", __name__)

@bp.route('/default', methods=['POST'])
def beat_generation():
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    return Response(), 200