import requests

from fastapi import FastAPI
from fastapi import Body
import url
import config
from slack_api import SlackAPI

app = FastAPI()


# URL Setting
# @app.post("/message")
# async def post_message(request_body: dict = Body(...)):
#     response = {"challenge": request_body["challenge"]}
#     print(response)
#     return response


# Notion API
# @app.post("/message")
# async def post_message(request_body: dict = Body(...)):
#     print(request_body["event"]["text"])
#
#     await set_message_notion(request_body["event"]["text"])
#     return request_body["event"]["text"]


# CHA Character
@app.post("/message")
async def post_message(request_body: dict = Body(...)):
    print(request_body["event"]["text"])

    await set_message_notion(request_body["event"]["text"])
    return request_body["event"]["text"]


@app.post("/myname")
async def input_myname():
    channel_id = "U023VKA2PUJ"

    slack_client = SlackAPI(config.slack_bot_token)
    result = slack_client.post_message(
        channel_id=channel_id,
        text="Hello world"
    )

    return "result"


async def set_message_notion(message: str):
    request_body = {"parent": {"database_id": "752bcc48aaa646be99b9a07676b32afc"}, "properties": {"Name": {"title": [{"text": {"content": message}}]}}}
    response = requests.post(url.database_url, headers={"Authorization": f"Bearer {config.notion_token}", "Notion-Version": "2022-02-22"}, json=request_body)
    print(response.text)
