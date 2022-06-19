from sqlalchemy.orm import Session

from db.models.china_character import ChinaCharacterInfo
from db.schema.china_character import ChinaCharacter


async def get_china_character_name(
    name: list[str],
    db: Session
):
    query = db.query(ChinaCharacter).filter(ChinaCharacter.CHA_NAME.in_(name)).all()

    result = [
        ChinaCharacterInfo(
            chn_character_no=row.CHN_CHARACTER_NO,
            cha_name=row.CHA_NAME,
            kor_name=row.KOR_NAME,
            description=row.DESCRIPTION,
            call_name=row.CALL_NAME,
        ) for row in query
    ]
    return result
