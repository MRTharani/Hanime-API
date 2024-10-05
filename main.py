import os
import asyncio
from yt_dlp import YoutubeDL
from scaper import *
from tools import generate_thumbnail
from upload import switch_upload,upload_thumb
from database import *
import logging
from config import *


# Setup logging
logging.basicConfig(level=logging.INFO)

db = connect_to_mongodb(MONGODB_URI, "Spidydb")
collection_name = COLLECTION_NAME

if db is not None:
    logging.info("Connected to MongoDB")




def download_video(url, output_file):
    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def main():
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
        downloads = [ download["Name"] for download in find_documents(db, collection_name)] 
        if title not in downloads:
            output_file = f'{title}.mp4'
            output_thumb = f'{title}.png'
            download_video(url, output_file)
            generate_thumbnail(output_file, output_thumb)
            img = await upload_thumb(output_thumb)
            msg = await switch_upload(output_file,output_thumb)
            media_link = msg.media_link
            img_link = img.media_link
            document = {"Name":title,"Raw_Url":url,"Video":media_link,"Image":img_link}
            insert_document(db, collection_name, document)
            if os.path.exists(output_file):
                os.remove(output_file)
            if os.path.exists(output_thumb):
                os.remove(output_thumb)
        else:
            logging.info(f"{title} is Already Downloaded")

if __name__ == '__main__':
    asyncio.run(main())
