from .models import Car
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class CarDetail(DetailView):
    template_name = 'home/detail.html'
    # model = Car
    # context_object_name = 'car'
    # pk_url_kwarg = 'my_pk'
    # slug_field = 'name'
    # slug_url_kwarg = 'my_slug'
    # queryset = Car.objects.filter(year__gte=2023)

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Car.objects.filter(name=self.kwargs['my_slug'])
    #     else:
    #         Car.objects.none()

    def get_object(self, queryset = None):
        return Car.objects.get(
            year = self.kwargs['year'],
            name = self.kwargs['name'],
            owner = self.kwargs['owner'],
        )