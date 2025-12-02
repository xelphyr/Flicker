from services.client import client
from services.slack_events_adapter import slack_events_adapter

@slack_events_adapter.on("app_mention")
def handle_mention(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    client.chat_postMessage(channel=channel_id, text="Pong!")