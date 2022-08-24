from datetime import datetime


def validate_date_format(date: str):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None
