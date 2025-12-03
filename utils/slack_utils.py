import os
import requests

from services.client import client


def send_file(buf_data, filename):
    # Step 1: Getting the URL
    buf_data_size = len(buf_data)
    upload_url = client.files_getUploadURLExternal(
        token = os.environ['SLACK_TOKEN'],
        filename=filename,
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
        "filename": filename,
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
            "title": filename
        }],
        channel_id = os.environ['BASE_CHANNEL'],
        initial_comment=None,
        thread_ts=None,
    )

    info = client.files_info(file=file_id)
    file_url = info["file"]["url_private"]

    return file_url
