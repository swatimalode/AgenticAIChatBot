from datetime import datetime
from zoneinfo import ZoneInfo

def current_date():
    now = datetime.now(ZoneInfo("UTC"))
    return now.strftime("%Y-%m-%d")