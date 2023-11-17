from django.db import DatabaseError, OperationalError
from django.http import HttpResponseServerError
import time

class DatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, (DatabaseError, OperationalError)):
            retries = 3
            delay = 0.5
            
            while retries > 0:
                try:
                    response = self.get_response(request)
                    return response
                except (DatabaseError, OperationalError):
                    print("Database connection error. Retrying...")
                    retries -= 1
                    if retries == 0:
                        return HttpResponseServerError("Database connection error after multiple retries.")
                    time.sleep(delay)
