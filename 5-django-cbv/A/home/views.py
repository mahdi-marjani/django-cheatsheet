from .models import Car
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class UserLogin(auth_views.LoginView):
    template_name = 'home/login.html'
    next_page = reverse_lazy('home:home')