from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.environ.get('API_ID', ''))
API_HASH = os.environ.get('API_HASH', '')
DUMP_ID = int(os.environ.get('DUMP_ID', ''))
MONGODB_URI = os.getenv("MONGODB_URI")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
COMMUNITY_ID = os.getenv("COMMUNITY_ID")
GROUP_ID = os.getenv("GROUP_ID")
TOKEN = os.getenv("TOKEN")