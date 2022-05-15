import datetime

from google_token import GoogleCalendar

now = datetime.datetime.now()
now2 = now + datetime.timedelta(hours=1)

today = datetime.date.today().isoformat()

event = {
        'summary': '일정 제목', # 일정 제목
        'location': '서울특별시', # 일정 장소
        'description': '일정 설명', # 일정 설명
        'start': { # 시작 날짜
            'dateTime': today + 'T00:00:00',
            'timeZone': 'Asia/Seoul',
        },
        'end': { # 종료 날짜
            'dateTime': today + 'T23:59:59',
            'timeZone': 'Asia/Seoul',
        },
        # 'recurrence': [ # 반복 지정
        #     'RRULE:FREQ=DAILY;COUNT=1' # 일단위; 총 2번 반복
        # ],
        # 'attendees': [ # 참석자
        #     {'email': 'kho5420@gmail.com'},
        # ],
        # 'reminders': { # 알림 설정
        #     'useDefault': False,
        #     'overrides': [
        #         # {'method': 'email', 'minutes': 24 * 60}, # 24 * 60분 = 하루 전 알림
        #         # {'method': 'popup', 'minutes': 10}, # 10분 전 알림
        #     ],
        # },
    }

test = GoogleCalendar()
test.set_google_calendar(event)
print(test.get_today_google_calendar())
