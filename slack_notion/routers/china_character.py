import sys, os
import json

from fastapi import Request, Depends, APIRouter
from sqlalchemy.orm import Session
from korean_lunar_calendar import KoreanLunarCalendar

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from db.connection import get_db
from db.repositories.china_character import get_china_character_name
from slack_notion import url
from slack_notion import config
from slack_notion.slack_api import SlackAPI


router = APIRouter(
    prefix="/slack",
    tags=["slack"],
)
slack_client = SlackAPI(config.slack_bot_token)


@router.post("/")
async def select_menu():
    elements_list = [
        {
            "text": "menu1",
            "value": "menu1",
            # "url": "https://www.naver.com"
        },
        {
            "text": "menu2",
            "value": "menu2",
            # "url": "https://www.google.com",
        }
    ]

    slack_client.post_message(
        channel_id=url.channel_id,
        text="select_menu",
        blocks=slack_client.action_buttons(
            elements=elements_list
        )
    )
    return


@router.post("/myname")
async def input_myname():
    slack_client.post_message(
        channel_id=url.channel_id,
        text="myname",
        blocks=slack_client.plain_text_input(
            label_text="당신의 이름을 '한자'로 입력해 주세요.",
            place_holder="ex) 炯旭 (성을 제외한 이름만 입력해주세요.)"
        )
    )
    return


async def input_birthdate(birth_type: str):
    slack_client.post_message(
        channel_id=url.channel_id,
        text=birth_type,
        blocks=slack_client.plain_text_input(
            label_text="당신의 생년월일을 6자리로 입력해 주세요.(음력/양력)",
            place_holder="ex) 220808"
        )
    )
    return


async def select_birthdate_type():
    options = [
        {
            "text": {
                "type": "plain_text",
                "text": "양력",
                "emoji": True
            },
            "value": "solar"
        },
        {
            "text": {
                "type": "plain_text",
                "text": "음력",
                "emoji": True
            },
            "value": "lunar"
        }
    ]

    response = slack_client.post_message(
        channel_id=url.channel_id,
        text="solar_lunar_birthdate",
        blocks=slack_client.radio_buttons(
            title="입력한 생년월일이 양력인지 음력인지 선택해 주세요.",
            options=options
        )
    )
    return response


@router.post("/interactive")
async def post_message(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    payload = json.loads(form_data.get("payload"))
    message = "message"
    actions = payload["actions"][0]
    plain_text = payload["message"]["text"]

    if payload:
        if actions["type"] == "plain_text_input":
            text_input_value = payload["actions"][0]["value"]

            if plain_text == "myname":
                message = await interactive_myname(myname=text_input_value, db=db)
            elif plain_text in ["solar", "lunar"]:
                message = await tojeong_secret_book(birthdate=text_input_value, birth_type=plain_text)

        elif actions["type"] == "radio_buttons":
            await input_birthdate(actions["selected_option"]["value"])
            return

        elif actions["type"] == "button":
            if actions["value"] == "menu1":
                await input_myname()
                return
            elif actions["value"] == "menu2":
                await select_birthdate_type()
                return

    slack_client.post_message(
        channel_id=url.channel_id,
        text=message,
    )

    return


async def interactive_myname(myname: str, db: Session) -> str:
    name_list = [myname[i:i + 1] for i in range(len(myname))]

    result = await get_china_character_name(name_list, db)

    if not result:
        message = "멋진 이름입니다. 당신의 이름에는 불용한자가 없습니다!"
    else:
        name_text = ""
        for name in result:
            name_text = f"{name_text}불용한자는 [{name.cha_name},{name.kor_name}]이며, 이 한자는 {name.description}\n"

        message = f"당신의 이름 중 불용한자는 총 {len(result)}개 입니다...\n{name_text}\n\n부모님이 주신 소중한 이름, 재미로만 봐주세요 🥹"

    return message


async def tojeong_secret_book(birthdate: str, birth_type: str):
    if not birthdate:
        message = "생년월일을 입력해 주시기 바랍니다."
        return message

    if len(birthdate) != 6:
        message = "생년월일 6자리를 맞춰서 입력해 주시기 바랍니다."
        return message

    # 임인년 육십갑자 세팅
    rule1 = 16  # 태세수
    rule2 = 13  # 월건수
    rule3 = 14  # 일진수

    year = birthdate[0:2]
    month = birthdate[2:4]
    day = birthdate[4:6]

    message = f"{year}/{month}/{day}"

    return birth_type