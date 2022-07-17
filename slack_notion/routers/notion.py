import sys, os
import requests

from fastapi import APIRouter, Body

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from slack_notion import url
from slack_notion import config


router = APIRouter(
    prefix="/notion",
    tags=["notion"],
)

# URL Setting
# @router.post("/message")
# async def post_message(request_body: dict = Body(...)):
#     response = {"challenge": request_body["challenge"]}
#     print(response)
#     return response


# Notion API
# @router.post("/message")
# async def post_message(request_body: dict = Body(...)):
#     print(request_body["event"]["text"])
#
#     await set_message_notion(request_body["event"]["text"])
#     return request_body["event"]["text"]


# CHA Character
@router.post("/message")
async def post_message(request_body: dict = Body(...)):
    # print(request_body["event"]["text"])
    # print(request_body)

    # await set_message_notion(request_body["event"]["text"])
    return request_body["event"]["text"]


async def set_message_notion(message: str):
    request_body = {"parent": {"database_id": "752bcc48aaa646be99b9a07676b32afc"}, "properties": {"Name": {"title": [{"text": {"content": message}}]}}}
    response = requests.post(url.database_url, headers={"Authorization": f"Bearer {config.notion_token}", "Notion-Version": "2022-02-22"}, json=request_body)
    print(response.text)
