import config
import pymongo

my_client = pymongo.MongoClient(config.MONGO_DB_URL)

myDb = my_client[config.MONGO_DB_NAME]
mycol = myDb["user"]

async def getUser(chat_id):
    found = mycol.find_one({"_id": chat_id})
    if (found):
        return found
    else:
        return False
    
async def addUser(chat_id):
    mycol.insert_one({"_id": chat_id})

async def delUser(chat_id):
    mycol.delete_one({"_id": chat_id})

async def getAlluser():
    data = []
    for x in mycol.find():
        data.append(x['_id'])
    return data

