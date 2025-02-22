from django.http import HttpResponseForbidden

class BlockOldAdminURLsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return HttpResponseForbidden("Access Denied")
        return self.get_response(request)
