from .models import Car
from django.views.generic import ListView, MonthArchiveView

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class MonthCar(MonthArchiveView):
    model = Car
    date_field = 'created'
    template_name = 'home/home.html'
    context_object_name = 'cars'
    # month_format = '%m'