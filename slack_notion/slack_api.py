from slack_sdk import WebClient


class SlackAPI:
    def __init__(self, token):
        self.client = WebClient(token)

    def post_message(self, channel_id: str, text: str = None, blocks = None):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            blocks=blocks,
        )
        return result