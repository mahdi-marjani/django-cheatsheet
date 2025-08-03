from .models import Car
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class CarDelete(DeleteView):
    model = Car
    success_url = reverse_lazy('home:home')
    template_name = 'home/delete.html'

class CarUpdate(UpdateView):
    model = Car
    fields = ['name', 'year']
    success_url = reverse_lazy('home:home')
    template_name = 'home/update.html'