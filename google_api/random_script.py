#!/usr/bin/python36
# -*- coding: utf-8 -*-
import sys
import random
import requests

import config


def get_google_calendar_list():
    url = f"https://www.googleapis.com/calendar/v3/calendars/{config.calendar_id}/events?key={config.google_api_key}"

    params = {'param1': 'value1', 'param2': 'value'}
    res = requests.get(URL, params=params)

    출처: https: // dgkim5360.tistory.com / entry / python - requests[개발새발로그]


project_list = ["1", "2", "3"]
all_name_list = ["리뷰어1", "리뷰어2", "리뷰어3", "리뷰어4", "리뷰어5", "리뷰어6", "리뷰어7"]

input_project = input("""
    Pr프로젝트 입력하세요 : 
     - 프로젝트 1 : 1
     - 프로젝트 2 : 2
     - 프로젝트 3 : 3
""")

if input_project not in project_list:
    sys.exit("잘못된 프로젝트 입력 입니다.")

input_name = input(f"""
    이름을 입력하세요 : 
     - 이름 리스트 : "리뷰어1", "리뷰어2", "리뷰어3", "리뷰어4", "리뷰어5", "리뷰어6", "리뷰어7"
""")

if input_name not in all_name_list:
    sys.exit("잘못된 이름 입력 입니다.")


first_approve_list = []
second_approve_list = []

if input_project == "1":
    first_approve_list = ["리뷰어1", "리뷰어2", "리뷰어3"]
elif input_project == "2":
    first_approve_list = ["리뷰어1", "리뷰어4"]
else:
    first_approve_list = ["리뷰어1", "리뷰어3"]

second_approve_list = list(set(all_name_list) - set(first_approve_list))

try:
    first_approve_list.remove(input_name)
except ValueError:
    pass

try:
    second_approve_list.remove(input_name)
except ValueError:
    pass

print("첫번째 승인자 : {}".format(random.choice(first_approve_list)))
print("두번째 승인자 : {}".format(random.choice(second_approve_list)))