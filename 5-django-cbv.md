## Index
- [View](#View)
- [TemplateView](#TemplateView)

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
