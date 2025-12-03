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
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="Format of the command: `/beat-gen <----------------> <grouping> <bpm> <type>`")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<---->`: Each dash represents a beat that you can add. For example: `x-x-`, or `---x---x---x---x`, or `x---x---x-x-`. You can imagine a metronome, and at each beat you move to the next dash. If the dash is actually an X, you play it out.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<grouping>`: This is how many dashes to play per beat. If the grouping were two and the bpm were 120, you'd have 4 notes every second, for example.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<bpm>`: The number of beats per minute. See <grouping> for more context.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<type>`: The bot supports `line` for now.")
    else:
        Thread(target=process_beat_gen, args=(data,)).start()
    return Response(), 200

def process_beat_gen(data):
    pass