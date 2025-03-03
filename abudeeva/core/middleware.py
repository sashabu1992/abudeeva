from django.http import HttpResponsePermanentRedirect
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # Убираем порт, если он есть
        if host.startswith('www.'):
            no_www_host = host[4:]
            url = request.build_absolute_uri().replace(host, no_www_host, 1)
            return HttpResponsePermanentRedirect(url)
        return self.get_response(request)


class LowercaseRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.isupper():
            lower_path = request.path.lower()
            if lower_path != request.path:
                return HttpResponsePermanentRedirect(lower_path)

