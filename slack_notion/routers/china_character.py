import sys, os
import json

from fastapi import Request, Depends, APIRouter
from sqlalchemy.orm import Session
from korean_lunar_calendar import KoreanLunarCalendar


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from db.connection import get_db
from db.repositories.china_character import get_china_character_name, get_sixty_cycle, get_divination
from slack_notion import url
from slack_notion import config
from slack_notion.util import validate_date_format
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
            label_text="당신의 생년월일을 입력해 주세요.(음력/양력)",
            place_holder="ex) 2022-08-01"
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
            title="입력할 생년월일이 양력인지 음력인지 선택해 주세요.",
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
                message = await tojeong_secret_book(birthdate=text_input_value, birth_type=plain_text, db=db)

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


async def tojeong_secret_book(birthdate: str, birth_type: str, db: Session):
    if not birthdate:
        return "생년월일을 입력해 주시기 바랍니다."

    date = validate_date_format(birthdate)

    if not date:
        return "생녈월일을 올바르게 입력해 주세요."

    calendar = KoreanLunarCalendar()

    if birth_type == "solar":
        calendar.setSolarDate(date.year, date.month, date.day)
        date = validate_date_format(calendar.LunarIsoFormat())

    calendar.setLunarDate(2022, date.month, date.day, False)
    gapja_text = calendar.getGapJaString()

    # 우선은 2022년 고정 기준으로 작성
    gapja_year = "임인"
    gapja_month = gapja_text[4:6]
    gapja_day = gapja_text[8:10]

    gapja_list = [gapja_year, gapja_month, gapja_day]
    result = await get_sixty_cycle(gapja_list, db)

    # 음력의 대월,소월 체크
    check_lunar = KoreanLunarCalendar()
    is_month = check_lunar.setLunarDate(2022, date.month, 30, False)

    # 임인년(2022년) 육십갑자 세팅
    rule1 = 0
    rule2 = 0
    rule3 = 0

    for row in result:
        if row.kor_name == gapja_year:
            rule1 = row.year
        elif row.kor_name == gapja_month:
            rule2 = row.month
        elif row.kor_name == gapja_day:
            rule3 = row.day

    # 상괘 = (올해의 나이 + 태세수) % 8
    # 중괘 = (당해의 음력월 달수의 소월/대월 소월이면 29, 대월이면 30 + 월건수) % 6
    # 하괘 = (음력 생일 + 일진수) % 3

    divination1 = ((2022 - date.year + 1) + rule1) % 8
    divination2 = ((30 if is_month else 29) + rule2) % 6
    divination3 = (date.day + rule3) % 3

    if divination1 == 0:
        divination1 = 8

    if divination2 == 0:
        divination2 = 6

    if divination3 == 0:
        divination3 = 3

    result = await get_divination(int(f"{divination1}{divination2}{divination3}"), db)

    return f"*<{result.url}|{result.number} {result.name}>*\n{result.type}"
