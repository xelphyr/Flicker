from slack_sdk import WebClient
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from polyrhythm_gen import polyrhythm_gen
from threading import Thread
import requests

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)
client = WebClient(token=os.environ['SLACK_TOKEN'])

@slack_events_adapter.on("app_mention")
def handle_mention(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    client.chat_postMessage(channel=channel_id, text="pong! Also: " + text)

@app.route('/polyrhythm-gen', methods=['POST'])
def polyrhythm_generation():
    data = request.form
    channel_id = data["channel_id"]
    client.chat_postMessage(channel=channel_id, text="Working...")
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

    with open("test1.gif", "wb") as f:
        f.write(buf.getvalue())

    # Step 1: Getting the URL
    buf_data_size = len(buf_data)
    upload_url = client.files_getUploadURLExternal(
        token = os.environ['SLACK_TOKEN'],
        filename=f"polyrhythm_{bpm}.gif",
        length = buf_data_size
    )

    if upload_url["ok"]:
        for item in upload_url:
            print(f"{item}")
    else:
        raise ValueError(
            f"Failed to get the URL for uploading the attachment to Slack! Response: {upload_url}"
        )

    #Step 2: Upload file to URL

    payload = {
        "filename": f"polyrhythm{bpm}.gif",
        "token": os.environ['SLACK_TOKEN']
    }
    response= requests.post(
        upload_url["upload_url"], params=payload, data=buf_data
    )

    if response.status_code == 200:
        print(
            f"Response from Slack: {response.status_code}, {response.text}"
        )
    else:
        raise ValueError(
            f"Response from Slack: {response.status_code}, {response.text}, {response.headers}"
        )

    file_id = upload_url["file_id"]

    #Step 3: Make file accessible in channel
    file_info = client.files_completeUploadExternal(
        files=[{
            "id": file_id,
            "title": f"Polyrhythm {bpm} {polyrhythm_arr}"
        }],
        channel_id = os.environ['BASE_CHANNEL'],
        initial_comment=None,
        thread_ts=None,
    )

    info = client.files_info(file=file_id)
    file_url = info["file"]["url_private"]

    attachment_with_slack_url = {
        "title": "Attachment",
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

if __name__ == '__main__':
    app.run(debug=True)