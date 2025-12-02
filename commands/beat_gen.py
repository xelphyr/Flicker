from flask import Blueprint, request, Response
from threading import Thread
import requests
import os

from utils.polyrhythm_gen import polyrhythm_gen
from services.client import client

beat_gen_bp = Blueprint("beat_gen_bp", __name__)

@beat_gen_bp.route('/beat-gen', methods=['POST'])
def beat_generation():
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")
    if text is None or text == "":
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="Format of the command: `/beat-gen <----------------> <grouping> <bpm>`")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="Each dash represents a beat that you generate from ")
    return Response(), 200