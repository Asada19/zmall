from django.utils import timezone
import motor.motor_asyncio
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://{}:{}@{}:{}/'.format(settings.MONGO_INITDB_USERNAME, settings.MONGO_INITDB_PASSWORD, settings.MONGO_HOST,
                                    settings.MONGO_PORT))
db = client[settings.MONGO_INITDB_DATABASE]
ads = db['ads']


async def create_chat_room(ad_id, user_id):
    if not await ads.find_one({"ad_id": ad_id}):
        await ads.insert_one({
            "ad_id": ad_id,
            "chat_rooms": [
                {
                    "chat_room_id": user_id,
                    "messages": []
                }
            ]
        })
    chatroom = await ads.find_one({"ad_id": ad_id, "chat_rooms.chat_room_id": user_id})

    if not chatroom:
        await ads.update_one(chatroom,
                             {"$push":
                                 {"chat_rooms": {
                                     "chat_room_id": user_id,
                                     "messages": []
                                 }}
                             })


async def write_message_to_db(ad_id, user_id, message):
    chatroom = await ads.find_one({"ad_id": ad_id})

    if not chatroom:
        raise ObjectDoesNotExist('Database Error: Could not find chatroom')

    await ads.update_one({"ad_id": ad_id, "chat_rooms.chat_room_id": user_id},
                         {'$push':
                              {'chat_rooms.$.messages':
                                   {'message': message,
                                    "user": user_id,
                                    "sent_at": timezone.now()
                                    }
                               }
                          })
