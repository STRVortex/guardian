from os import getenv
from dotenv import load_dotenv

load_dotenv()

#API_ID = int(getenv("API_ID", ))
#API_HASH = getenv("API_HASH", )
#BOT_TOKEN = getenv("BOT_TOKEN") #Put your bot token here
#LOG_ID = int(getenv("LOG_ID"))
#SUDOERS = list(map(int, getenv("SUDOERS", "").split()))
#MONGO_DB_URI = getenv("MONGO_DB_URI", "")

API_ID = int(getenv("API_ID", "27696582"))  # Replace default value if necessary
API_HASH = getenv("API_HASH", "45fccefb72a57ff1b858339774b6d005")
BOT_TOKEN = getenv("BOT_TOKEN", "8066611257:AAEjhv6N3v-5w_mtdVHyHOGfFMKMwaaYCZo")  # Replace default value if necessary
LOG_ID = int(getenv("LOG_ID", "-1002064111110"))
SUDOERS = list(map(int, getenv("SUDOERS", "6257927828").split(",")))  # Support multiple SUDOERS
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://strvortexcore:vortexcore0019@cluster0.fkb3o.mongodb.net/?retryWrites=true&w=majority")
BOT_OWNER_ID = "6257927828"
