from flask import Blueprint, request, Response
from threading import Thread
import requests
import os

from utils.polyrhythm_gen import polyrhythm_gen
from utils.slack_utils import send_file
from services.client import client

polyrhythm_gen_bp = Blueprint("polyrhythm_gen", __name__)

@polyrhythm_gen_bp.route('/polyrhythm-gen', methods=['POST'])
def polyrhythm_generation():
    data = request.form
    channel_id = data["channel_id"]
    user_id = data["user_id"]
    client.chat_postEphemeral(channel=channel_id, user=user_id, text="Working...")
    Thread(target=process_poly_gen, args=(data,)).start()
    return Response(), 200

def process_poly_gen(data):
    channel_id = data["channel_id"]
    user_id = data["user_id"]
    args = data.get('text').replace(" ", "").split("]")

    #getting args
    polyrhythm_arr = args[0].split(",")
    polyrhythm_arr[0] = polyrhythm_arr[0][1:]

    bpm = args[1]
    try:
        polyrhythm_arr = list(map(int, polyrhythm_arr))
        bpm = int(bpm)
    except ValueError:
        client.chat_postMessage(channel=channel_id, text="Bad input, use something like `[3,4,5] 120`.")
        print("Bad Input")
        return

    #generating the polyrhythm gif
    buf = polyrhythm_gen(polyrhythm_arr, bpm)

    if buf is None:
        client.chat_postMessage(channel=channel_id, text="Too many frames to generate, reduce input sizes.")
        print("Large Input")
        return
    buf.seek(0)
    buf_data = buf.getvalue()

    filename = f"Polyrhythm {bpm} {polyrhythm_arr}"

    with open("test.gif", "wb") as f:
        f.write(buf.getvalue())

    file_url = send_file(buf_data, filename)

    attachment_with_slack_url = {
        "title": filename,
        "image_url": file_url,
    }

    #Step 4: Send msg to the Slack channel
    response = client.chat_postMessage(
        channel=channel_id,
        text=f"Here's your polyrhythm!",
        attachments=[attachment_with_slack_url]
    )

    if response.status_code != 200:
        raise ValueError(
            f"Failed to send the message to Slack! Status code returned from the Slack API: {response.status_code}"
        )
