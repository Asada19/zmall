from django.db import connection

def get_ads_sorted_by(parameter, asc=True):
    """ Returns ads sorted by any existing parameter """

    with connection.cursor() as cursor:
        keyword = "ASC" if asc else "DESC"

        cursor.execute("SELECT * FROM advertisement_advertisement ORDER BY " + parameter + " " + keyword)
        fetched = cursor.fetchall()
    return fetched


def get_ads_filtered_by(price=0, max_price=None, city="", has_image=None):
    with connection.cursor() as cursor:
        max_price_query = " AND max_price < {}".format(max_price) if max_price else ""

        city_query = " AND city ILIKE %%{}%%".format(city)

        image_query = " AND id {} IN (SELECT DISTINCT advertisement_id FROM advertisement_advertisementimage)".format(
            "NOT" if not has_image else "") if has_image is not None else ""

        cursor.execute("SELECT * from advertisement_advertisement WHERE price > %s" +
                       max_price_query + city_query + image_query, [price])
        fetched = cursor.fetchall()

    return fetched


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
