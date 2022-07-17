from slack_sdk import WebClient


class SlackAPI:
    def __init__(self, token):
        self.client = WebClient(token)

    def plain_text_input(self, label_text: str, place_holder: str = ""):
        blocks = [
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": place_holder
                    },
                },
                "label": {
                    "type": "plain_text",
                    "text": label_text,
                    "emoji": True,
                }
            }
        ]
        return blocks

    def post_message(self, channel_id: str, text: str = None, blocks = None):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            blocks=blocks,
        )
        return result