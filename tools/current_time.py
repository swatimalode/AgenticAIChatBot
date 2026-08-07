from datetime import datetime
from zoneinfo import ZoneInfo


def current_time(timezone):
    now = datetime.now(ZoneInfo(timezone))
    return now.strftime("%Y-%m-%d %H:%M:%S")