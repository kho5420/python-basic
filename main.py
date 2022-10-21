import sys

from fastapi import FastAPI
from slack_notion.routers import china_character, notion

sys.path.append('/Users/hyungukkim/Desktop/Developments/test-folder/python-basic')

app = FastAPI()

app.include_router(notion.router)
app.include_router(china_character.router)
