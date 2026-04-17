from datetime import UTC, datetime
from os import path

timestamp_with_tz = datetime.now(UTC)


def in_container():
    return path.exists("/.dockerenv")
