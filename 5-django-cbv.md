## Index
- [View](#View)
- [TemplateView](#TemplateView)
- [RedirectView](#RedirectView)
- [ListView](#ListView)
- [DetailView](#DetailView)
- [FormView](#FormView)
- [CreateView](#CreateView)
- [DeleteView](#DeleteView)
- [UpdateView](#UpdateView)
- [LoginView](#LoginView)
- [LogoutView](#LogoutView)
- [MonthArchiveView (show data by date)](#MonthArchiveView-show-data-by-date)
- [ListAPIView & RetrieveAPIView](#listapiview--retrieveapiview)

### View:
views.py:
```python
from django.shortcuts import render
from django.views import View


class Home(View):
    http_method_names = ['post', 'options']                        # only allow POST and OPTIONS methods

    def post(self, request):
        ...
    
    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'                     # add custom header
        response.headers['user'] = request.user                    # add user info to headers
        return response
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        super().http_method_not_allowed(request, *args, **kwargs)
        return render(request, 'method_not_allowed.html')          # show custom template for disallowed methods
```
#
### TemplateView:
models.py:
```python
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
```
views.py:
```python
from django.views.generic import TemplateView
from .models import Car


class Home(TemplateView):
    template_name = 'home/home.html'                    # specify which template to render

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    # get default context
        context['cars'] = Car.objects.all()             # add all Car objects to context
        return context
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home</h2>

    {% for car in cars %}         {# loop through cars passed from context #}
        <p>
            {{ car.name }}        {# display each car's name #}
        </p>
    {% endfor %}

{% endblock %}
```
#
### RedirectView:
views.py:
```python
from django.views.generic import TemplateView, RedirectView
from .models import Car

class Home(TemplateView):
    ...

class Two(RedirectView):
    # url = 'https://google.com'                            # redirect to external site
    # pattern_name = 'home:home'                            # redirect to named route
    # url = '/'                                             # redirect to homepage
    url = '/home/%(id)i/%(name)s'                           # redirect to dynamic URL with kwargs
    query_string = True                                     # keep query parameters (e.g. ?page=2)

    def get_redirect_url(self, *args, **kwargs):            # override for custom behavior before redirecting
        # print('processing your request...')
        # print(kwargs['id'])
        # print(kwargs['name'])
        # kwargs.pop('id')
        # kwargs.pop('name')
        return super().get_redirect_url(*args, **kwargs)    # use default behavior
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),                          # home page
    path('two/<int:id>/<str:name>/', views.Two.as_view(), name='two'),    # redirect view
]
```
#
### ListView:
views.py:
```python
from .models import Car
from django.views.generic.list import ListView

class Home(ListView):
    template_name = 'home/home.html'                    # specify template to render
    # model = Car                                       # optionally define model (auto queryset = Car.objects.all())
    # queryset = Car.objects.filter(year__gte=2023)     # manually define queryset (alternative to get_queryset)
    context_object_name = 'cars'                        # name used in template (default: object_list)
    # ordering = 'year'                                 # sort results by field
    # allow_empty = False                               # raise 404 if no objects found

    def get_queryset(self):                             # custom queryset logic (e.g. filter by year)
        result = Car.objects.filter(year__gte=2023)
        return result
    
    def get_context_data(self, **kwargs):               # add extra data to context
        context = super().get_context_data(**kwargs)
        context['username'] = 'jack'                    # example extra context
        return context
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home {{ username }}</h2>        {# using extra context data #}

    {% for car in cars %}               {# iterating over context_object_name = 'cars' #}
        <p>
            {{ car.name }}
        </p>
    {% endfor %}

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # Home view shows list of filtered Car objects
]
```
#
### DetailView:
views.py:
```python
from .models import Car
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class Home(ListView):
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class CarDetail(DetailView):
    template_name = 'home/detail.html'                 # template to render detail page
    # model = Car                                      # model used to get object
    # context_object_name = 'car'                      # variable name in template (default: 'object')
    # pk_url_kwarg = 'my_pk'                           # pass pk with custom name in url (e.g. <int:my_pk>/)
    # slug_field = 'name'                              # fetch object by slug
    # slug_url_kwarg = 'my_slug'                       # pass slug with custom name in url (e.g. <slug:my_slug>/)
    # queryset = Car.objects.filter(year__gte=2023)    # custom queryset for filter visible objects

    # def get_queryset(self):                          # customize more queryset
    #     if self.request.user.is_authenticated:
    #         return Car.objects.filter(
    #             name=self.kwargs['my_slug']
    #         )
    #     else:
    #         return Car.objects.none()

    def get_object(self, queryset = None):             # override object fetching logic
        return Car.objects.get(
            year = self.kwargs['year'],                # access URL param 'year'
            name = self.kwargs['name'],                # access URL param 'name'
            owner = self.kwargs['owner'],              # access URL param 'owner'
        )
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # root path shows list of cars
    path(                                           # detail view expects year, name, and owner
        '<int:year>/<str:name>/<str:owner>/',
        views.CarDetail.as_view(),
        name='car_detail'
    ),
]
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home {{ username }}</h2>

    {% for car in cars %}
        <a href="{% url 'home:car_detail' car.year car.name car.owner %}">    {# link to CarDetail view using URL params #}
            {{ car.name }}
        </a>
    {% endfor %}

{% endblock %}
```
detail.html:
```html
{% extends 'base.html' %}

{% block content %}

    <p>{{ object.name }}</p>        {# object refers to the Car instance by default #}
    <p>{{ object.owner }}</p>
    <p>{{ object.year }}</p>

{% endblock %}
```
#
### FormView:
forms.py:
```python
from django import forms
from .models import Car

class CarCreateForm(forms.ModelForm):    # form based on Car model
    class Meta:
        model = Car
        fields = '__all__'
```
views.py:
```python
...
from .models import Car
from django.views.generic import FormView
from .forms import CarCreateForm
from django.urls import reverse_lazy
from django.contrib import messages

...

class CreateCarView(FormView):
    template_name = 'home/create.html'            # template to render the form
    form_class = CarCreateForm                    # form class to use
    success_url = reverse_lazy('home:home')       # redirect after successful form submission

    def form_valid(self, form):                   # called when form is valid
        self._create_car(form.cleaned_data)       # manually create a Car instance
        messages.success(
            self.request,
            'created car successfully',
            'success'
        )
        return super().form_valid(form)
    
    def _create_car(self, data):                  # custom method to create Car
        Car.objects.create(
            name=data['name'],
            owner=data['owner'],
            year=data['year'],
        )
```
create.html:
```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post" novalidate>    {# render the form for car creation #}
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Create">
    </form>

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    ...
    path('create/', views.CreateCarView.as_view(), name='car_create'),
]
```
#
### CreateView:
views.py:
```python
...
from .models import Car
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

...

class CreateCarView(CreateView):
    model = Car
    fields = ['name', 'year']                    # fields to include in form (owner set manually)
    template_name = 'home/create.html'           # template to render the form
    success_url = reverse_lazy('home:home')      # redirect after successful creation

    def form_valid(self, form):                  # called when form is valid
        car = form.save(commit=False)            # create Car instance but don't save yet
        user = self.request.user.username
        if user:
            car.owner = user
        else:
            car.owner = 'anonymous'
        car.save()                               # save Car to database
        messages.success(
            self.request,
            'created car successfully',
            'success'
        )
        return super().form_valid(form)
```
create.html:
```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post" novalidate>    {# render the car creation form #}
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Create">
    </form>

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    ...
    path('create/', views.CreateCarView.as_view(), name='car_create'),
]
```
#
### DeleteView:
views.py:
```python
from .models import Car
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

class Home(ListView):                            # list all cars
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

class CarDelete(DeleteView):
    model = Car                                  # model instance to delete
    success_url = reverse_lazy('home:home')      # redirect after successful deletion
    template_name = 'home/delete.html'           # confirmation template to show before deletion
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home {{ username }}</h2>

    {% for car in cars %}
        <p>
            {{ car.name }}
            <a href="{% url 'home:car_delete' car.id %}">    {# link to confirmation page for car deletion #}
                Delete
            </a>
        </p>
    {% endfor %}

{% endblock %}
```
delete.html:
```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post">                            {# submit confirmation to delete the object #}
        {% csrf_token %}
        <p>Are really want to delete "{{ object }}"?</p>
        <input type="submit" value="Delete">
    </form>

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),                                # homepage with car list
    path('delete/<int:pk>/', views.CarDelete.as_view(), name='car_delete'),     # URL for deleting car by pk
]
```
#
### UpdateView:
views.py:
```python
from .models import Car
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy

class Home(ListView):                            # list all cars
    template_name = 'home/home.html'
    model = Car
    context_object_name = 'cars'

...

class CarUpdate(UpdateView):
    model = Car                                  # model instance to update
    fields = ['name', 'year']                    # fields to update
    success_url = reverse_lazy('home:home')      # redirect after successful update
    template_name = 'home/update.html'           # template contain update form
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home {{ username }}</h2>

    {% for car in cars %}
        <p>
            {{ car.name }}
            ...
            <a href="{% url 'home:car_update' car.id %}">    {# link to the car update form #}
                Update
            </a>
        </p>
    {% endfor %}

{% endblock %}
```
update.html:
```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post">                {# submit the form to update the car #}
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update">
    </form>

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),                                # homepage with car list
    ...
    path('update/<int:pk>/', views.CarUpdate.as_view(), name='car_update'),     # URL for updating a specific car
]
```
#
### LoginView:
views.py:
```python
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

class UserLogin(auth_views.LoginView):
    template_name = 'accounts/login.html'                # template contains login form
    next_page = reverse_lazy('home:home')                # redirect after successful login
```
login.html:
```html
{% extends 'base.html' %}

{% block content %}

    <form action="" method="post">                {# submit login credentials #}
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Login">
    </form>

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login')    # URL for user login
]
```
#
### LogoutView:
views.py:
```python
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

class UserLogin(auth_views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('home:home')

class UserLogout(auth_views.LogoutView):
    next_page = reverse_lazy('home:home')                # redirect after successful logout
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),     # URL for user logout
]
```
#
### MonthArchiveView (show data by date):
models.py:
```python
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    created = models.DateField(null=True, blank=True)    # date field

    def __str__(self):
        return self.name
```
views.py:
```python
from .models import Car
from django.views.generic import MonthArchiveView

class MonthCar(MonthArchiveView):
    model = Car                                        # model to fetch data from
    date_field = 'created'                             # filter data by 'created' date
    template_name = 'home/home.html'                   # template to show results
    context_object_name = 'cars'                       # context variable for loop in template
    # month_format = '%m'                              # optional: if you want numeric months (e.g. 01 for Jan)
```
home.html:
```html
{% extends 'base.html' %}

{% block content %}

    <h2>Home</h2>

    {% for car in cars %}            {# loop through cars created in the given month #}
        <p>
            {{ car.name }}
        </p>
    {% endfor %}

{% endblock %}
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    # path(                                # if using numeric month (01, 02, ...)
    #     '<int:year>/<int:month>/',
    #     views.MonthCar.as_view(),
    #     name='home'
    # ),
    path(                                  # URL includes year and month name (e.g. /2024/jun/)
        '<int:year>/<str:month>/',
        views.MonthCar.as_view(),
        name='home'
    ),
    
]
```
#
### ListAPIView & RetrieveAPIView:
models.py:
```python
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
```
serializers.py:
```python
from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
```
views.py:
```python
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView
)
from .models import Car
from .serializers import CarSerializer


class Home(ListAPIView):
    serializer_class = CarSerializer        # serializer to convert Car objects to JSON
    queryset = Car.objects.all()            # fetch all Car records from DB

class SingleCar(RetrieveAPIView):
    serializer_class = CarSerializer        # serializer for single Car object
    queryset = Car.objects.all()            # search in all cars
    lookup_field = 'name'                   # get single Car by its name (instead of default 'pk')
```
urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view()),                     # list all cars
    # path('<int:pk>/', views.SingleCar.as_view()),     # retrieve one car by ID (e.g. /3/)
    path('<str:name>/', views.SingleCar.as_view()),     # retrieve one car by name (e.g. /BMW/)
]
```
#
