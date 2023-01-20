import motor.motor_asyncio
from django.conf import settings
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(
        'mongodb://{}:{}@{}:{}'.format(settings.MONGO_INITDB_USERNAME, settings.MONGO_INITDB_PASSWORD, settings.MONGO_HOST, settings.MONGO_PORT))
db = client[settings.MONGO_INITDB_DATABASE]
ads = db['ads']
ads.create_index('ad', unique=True)


async def write_chatroom_to_db(ad_id, data):
    await ads[ad_id].insert_one(data)


# async def write_message_to_db(data):
#     await chat_rooms.insert_one(data)


async def create_chat_room(ad_id, user_id):
    if not ads.find({f"{ad_id}": {}}):
        ads.insert_one({f"{ad_id}": {}})
    ad = ads.find_one({f"{ad_id}": {}})
    ads.update_one({"_id": ObjectId(ad["_id"])}, {"$push": {f"{ad_id}": {user_id: {}}}})
