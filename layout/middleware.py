from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from layout.views import base


class HTMXMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.htmx and request.method == 'GET' and request.path != '/':
            return base(request)
        return response
