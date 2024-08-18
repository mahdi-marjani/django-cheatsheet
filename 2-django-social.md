## Index
- [connect app to project (recommended)](#connect-app-to-project-recommended-)
- [project structure with templates (recommended)](#project-structure-with-templates-recommended-)
- [simple class-based view](#simple-class-based-view)
- [PasswordInput widget](#passwordinput-widget)
- [namespaces](#namespaces)
- [form validation](#form-validation)
- [form validation (2 field)](#form-validation-2-field-)


### connect app to project (recommended) :

e.g. app name is `home`

&lt;project-name&gt;/home/apps.py:
```python
from django.apps import AppConfig

class HomeConfig(AppConfig):                                    # target
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
```

so :

&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
INSTALLED_APPS = [
    ...
    'home.apps.HomeConfig',                  # Add target here
    ...
]
```
#
### project structure with templates (recommended) :
e.g. app name is `home`
```text
<project-name>/
      ├── <project-name>/
      │     ├── __init__.py
      │     ├── asgi.py
      │     ├── settings.py
      │     ├── urls.py
      │     └── wsgi.py
      ├── home/                                # app name
      │     ├── migrations/
      │     │     └── __init__.py
      │     ├── templates/                     # templates related to this app
      │     │     └── home/                    # app name
      │     │          └── index.html          # home page
      │     ├── __init__.py
      │     ├── admin.py
      │     ├── apps.py
      │     ├── models.py
      │     ├── tests.py
      │     └── views.py
      ├── templates/                           # main templates
      │     ├── inc/                           # include templates
      │     │     └── navbar.html
      │     └── base.html
      └── manage.py
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
TEMPLATES = [
    {
        ...
        'DIRS': [
            BASE_DIR / 'templates'            # main templates
        ],
        'APP_DIRS': True,                     # app templates
        ...
    },
]
```
#
### simple class-based view:

e.g. app name is `home`

&lt;project-name&gt;/home/views.py:
```python
from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):                             # If the request method is GET, this method runs.
        return render(request, 'home/index.html')
    def post(self, request):                            # If the request method is POST, this method runs.
        return render(request, 'home/index.html')
```
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
```
#
### PasswordInput widget:
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
```
#
### namespaces:

e.g. app name is `home`

&lt;project-name&gt;/&lt;project-name&gt;/urls.py:
```python
path('', include('home.urls', namespace='home')),
```
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path
from . import views

app_name = "home"                                        # namespace
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
```
use in template:
```html
<a href="{% url 'home:home' %}">Home</a>    # namespace:name
```
#
### form validation:
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):                                    # Email validation (Check for duplicate email)
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Email already exists')
        return email
```
#
### form validation (2 field) :
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django import forms
from django.core.exceptions import ValidationError

class UserRegisterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # overriding clean
    def clean(self):                                            # Password validation (Check Password1 and Password2 match)
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
```
#
