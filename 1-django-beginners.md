### start project:
```bash
django-admin startproject <project-name>
```
### project structure:
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py        # Marks this directory as a Python package.
      │         ├── asgi.py            # ASGI configuration for async servers.
      │         ├── settings.py        # Project settings and configuration.
      │         ├── urls.py            # URL routing for the project.
      │         └── wsgi.py            # WSGI configuration for traditional servers.
      └── manage.py                    # Command-line tool for managing the project.
```
### run project:
```bash
python manage.py runserver
```
#
### MVT (Model-View-Template):

![django-mvt-based-control-flow](https://github.com/user-attachments/assets/f09e8b74-7fc8-434f-97f6-59d550ae192b)

* **Model** : Defines and manages the data structure and database interaction.
* **View** : Handles request processing and business logic.
* **Template** : Renders HTML output with data provided by the View.
#
### migrations:
After creating or changing models:
```bash
python manage.py makemigrations
```
To apply those changes:
```bash
python manage.py migrate
```
**Note:** On first setup, `python manage.py migrate` creates default tables for built-in apps like authentication and admin.
### Create Super User:
Create a superuser for access to the site's admin panel (`http://<yourdomain>/admin/`) :
```bash
python manage.py createsuperuser
```
#
### create app:
```bash
python manage.py startapp <app-name>
```
### project structure (with app) :
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py              # Marks this directory as a Python package.
      │         ├── asgi.py                  # ASGI configuration for async servers.
      │         ├── settings.py              # Project settings and configuration.
      │         ├── urls.py                  # URL routing for the project.
      │         └── wsgi.py                  # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        └── __init__.py     # Marks this directory as a Python package.
      │         ├── __init__.py              # Marks this directory as a Python package.
      │         ├── admin.py                 # Admin panel configurations.
      │         ├── apps.py                  # App configuration.
      │         ├── models.py                # Defines the data models (database structure).
      │         ├── tests.py                 # Tests for the app.
      │         ├── views.py                 # View functions for handling requests.
      │         └── urls.py (optional)       # Optional: Defines URL routing for the app.
      └── manage.py                          # Command-line tool for managing the project.
```
### Connecting the app to the project:
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'your_app_name',                  # Add your app here
]
```
### hello world (a simple view) :
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World")
```
&lt;project-name&gt;/&lt;app-name&gt;/urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world),
]
```
&lt;project-name&gt;/&lt;project-name&gt;/urls.py:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
```
Now, if you send a request to `http://<yourdomain>/hello/`, you will receive **"Hello World"** in the response.
#
### create template:
Create a `templates` folder in the `<project-name>` folder

For example, create an HTML file named `hello-world.html` in the `templates` folder with this content:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hello World</title>
  </head>
  <body>
    <h3>Hello World</h3>
  </body>
</html>
```
### project structure (with template) :
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py              # Marks this directory as a Python package.
      │         ├── asgi.py                  # ASGI configuration for async servers.
      │         ├── settings.py              # Project settings and configuration.
      │         ├── urls.py                  # URL routing for the project.
      │         └── wsgi.py                  # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        └── __init__.py     # Marks this directory as a Python package.
      │         ├── __init__.py              # Marks this directory as a Python package.
      │         ├── admin.py                 # Admin panel configurations.
      │         ├── apps.py                  # App configuration.
      │         ├── models.py                # Defines the data models (database structure).
      │         ├── tests.py                 # Tests for the app.
      │         ├── views.py                 # View functions for handling requests.
      │         └── urls.py (optional)       # Optional: Defines URL routing for the app.
      ├── templates/
      │         └── hello-world.html         # A sample template
      └── manage.py                          # Command-line tool for managing the project.
```
### Connecting the templates to the project:
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'            # Add your templates folder here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
### use a template:
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render

def hello_world(request):
    return render(request, 'hello-world.html')
```
#
