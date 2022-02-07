import redis
import os
import json
from log import log_debug

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
ADMIN_PASSWORD = os.getenv("REDIS_PASSWORD")


def get_connection():
    print(f"connecting to {REDIS_HOST}:{REDIS_PORT} password: {ADMIN_PASSWORD}")
    return redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=ADMIN_PASSWORD)


def get_video_info_from_cache(video_id: str):
    connection = get_connection()
    video_info = connection.get(f"video-{video_id}")

    if video_info is None:
        return None
    else:
        video_info_dict = json.loads(video_info)
        return Video(**video_info_dict)


class Video:
    def __init__(self, id, title, created_on: int, status: int):
        self.id = id
        self.title = title
        self.created_on = created_on
        self.status = status

    def serialize(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def save_to_redis(self):
        connection = get_connection()
        key = f"video-{self.id}"
        value = self.serialize()
        connection.set(key, value)
        log_debug(f"saved {key} as {value}")
