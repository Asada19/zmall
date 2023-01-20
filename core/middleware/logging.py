import json
import time
from asgiref.sync import async_to_sync

from core.db_management.connections.mongo_conn import get_collection_handle


class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "/api/" not in str(request.get_full_path()):
            return response

        key = "{endpoint}-{response_code}-{date}".format(
            endpoint=request.path,
            response_code=response.status_code,
            date=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
        )

        value = response.content

        collection_handle = get_collection_handle('logs')
        async_to_sync(collection_handle.insert_one({key: value}))

        return response
