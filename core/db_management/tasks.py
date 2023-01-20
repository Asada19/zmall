from advertisement.models import Advertisement
from config.celery import app
from core.db_management.connections.redis_conn import redis_db


@app.task
def unload_data():
    ads = Advertisement.objects.select_related('sub_category').filter(is_active=True)
    ads_ids = [i.id for i in ads]
    views = [view for view in [redis_db.smembers(i) for i in ads_ids]]
    views = [len(i) for i in views if i is not None]
    ads_views = dict(zip(ads_ids, views))
    for i in ads:
        i.views += ads_views.get(i.id, 0)
    Advertisement.objects.bulk_update(ads, ['views'])
    redis_db.flushdb()
