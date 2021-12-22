from fastapi import FastAPI
import uuid
from downloader import download_in_max_res_available, get_video
from downloader import download
import os
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/download")
async def donwload(url:str):
    try:
        video = get_video(url)
    except:
        return {"error_message":"video cannot be retrieved"}
    
    video_id = uuid.uuid4()
    download_in_max_res_available(video, f"{video_id}.mp4", True)

    return {"id": video_id}

@app.get("/download/{video_id}")
async def retrieve_video(video_id:str):
    filepath = f"{video_id}.mp4"
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        return {"error_message":"video not found"}
