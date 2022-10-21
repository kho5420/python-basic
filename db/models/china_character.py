from pydantic import BaseModel, Field


class ChinaCharacterInfo(BaseModel):
    chn_character_no: int = Field(...)
    cha_name: str = Field(...)
    kor_name: str = Field(...)
    description: str = Field(...)
    call_name: str = Field(...)


class SixtyCycleInfo(BaseModel):
    kor_name: str
    chn_name: str
    year: int
    month: int
    day: int


class DivinationInfo(BaseModel):
    number: int
    name: str
    type: str
    url: str