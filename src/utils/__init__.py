from datetime import datetime, timezone
from os import path

timestamp_with_tz = datetime.now(timezone.utc)

def in_container():
    return path.exists("/.dockerenv")