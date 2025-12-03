from flask import Blueprint, request, Response
from threading import Thread
import requests
import os

from utils.beat_gen import beat_gen
from utils.slack_utils import send_file
from services.client import client

beat_gen_bp = Blueprint("beat_gen_bp", __name__)

@beat_gen_bp.route('/beat-gen', methods=['POST'])
def beat_generation():
    data = request.form
    channel_id = data.get("channel_id")
    user_id = data.get("user_id")
    text = data.get("text")
    if text is None or text == "":
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="Format of the command: `/beat-gen <beatmap> <grouping> <bpm> <type>`")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<beatmap>`: In the format of `------`, where each dash represents a beat that you can add. For example: `x-x-`, or `---x---x---x---x`, or `x---x---x-x-`. You can imagine a metronome, and at each beat you move to the next dash. If the dash is actually an X, you play it out.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<grouping>`: This is how many dashes to play per beat. If the grouping were two and the bpm were 120, you'd have 4 notes every second, for example.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<bpm>`: The number of beats per minute. See <grouping> for more context.")
        client.chat_postEphemeral(channel=channel_id, user=user_id, text="`<type>`: The bot supports `line` for now.")
    else:
        Thread(target=process_beat_gen, args=(data,)).start()
    return Response(), 200

def process_beat_gen(data):
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    args = data.get('text').split(" ")

    try:
        beatmap = args[0]
        grouping = args[1]
        bpm = args[2]
        kind = args[3]

        grouping = int(grouping)
        bpm = int(bpm)

        if kind not in ['line']:
            raise ValueError
    except IndexError:
        return
    except ValueError:
        return

    buf = beat_gen(beatmap, grouping, bpm, kind)

    if buf is None:
        client.chat_postMessage(channel=channel_id, text="Too many frames to generate, reduce input sizes.")
        print("Large Input")
        return
    buf.seek(0)
    buf_data = buf.getvalue()

    filename = f"Beatmap BPM:{bpm} Grouping:{grouping}"

    file_url = send_file(buf_data, filename)

    attachment_with_slack_url = {
        "title": filename,
        "image_url": file_url,
    }

    #Step 4: Send msg to the Slack channel
    response = client.chat_postMessage(
        channel=channel_id,
        text=f"Here's your beat!",
        attachments=[attachment_with_slack_url]
    )

    if response.status_code != 200:
        raise ValueError(
            f"Failed to send the message to Slack! Status code returned from the Slack API: {response.status_code}"
        )





