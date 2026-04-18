from datetime import UTC, datetime
from os import getenv, path

timestamp_with_tz = datetime.now(UTC)

env_state = getenv("ENV_STATE", "dev")
env_file = ".env.test" if env_state == "test" else ".env"


def in_container():
    return path.exists("/.dockerenv")
