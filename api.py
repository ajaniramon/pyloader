import binascii
import os
import uuid

from typing import Optional
from fastapi import FastAPI, Header, status, HTTPException
from fastapi.responses import FileResponse
from pprint import pprint
from downloader import download_in_max_res_available, get_video
import threading
import base64

app = FastAPI()

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

print(f"Initialized pyloader with user: {ADMIN_USER} and password: {ADMIN_PASSWORD}")

def unauthorized(message: str = "unauthorized"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


def check_credentials(user: str, password: str):
    return user == ADMIN_USER and password == ADMIN_PASSWORD


def verify_auth(authorization: Optional[str] = Header(None)):
    if authorization is None:
        unauthorized()
    else:
        try:
            credentials = base64.b64decode(authorization).decode("utf-8").replace("\n", "").split(":")

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

    video_id = uuid.uuid4()

    thread = threading.Thread(target=download_in_max_res_available, args=(video, f"{video_id}.mpg", True))
    thread.start()

    return {"id": video_id}


@app.get("/download/{video_id}")
async def retrieve_video(video_id: str, authorization: Optional[str] = Header(None)):
    verify_auth(authorization)

    filepath = f"{video_id}.mp4"
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return {"error_message": "video not found"}
