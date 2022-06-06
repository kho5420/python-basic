import requests

from fastapi import FastAPI
from fastapi import Body
import url
import config

app = FastAPI()


@app.post("/")
async def post_message(request_body: dict = Body(...)):
    print(request_body["event"]["text"])

    await set_message_notion(request_body["event"]["text"])
    return request_body["event"]["text"]


async def set_message_notion(message: str):
    request_body = {"parent": {"database_id": "752bcc48aaa646be99b9a07676b32afc"}, "properties": {"Name": {"title": [{"text": {"content": message}}]}}}
    response = requests.post(url.database_url, headers={"Authorization": f"Bearer {config.notion_token}", "Notion-Version": "2022-02-22"}, json=request_body)
    print(response.text)
