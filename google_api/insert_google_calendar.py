import datetime
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from google_token import GoogleCalendar


def convert_date(game_date: str):
    month = int(game_date[0:2])
    day = int(game_date[3:5])
    return {"month": month, "day": day}

def convert_team_data(team_data: str):
    team_data = team_data.replace("vs", " vs ")
    return "".join(re.compile("[^0-9]").findall(team_data))

def crawling_kia_tigers():
    driver = webdriver.Chrome("./chromedriver")
    driver.get('https://www.koreabaseball.com/Schedule/Schedule.aspx')

    # 정규 시즌 콤보 박스 클릭
    driver.find_element(by=By.XPATH, value="//select[@id='ddlSeries']/option[text()='KBO 정규시즌 일정']").click()

    # 기아 선택
    driver.find_element(by=By.XPATH, value="//ul[@class='tab-schedule']/li[@attr-value = 'HT']").click()

    month_list = ['05']
    schedule_list = []

    for month in month_list:
        # 달력 선택
        driver.find_element(by=By.XPATH, value="//select[@id='ddlMonth']/option[text()='"+str(month)+"']").click()
        # 결과
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'class': 'tbl'})
        trs = table.find_all('tr')

        for idx, tr in enumerate(trs):
            if idx > 0:
                tds = tr.find_all('td')
                # tds[0] 날짜, tds[1] 시간, tds[2] 팀 + 스코어, tds[7] 장소
                date = convert_date(tds[0].text.strip())
                schedule_info = {
                    "date": tds[0].text.strip(),
                    "month": date["month"],
                    "day": date["day"],
                    "begin_time": tds[1].text.strip(),
                    "end_time": f"{(int(tds[1].text.strip()[0:2]) + 3)}:{tds[1].text.strip()[3:5]}",
                    "team": convert_team_data(tds[2].text.strip()),
                    "stadium": tds[7].text.strip(),
                }
                schedule_list.append(schedule_info)

    driver.close()
    return schedule_list

def set_game_schedule(schedule_list: list):
    google_calendar = GoogleCalendar()

    for schedule in schedule_list:
        date = datetime.date(year=2022, month=schedule["month"], day=schedule["day"]).isoformat()
        event = {
            "summary": schedule["team"],  # 일정 제목
            "location": schedule["stadium"],  # 일정 장소
            "description": '야구 경기',  # 일정 설명
            "start": {  # 시작 날짜
                "dateTime": date + f"T{schedule['begin_time']}:00",
                "timeZone": "Asia/Seoul",
            },
            "end": {  # 종료 날짜
                "dateTime": date + f"T{schedule['end_time']}:59",
                "timeZone": "Asia/Seoul",
            },
        }

        google_calendar.set_google_calendar(event)

def delete_game_schedule():
    google_calendar = GoogleCalendar()

    game_list = google_calendar.get_total_google_calendar()
    for game in game_list:
        if game.get("description") and game["description"] == "야구 경기":
            google_calendar.delete_google_calendar(game["id"])


# 게임 스케줄 크롤링
schedule_list = crawling_kia_tigers()
# 일정 등록
# set_game_schedule(schedule_list)
# 일정 삭제
# delete_game_schedule()