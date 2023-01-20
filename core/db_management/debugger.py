from django.db import connection, reset_queries
import time
import functools
from advertisement.models import *


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


@query_debugger
def ads_list():
    queryset = AdvertisementPromotion.objects.all()
    ads = []
    for i in queryset:
        ads.append({'id': i.id, 'title': i.promotion.name})
    return ads
