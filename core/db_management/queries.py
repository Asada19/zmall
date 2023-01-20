from django.db import connection

from advertisement.models import Advertisement
from core.db_management.connections.mongo_conn import get_collection_handle


def create_chat_room(ad_id, user_id):
    ads = get_collection_handle('ads')
    if not ads.find_one({"ad_id": ad_id}):
        ads.insert_one({
            "ad_id": ad_id,
            "chat_rooms": [
                {
                    "chat_room_id": user_id,
                    "messages": []
                }
            ]
        })
    chatroom = ads.find_one({"ad_id": ad_id, "chat_rooms.chat_room_id": user_id})

    if not chatroom:
        ads.update_one(chatroom,
                       {"$push":
                           {"chat_rooms": {
                               "chat_room_id": user_id,
                               "messages": []
                           }}
                       })

    print(chatroom)


def get_ads_sorted(parameter, asc=True):
    """ Returns ads sorted by any existing parameter """

    with connection.cursor() as cursor:
        keyword = "ASC" if asc else "DESC"

        cursor.execute("SELECT * FROM advertisement_advertisement ORDER BY " + parameter + " " + keyword)
        fetched = cursor.fetchall()
    return fetched


def get_ads_filtered(price=-1, max_price=None, city="", has_image=None):
    with connection.cursor() as cursor:
        max_price_query = " AND max_price < {}".format(max_price) if max_price else ""

        city_query = " AND city ILIKE '%%{}%%'".format(city) if city else ""

        image_query = " AND id {} IN (SELECT DISTINCT advertisement_id FROM advertisement_advertisementimage)".format(
            "NOT" if has_image == "false" else "") if has_image is not None else ""

        cursor.execute("SELECT * from advertisement_advertisement WHERE price > %s" +
                       max_price_query + city_query + image_query, [price if price else -1])
        fetched = cursor.fetchall()

        list_of_ids = []
        for obj in fetched:
            list_of_ids.append(obj[0])
        queryset = Advertisement.objects.filter(pk__in=list_of_ids)
    return queryset


def get_comment_tree(advertisement_id):
    # Supposing we have only one comment per ad
    query = """ 
    WITH RECURSIVE comment_tree AS (
            SELECT * 
            FROM advertisement_advertisementcomment
            WHERE parent_id = id
        UNION ALL
            SELECT ad2.*
            FROM advertisement_advertisementcomment ad2
            JOIN advertisement_advertisementcomment ad 
            ON ad.id = ad2.parent_id
    )
    SELECT * FROM comment_tree;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        fetched = cursor.fetchall()
    return fetched
