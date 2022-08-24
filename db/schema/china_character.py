from sqlalchemy import Column, String, Integer
from db.session import Base


class ChinaCharacter(Base):
    __tablename__ = "TB_CHN_CHARACTER"

    CHN_CHARACTER_NO = Column(Integer, primary_key=True, index=True)
    CHA_NAME = Column(String, nullable=False)
    KOR_NAME = Column(String, nullable=False)
    DESCRIPTION = Column(String, nullable=False)
    CALL_NAME = Column(String, nullable=False)


class SixtyCycle(Base):
    __tablename__ = "TB_SIXTY_CYCLE"

    SIXTY_CYCLE_NO = Column(Integer, primary_key=True, index=True)
    KOR_NAME = Column(String, nullable=False)
    CHN_NAME = Column(String, nullable=False)
    YEAR = Column(Integer, nullable=False)
    MONTH = Column(Integer, nullable=False)
    DAY = Column(Integer, nullable=False)
