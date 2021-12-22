#!/usr/bin/python3
from pytube import YouTube
import sys
from storage import upload_to_storage
version = "0.0.1"
resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]


def main():
    print(f"pyloader v{version}.")

    if len(sys.argv) < 2:
        print("usage: main.py <URL>")
        exit(1)

    if len(sys.argv) == 3:
        download(sys.argv[1], sys.argv[2])
    else:
        download(sys.argv[1], None)

def get_video(url: str):
    return YouTube(url)


def download(url: str, filename: str):
    video = get_video(url)
    download_in_max_res_available(video, filename)

def download_in_max_res_available(video: YouTube, filename: str, upload: bool):
    print(f"searching for best stream for {video.title} as MP4...")
    
    for res in resolutions:
        streams = video.streams.filter(progressive=True, res=res)
        if len(streams) > 0:
            print(f"found stream for resolution {res}, donwloading...")
            streams[0].download(filename=filename)
            if upload:
                upload_to_storage(filename)
            break
        else:
            print(f"no found streams for {res}")        

if __name__ == "__main__":
    main()