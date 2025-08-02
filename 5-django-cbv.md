## Index
- [View](#View)
- [TemplateView](#TemplateView)
- [RedirectView](#RedirectView)
- [ListView](#ListView)
- [DetailView](#DetailView)

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
