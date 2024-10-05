import os
from yt_dlp import YoutubeDL
from scaper import *
from tools import generate_thumbnail
from upload import switch_upload,upload_thumb
from database import *
import logging
from config import *
from pyrogram import Client


# Setup logging
logging.basicConfig(level=logging.INFO)

db = connect_to_mongodb(MONGODB_URI, "Spidydb")
collection_name = COLLECTION_NAME

if db is not None:
    logging.info("Connected to MongoDB")


app = Client("SpidyHanime", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workers=10)




def download_video(url, output_file):
    ydl_opts = {
        'outtmpl': output_file,
        'format': 'best',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

async def main():
  async with app:
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
            msg = await switch_upload(output_file,output_thumb)
            media_link = msg.media_link
            document = {"Name":title,"Raw_Url":url,"Video":media_link}
            await app.send_video(DUMP_ID,output_file,caption=f"Name: {title}\nLink: {media_link}",thumb=output_thumb)
            insert_document(db, collection_name, document)
            if os.path.exists(output_file):
                os.remove(output_file)
            if os.path.exists(output_thumb):
                os.remove(output_thumb)
        else:
            logging.info(f"{title} is Already Downloaded")


if __name__ == "__main__":
    logging.info("Bot Started...")
    app.run(main())