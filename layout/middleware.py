from django.utils.deprecation import MiddlewareMixin
from activity_guide.settings import IS_READY, DEBUG
from layout.views import not_ready


class HTMXMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.base_template = 'layout/fragment.html' if request.htmx else 'layout/base.html'

    def process_response(self, request, response):
        # if DEBUG:
        #     response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        # else:
        #     response['Cache-Control'] = 'public, max-age=315360000, must-revalidate'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return response


class IsReadyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not IS_READY and request.META['HTTP_HOST'] == 'activityguide.ca':
            return not_ready(request)
        return response
