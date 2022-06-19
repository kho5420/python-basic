from db import config


class Settings:
    DB_USERNAME: str = config.DB_USERNAME
    DB_PASSWORD = config.DB_PASSWORD
    DB_HOST: str = "localhost"
    DB_PORT: str = 3306
    DB_DATABASE: str = config.DB_DATABASE

    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"


settings = Settings()