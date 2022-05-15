#!/usr/bin/python36
# -*- coding: utf-8 -*-
import itertools
import sys
import random

from google_token import GoogleCalendar

google_calendar = GoogleCalendar()

def get_vacationer_list():
    response = google_calendar.get_today_google_calendar()

    vacationer_list = []
    if response.get("items"):
        for item in response["items"]:
            vacationer_list.append(item.get("summary"))

    return vacationer_list

def convert_reviewer(vacationer_list):
    status_list = ["연차", "오후반차", "오전반차", "오전반반차", "오후반반차"]

    for i, vacationer in enumerate(vacationer_list):
        for vacation in status_list:
            if vacationer.find(vacation) != -1:
                vacationer_list[i] = vacationer.replace(f" {vacation}", "").split(",")

    reviewer_list = list(itertools.chain(*vacationer_list))
    return [review.strip() for review in reviewer_list]


vacationer_list = get_vacationer_list()
reviewer_list = convert_reviewer(vacationer_list)

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

all_name_list = list(set(all_name_list) - set(reviewer_list))
first_approve_list = list(set(first_approve_list) - set(reviewer_list))
second_approve_list = list(set(all_name_list) - set(first_approve_list))

try:
    first_approve_list.remove(input_name)
except ValueError:
    pass

try:
    second_approve_list.remove(input_name)
except ValueError:
    pass

first_reviewer = None
second_reviewer = None

if first_approve_list:
    first_reviewer = random.choice(first_approve_list)
    second_reviewer = random.choice(second_approve_list)
else:
    first_reviewer = random.choice(second_approve_list)
    second_approve_list.remove(first_reviewer)
    second_reviewer = random.choice(second_approve_list)

print(f"첫번째 승인자 : {first_reviewer}")
print(f"두번째 승인자 : {second_reviewer}")