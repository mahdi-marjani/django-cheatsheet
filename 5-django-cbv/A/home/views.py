from .models import Car
from django.views.generic.list import ListView

class Home(ListView):
    template_name = 'home/home.html'
    # model = Car
    # queryset = Car.objects.filter(year__gte=2023)
    context_object_name = 'cars' # default : object_list
    # ordering = 'year'
    # allow_empty = False

    def get_queryset(self):
        result = Car.objects.filter(year__gte=2023)
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = 'jack'
        return context