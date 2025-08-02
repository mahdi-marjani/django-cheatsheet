from .models import Car
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class CreateCarView(CreateView):
    model = Car
    fields = ['name', 'year']
    template_name = 'home/create.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        car = form.save(commit=False)
        user = self.request.user.username
        if user:
            car.owner = user
        else:
            car.owner = 'anonymous'
        car.save()
        messages.success(
            self.request,
            'created car successfully',
            'success'
        )
        return super().form_valid(form)