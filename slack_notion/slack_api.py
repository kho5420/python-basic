from slack_sdk import WebClient


class SlackAPI:
    def __init__(self, token):
        self.client = WebClient(token)

    def post_message(self, channel_id, text):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
        return result