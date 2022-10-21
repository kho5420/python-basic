from sqlalchemy.orm import Session

from db.models.china_character import ChinaCharacterInfo, SixtyCycleInfo, DivinationInfo
from db.schema.china_character import ChinaCharacter, SixtyCycle, Divination, DivinationType


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


async def get_sixty_cycle(
    name: list[str],
    db: Session
):
    query = db.query(SixtyCycle).filter(SixtyCycle.KOR_NAME.in_(name)).all()

    result = [
        SixtyCycleInfo(
            kor_name=row.KOR_NAME,
            chn_name=row.CHN_NAME,
            year=row.YEAR,
            month=row.MONTH,
            day=row.DAY,
        ) for row in query
    ]
    return result


async def get_divination(
    divination_num: int,
    db: Session
):
    query = db.query(Divination, DivinationType).filter(Divination.NUMBER == divination_num).join(DivinationType, Divination.TYPE == DivinationType.ID).first()
    result = DivinationInfo(
        number=query.Divination.NUMBER,
        name=query.Divination.NAME,
        type=query.DivinationType.NAME,
        url=query.Divination.URL,
    )

    return result