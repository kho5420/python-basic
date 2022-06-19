from pydantic import BaseModel, Field


class ChinaCharacterInfo(BaseModel):
    chn_character_no: int = Field(...)
    cha_name: str = Field(...)
    kor_name: str = Field(...)
    description: str = Field(...)
    call_name: str = Field(...)