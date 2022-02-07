import os
import uuid
import threading
import base64
import time

from typing import Optional

from fastapi import FastAPI, Header, status, HTTPException
from fastapi.responses import FileResponse

from downloader import download_in_max_res_available, get_video

from persistence import Video
from persistence import get_video_info_from_cache

from log import configure_logging
from log import log
from log import log_debug

app = FastAPI()

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


configure_logging()

log(f"Initialized pyloader with user: {ADMIN_USER} and password: {ADMIN_PASSWORD}")


def unauthorized(message: str = "unauthorized"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


def check_credentials(user: str, password: str):
    return user == ADMIN_USER and password == ADMIN_PASSWORD


def verify_auth(authorization: Optional[str] = Header(None)):
    if authorization is None:
        unauthorized()
    else:
        try:
            credentials = base64.b64decode(authorization.replace("Basic ", "")) \
                .decode("utf-8") \
                .replace("\n", "") \
                .split(":")

            user = credentials[0]
            password = credentials[1]

            if not check_credentials(user, password):
                unauthorized()
        except:
            unauthorized()


@app.get("/download")
async def donwload(url: str, authorization: Optional[str] = Header(None)):
    verify_auth(authorization)

    try:
        video = get_video(url)
    except:
        return {"error_message": "video cannot be retrieved"}

    video_id = str(uuid.uuid4())

    thread = threading.Thread(target=download_in_max_res_available, args=(video_id, video, False))
    thread.start()

    video_info = Video(video_id, video.title, int(time.time()), 1)
    video_info.save_to_redis()

    return {"id": video_id}


@app.get("/download/{video_id}")
async def retrieve_video(video_id: str, authorization: Optional[str] = Header(None)):
    verify_auth(authorization)

    video_info = get_video_info_from_cache(video_id)

    if video_info is None:
        log_debug(f"video-{video_id} not found in cache")
        return {"error_message", "video not found"}

    filepath = f"{video_id}.mp4"
    if os.path.exists(filepath):
        filename = f"{video_info.title}.mp4"
        log_debug(f"requested download for video {video_info.id} as {filename}")
        return FileResponse(path=filepath, filename=filename)
    else:
        return {"error_message": "video does not exist anymore"}
