#!/usr/bin/python3
from pytube import YouTube

from storage import upload_to_storage

from log import log
from log import log_debug

version = "0.0.1"
resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]

STATUS_AVAILABLE = 1
STATUS_REMOVED = 2


def get_video(url: str):
    return YouTube(url)


def download(url: str, filename: str):
    video = get_video(url)
    download_in_max_res_available(video, filename)


def download_in_max_res_available(video_id: str, video: YouTube, upload: bool):
    print(f"searching for best stream for {video.title} as MP4...")

    for res in resolutions:
        streams = video.streams.filter(progressive=True, res=res)
        filename = f"{video_id}.mp4"
        if len(streams) > 0:
            log(f"found stream for resolution {res}, downloading...")
            streams[0].download(filename=filename)

            if upload:
                upload_to_storage(filename)
            else:
                log_debug("skipping upload to storj")

            log_debug(f"download finished for {filename}")
            break
        else:
            log_debug(f"no found streams for {res}")
