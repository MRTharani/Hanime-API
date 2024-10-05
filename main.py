import os
from yt_dlp import YoutubeDL
from scaper import *

def download_video(url, output_file):
    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    links = []
    commands = [
        ["htv", "new-uploads", "-u", "-a"],
        ["htv", "ALL", "-u", "-a"],
        ["htv", "new-releases", "-u", "-a"]
    ]

    # Fetch video links using the existing function (assumed to be defined)
    for command in commands:
        links.extend(fetch_video_links(command))

    for title, url in links:
        output_file = f'{title}.mp4'
        download_video(url, output_file)

if __name__ == '__main__':
    main()
