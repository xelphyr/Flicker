import requests

class SlackBot:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    def send_message(self, message: str):
        message_payload = {
            "text": message,
        }
        try:
            response = requests.post(self.webhook_url, json=message_payload)
            if response.status_code == 200:
                print("Message was sent successfully to slack")
            else:
                print("Message was not sent to slack, status_code:", response.status_code)
        except Exception as e:
            print("An exception occurred while sending a slack message", e)

slack_bot = SlackBot("")