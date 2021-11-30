from fastapi import FastAPI
import uuid
from downloader import download_in_max_res_available, get_video
from downloader import download

app = FastAPI()


@app.get("/download")
async def root(url:str):
    try:
        video = get_video(url)
    except:
        return {"error_message":"video cannot be retrieved"}
    
    video_id = uuid.uuid4()
    download_in_max_res_available(video, f"{video_id}.mp4")

    return {"id": video_id}