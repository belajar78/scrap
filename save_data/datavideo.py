import config
import pymongo

my_client = pymongo.MongoClient(config.MONGO_DB_URL)

mydb = my_client[config.MONGO_DB_NAME]

mycol = mydb["files"]

async def getFiles(url):
    found = mycol.find_one({"url": url})
    if found:
        return found
    else:
        return False
    
async def addFile(url, name, size, duration, date, video_id):
    mycol.insert_one({
        "url": url,
        "name": name,
        "size": size,
        "duration": duration,
        "date": date,
        "video": video_id
    })