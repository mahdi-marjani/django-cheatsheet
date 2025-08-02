from django.views.generic import TemplateView, RedirectView
from .models import Car


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.all()
        return context

class Two(RedirectView):
    # url = 'https://google.com'
    # pattern_name = 'home:home'
    # url = '/'
    url = '/home/%(id)i/%(name)s'
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # print('processing your request...')
        # print(kwargs['id'])
        # print(kwargs['name'])
        # kwargs.pop('id')
        # kwargs.pop('name')
        return super().get_redirect_url(*args, **kwargs)