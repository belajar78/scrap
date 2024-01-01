import os

API_ID = int(os.environ.get("API_ID", "23393031"))
API_HASH = os.environ.get("API_HASH", "77a1ccce0177c7e4925a1081a0d6fed2")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6915074471:AAHIW9JaCAepIrn2YUDeUdphXKPj3VyNSrA")

OWNER_ID = int(os.environ.get("OWNER_ID", "6492851132"))

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002110824585"))
CHANNEL_DATABASE = int(os.environ.get("CHANNEL_DATABASE", "-1002108851080"))

MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "mongodb+srv://dood:dood@cluster0.vxcg4ot.mongodb.net/?retryWrites=true&w=majority")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "DDIDBot")