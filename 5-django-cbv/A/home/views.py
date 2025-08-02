from django.shortcuts import render
from django.views import View


class Home(View):
    http_method_names = ['post', 'options']

    def post(self, request):
        ...
    
    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        response.headers['user'] = request.user
        return response
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        super().http_method_not_allowed(request, *args, **kwargs)
        return render(request, 'method_not_allowed.html')