import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "6818931531").split()))

API_ID = int(os.getenv("API_ID", "your ip id"))

API_HASH = os.getenv("API_HASH", "your api hash")

BOT_TOKEN = os.getenv("BOT_TOKEN", "Your bot token")

OWNER_ID = int(os.getenv("OWNER_ID", "6818931531"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", " -1002356932965").split()))

RMBG_API = os.getenv("RMBG_API", "f3CYy31QTGdSyYABY8D7FTqQ")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Linxxxx:Linxx2005@cluster0.ea9bybg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-your logs "))
