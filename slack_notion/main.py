import sys
import requests
import json

from fastapi import FastAPI, Body, Request, Depends
from sqlalchemy.orm import Session
import url
import config
from slack_api import SlackAPI

sys.path.append('/Users/hyungukkim/Desktop/Developments/test-folder/python-basic')
from db.connection import get_db
from db.repositories.china_character import get_china_character_name

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
    # print(request_body["event"]["text"])
    # print(request_body)

    # await set_message_notion(request_body["event"]["text"])
    return request_body["event"]["text"]


@app.post("/myname")
async def input_myname():
    channel_id = "U023VKA2PUJ"
    blocks = [
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "plain_text_input-action",
                "placeholder": {
                    "type": "plain_text",
                    "text": "ex) 炯旭 (성을 제외한 이름만 입력해주세요.)"
                },
            },
            "label": {
                "type": "plain_text",
                "text": "당신의 이름을 '한자'로 입력해 주세요.",
                "emoji": True,
            }
        }
    ]

    slack_client = SlackAPI(config.slack_bot_token)
    result = slack_client.post_message(
        channel_id=channel_id,
        text="나의이름은",
        blocks=blocks
    )
    return


@app.post("/interactive")
async def post_message(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    payload = json.loads(form_data.get("payload"))

    myname = payload["actions"][0]["value"]
    name_list = [myname[i:i+1] for i in range(len(myname))]

    result = await get_china_character_name(name_list, db)

    if not result:
        message = "멋진 이름입니다. 당신의 이름에는 불용한자가 없습니다!"
    else:
        name_text = ""
        for name in result:
            name_text = f"{name_text}불용한자는 [{name.cha_name},{name.kor_name}]이며, 이 한자는 {name.description}\n"

        message = f"당신의 이름 중 불용한자는 총 {len(result)}개 입니다...\n{name_text}\n\n부모님이 주신 소중한 이름, 재미로만 봐주세요 🥹"

    channel_id = "U023VKA2PUJ"
    slack_client = SlackAPI(config.slack_bot_token)
    slack_client.post_message(
        channel_id=channel_id,
        text=message,
    )

    return


async def set_message_notion(message: str):
    request_body = {"parent": {"database_id": "752bcc48aaa646be99b9a07676b32afc"}, "properties": {"Name": {"title": [{"text": {"content": message}}]}}}
    response = requests.post(url.database_url, headers={"Authorization": f"Bearer {config.notion_token}", "Notion-Version": "2022-02-22"}, json=request_body)
    print(response.text)
