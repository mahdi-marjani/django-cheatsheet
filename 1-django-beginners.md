## Index
- [start project](#start-project)
- [project structure](#project-structure)
- [run project](#run-project)
- [MVT (Model-View-Template)](#mvt-model-view-template)
- [migrations](#migrations)
- [create super user](#create-super-user)
- [create app](#create-app)
- [project structure (with app)](#project-structure-with-app-)
- [connect app to project](#connect-app-to-project)
- [hello world (a simple view)](#hello-world-a-simple-view-)
- [create template](#create-template)
- [project structure (with template)](#project-structure-with-template-)
- [connect templates to project](#connect-templates-to-project)
- [use template](#use-template)
- [pass value to template](#pass-value-to-template)
- [if and else in template](#if-and-else-in-template)
- [template filter - upper](#template-filter---upper)
- [models](#models)
- [project structure (with models)](#project-structure-with-models-)
- [add model to admin panel](#add-model-to-admin-panel)
- [reading from models](#reading-from-models)
- [extend template](#extend-template)
- [template tag - include](#template-tag---include)
- [extract value from url](#extract-value-from-url)
- [url name](#url-name)
- [delete an object from a model](#delete-an-object-from-a-model)
- [show messages to user](#show-messages-to-user)
- [create form](#create-form)
- [project structure (with form)](#project-structure-with-form-)
- [add object to model via form (POST)](#add-object-to-model-via-form-post-)
- [model form](#model-form)
- [update object in model via ModelForm (POST)](#update-object-in-model-via-modelform-post-)
- [users](#users)
- [project structure (with users)](#project-structure-with-users-)
- [register](#register)

#

### start project:
```bash
django-admin startproject <project-name>
```
### project structure:
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py
      │         ├── asgi.py            # ASGI configuration for async servers.
      │         ├── settings.py        # Project settings and configuration.
      │         ├── urls.py            # URL routing for project.
      │         └── wsgi.py            # WSGI configuration for traditional servers.
      └── manage.py                    # Command-line tool for managing project.
```
### run project:
```bash
python manage.py runserver
```
#
### MVT (Model-View-Template):

![django-mvt-based-control-flow](https://github.com/user-attachments/assets/f09e8b74-7fc8-434f-97f6-59d550ae192b)

* **Model** : Defines and manages data structure and database interaction.
* **View** : Handles request processing and business logic.
* **Template** : Renders HTML output with data provided by View.
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
### create super user:
Create a superuser for access to site's admin panel (`http://<yourdomain>/admin/`) :
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
      │         ├── __init__.py
      │         ├── asgi.py                  # ASGI configuration for async servers.
      │         ├── settings.py              # Project settings and configuration.
      │         ├── urls.py                  # URL routing for project.
      │         └── wsgi.py                  # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        └── __init__.py
      │         ├── __init__.py
      │         ├── admin.py                 # Admin panel configurations.
      │         ├── apps.py                  # App configuration.
      │         ├── models.py                # Defines data models (database structure).
      │         ├── tests.py                 # Tests for app.
      │         ├── views.py                 # View functions for handling requests.
      │         └── urls.py (optional)       # Optional: Defines URL routing for app.
      └── manage.py                          # Command-line tool for managing project.
```
### connect app to project:
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
    path('', include('your_app_name.urls')),
]
```
When you send a request to `http://<yourdomain>/hello/`, you will receive **"Hello World"** in response.
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
      │         ├── __init__.py
      │         ├── asgi.py                  # ASGI configuration for async servers.
      │         ├── settings.py              # Project settings and configuration.
      │         ├── urls.py                  # URL routing for project.
      │         └── wsgi.py                  # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        └── __init__.py
      │         ├── __init__.py
      │         ├── admin.py                 # Admin panel configurations.
      │         ├── apps.py                  # App configuration.
      │         ├── models.py                # Defines data models (database structure).
      │         ├── tests.py                 # Tests for app.
      │         ├── views.py                 # View functions for handling requests.
      │         └── urls.py (optional)       # Optional: Defines URL routing for app.
      ├── templates/
      │         └── hello-world.html         # A sample template
      └── manage.py                          # Command-line tool for managing project.
```
### connect templates to project:
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
### use template:
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render

def hello_world(request):
    return render(request, 'hello-world.html')
```
#
### pass value to template:
&lt;project-name&gt;/templates/say-hello.html:
```html
<h3>Hello {{ name }}</h3>
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render

def say_hello(request):
    return render(request, 'say-hello.html', {'name': 'mahdi'})
```
When you send a request to to this view, you will receive **Hello mahdi** in response.
### if and else in template:
&lt;project-name&gt;/templates/say-hello.html:
```html
{% if name == "admin" %}
      <p>you are admin</p>
{% else %}
      <h3>Hello {{ name }}</h3>
{% endif %}
```
If the name is **"admin,"** it says **"you are admin."** If not, it just says **"Hello {{ name }}"**
### template filter - upper:
&lt;project-name&gt;/templates/say-hello.html:
```html
<h3>Hello {{ name|upper }}</h3>
```
name will be displayed in uppercase
#
### models:
&lt;project-name&gt;/&lt;app-name&gt;/models.py:
```python
from django.db import models

class Todo(models.Model):                                    # A sample model
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
```
Run `python manage.py makemigrations` and `python manage.py migrate`
### project structure (with models) :
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py
      │         ├── asgi.py                       # ASGI configuration for async servers.
      │         ├── settings.py                   # Project settings and configuration.
      │         ├── urls.py                       # URL routing for project.
      │         └── wsgi.py                       # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        ├── __init__.py
      │         │        └── 0001_initial.py      # Creates initial database tables.
      │         ├── __init__.py
      │         ├── admin.py                      # Admin panel configurations.
      │         ├── apps.py                       # App configuration.
      │         ├── models.py                     # Defines data models (database structure).
      │         ├── tests.py                      # Tests for app.
      │         ├── views.py                      # View functions for handling requests.
      │         └── urls.py (optional)            # Optional: Defines URL routing for app.
      ├── templates/
      │         └── hello-world.html              # A sample template
      ├── db.sqlite3                              # Django's default database.
      └── manage.py                               # Command-line tool for managing project.
```
#
### add model to admin panel:
&lt;project-name&gt;/&lt;app-name&gt;/admin.py:
```python
from django.contrib import admin
from .models import Todo            # target model

admin.site.register(Todo)
```
### reading from models:
&lt;project-name&gt;/templates/todo_list.html:
```html
<!DOCTYPE html>
<html>
  <head>
    <title>Todo List</title>
  </head>
  <body>
    <h1>Todo List</h1>
    <ul>
      {% for todo in todos %}
        <li>
            {{ todo.title }} - {{ todo.body }} - {{ todo.created_at }}
        </li>
      {% empty %}
        <li>No todos found.</li>
      {% endfor %}
    </ul>
  </body>
</html>
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render
from .models import Todo                  # target model

def show_todos(request):
    todos = Todo.objects.all()
    return render(request, 'todo_list.html', {'todos': todos})
```
#
### extend template:
&lt;project-name&gt;/templates/base.html:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <title>{% block title %}Default Title{% endblock %}</title>
</head>

<body>
    {% block content %}{% endblock %}
</body>

</html>
```
&lt;project-name&gt;/templates/home.html:
```html
{% extends "base.html" %}

{% block title %}
  Home
{% endblock %}

{% block content %}
  <h2>Welcome to the Home Page!</h2>
{% endblock %}
```
When `home.html` renders in browser, final output will be:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <title>Home</title>                     <!-- Title from home.html -->
</head>

<body>
    <h2>Welcome to the Home Page!</h2>      <!-- Content from home.html -->
</body>

</html>
```
#
### template tag - include:
&lt;project-name&gt;/templates/header.html:
```html
<header>
    <h1>My Website</h1>
</header>
```
&lt;project-name&gt;/templates/home.html:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <title>Home</title>
</head>

<body>
    {% include "header.html" %}                  <!-- Header is included from header.html -->

    <h2>Welcome to the Home Page!</h2>
</body>

</html>
```
When `home.html` renders in browser, final output will be:
```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <title>Home</title>
</head>

<body>
    <header>                                 <!-- Content from header.html -->
        <h1>My Website</h1>                  <!-- Content from header.html -->
    </header>                                <!-- Content from header.html -->

    <h2>Welcome to the Home Page!</h2>
</body>

</html>
```
#
### extract value from url:
&lt;project-name&gt;/&lt;app-name&gt;/urls.py:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('number/<int:number_val>/', views.handle_number),
]
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.http import HttpResponse

def handle_number(request, number_val):
    return HttpResponse(f'The number is {number_val}')
```
**Example:**

Request URL: `http://<yourdomain>/number/42/`

Response: `The number is 42`
#
### url name:
**Define URL Name:**
```python
path('long-url-path-that-might-change/', views.some_view, name='some_name'),
```

<br />
<br />

**Use URL Name in Templates:**
```html
<a href="{% url 'some_name' %}">Go to Some Path</a>
```
Result: `{% url 'some_name' %}` generates URL `http://<yourdomain>/long-url-path-that-might-change/`

<br />
<br />

**Use URL Name in Views for Redirects:**
```python
from django.shortcuts import redirect

def some_other_view(request):
    return redirect('some_name')
```
Result: `redirect('some_name')` sends user to URL named `some_name`
#
### delete an object from a model:
Example:

Delete a Todo Object:

&lt;project-name&gt;/&lt;app-name&gt;/views.py:

```python
from django.shortcuts import redirect
from .models import Todo                        # target model

def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)         # target object
    todo.delete()
    return redirect('todo_list')
```
#
### show messages to user:
Add a message in your view:
```python
from django.contrib import messages
from django.shortcuts import redirect
from .models import Todo

def delete_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    messages.success(request, 'Todo deleted successfully!', extra_tags='alert-success')      # messages
    return redirect('todo_list')
```
Show the message in redirected template:
```html
{% if messages %}
  {% for message in messages %}
    <div class="{{ message.extra_tags }}">{{ message }}</div>
  {% endfor %}
{% endif %}
```
#
### create form:
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django import forms

class SimpleForm(forms.Form):                  # A sample form
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render
from .forms import SimpleForm                                         # target form

def show_form(request):
    form = SimpleForm()
    return render(request, 'form_template.html', {'form': form})      # Send form to template
```
template:
```html
<form>
    {% csrf_token %}                              <!-- Stops fake form submissions -->
    {{ form }}                                    <!-- use form in template (Default: form.as_table) -->
    <input type="submit" value="Submit">
</form>
```
### project structure (with form) :
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py
      │         ├── asgi.py                       # ASGI configuration for async servers.
      │         ├── settings.py                   # Project settings and configuration.
      │         ├── urls.py                       # URL routing for project.
      │         └── wsgi.py                       # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        ├── __init__.py
      │         │        └── 0001_initial.py      # Creates initial database tables.
      │         ├── __init__.py
      │         ├── admin.py                      # Admin panel configurations.
      │         ├── apps.py                       # App configuration.
      │         ├── forms.py (optional)           # Optional: Django forms.
      │         ├── models.py                     # Defines data models (database structure).
      │         ├── tests.py                      # Tests for app.
      │         ├── views.py                      # View functions for handling requests.
      │         └── urls.py (optional)            # Optional: Defines URL routing for app.
      ├── templates/
      │         └── hello-world.html              # A sample template
      ├── db.sqlite3                              # Django's default database.
      └── manage.py                               # Command-line tool for managing project.
```
#
### add object to model via form (POST) :
&lt;project-name&gt;/&lt;app-name&gt;/models.py:
```python
from django.db import models

class Todo(models.Model):                                    # A sample model
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
```
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django import forms

class TodoCreateForm(forms.Form):                                    # A simple form suitable for Todo model
    title = forms.CharField(label='title', max_length=100)
    body = forms.CharField(label='body', widget=forms.Textarea)
```
&lt;project-name&gt;/templates/todo_create.html:
```html
<h1>Todo Create</h1>
<form action="" method="post">                  <!-- Use POST method -->
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Create">
</form>
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoCreateForm

def todo_create(request):
    if request.method == 'POST':
        form = TodoCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Todo.objects.create(title=data['title'], body=data['body'])
            messages.success(request, 'Todo created successfully!', extra_tags='alert-success')
            return redirect('todo_list')
    else:
        form = TodoCreateForm()

    return render(request, 'todo_create.html', {'form': form})
```
#
### model form
&lt;project-name&gt;/&lt;app-name&gt;/models.py:
```python
from django.db import models

class Todo(models.Model):                                    # A sample model
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
```
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django.forms import ModelForm
from .models import Todo

class TodoCreateForm(ModelForm):            # A sample model form suitable for Todo model
    class Meta:
        model = Todo
        fields = ['title', 'body']
```
#
### update object in model via ModelForm (POST) :
&lt;project-name&gt;/&lt;app-name&gt;/models.py:
```python
from django.db import models

class Todo(models.Model):                                    # A sample model
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
```
&lt;project-name&gt;/&lt;app-name&gt;/forms.py:
```python
from django import forms
from .models import Todo

class TodoUpdateForm(forms.ModelForm):            # A ModelForm suitable for updating Todo model
    class Meta:
        model = Todo
        fields = ['title', 'body']
```
&lt;project-name&gt;/templates/todo_update.html:
```html
<h1>Update Todo</h1>
<form action="" method="post">                  <!-- Use POST method -->
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Update">
</form>
```
&lt;project-name&gt;/&lt;app-name&gt;/views.py:
```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Todo
from .forms import TodoUpdateForm

def todo_update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)                         # Get the Todo object by id
    if request.method == 'POST':
        form = TodoUpdateForm(request.POST, instance=todo)      # Connect form to the existing Todo object
        if form.is_valid():
            form.save()                                         # Save the updated Todo object
            messages.success(request, 'Todo updated successfully!', extra_tags='alert-success')
            return redirect('todo_list')
    else:
        form = TodoUpdateForm(instance=todo)                    # Fill the form with existing data

    return render(request, 'todo_update.html', {'form': form})
```
#
### users:
create `accounts` app:
```bash
python manage.py startapp accounts
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
INSTALLED_APPS = [
    ...
    'accounts',
    ...
]
```
### project structure (with users) :
```text
<project-name>/
      ├── <project-name>/
      │         ├── __init__.py
      │         ├── asgi.py                       # ASGI configuration for async servers.
      │         ├── settings.py                   # Project settings and configuration.
      │         ├── urls.py                       # URL routing for project.
      │         └── wsgi.py                       # WSGI configuration for traditional servers.
      ├── <app-name>/
      │         ├── migrations/
      │         │        ├── __init__.py
      │         │        └── 0001_initial.py      # Creates initial database tables.
      │         ├── __init__.py
      │         ├── admin.py                      # Admin panel configurations.
      │         ├── apps.py                       # App configuration.
      │         ├── forms.py (optional)           # Optional: Django forms.
      │         ├── models.py                     # Defines data models (database structure).
      │         ├── tests.py                      # Tests for app.
      │         ├── views.py                      # View functions for handling requests.
      │         └── urls.py (optional)            # Optional: Defines URL routing for app.
      ├── accounts/
      │         ├── migrations/
      │         │        └── __init__.py
      │         ├── __init__.py
      │         ├── admin.py
      │         ├── apps.py
      │         ├── forms.py (optional)
      │         ├── models.py
      │         ├── tests.py
      │         ├── views.py
      │         └── urls.py (optional)
      ├── templates/
      │         └── hello-world.html              # A sample template
      ├── db.sqlite3                              # Django's default database.
      └── manage.py                               # Command-line tool for managing project.
```
#
### register
&lt;project-name&gt;/accounts/forms.py:
```python
from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
```
&lt;project-name&gt;/templates/register.html:
```html
<h1>Register</h1>
<form action="" method="post">                  <!-- Use POST method -->
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Register">
</form>
```
&lt;project-name&gt;/accounts/views.py:
```python
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User      # Import Django User model.
from django.contrib import messages

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Create a new user with form data.
            User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])

            messages.success(request, 'User registered successfully!', extra_tags='alert-success')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
```
#
### login
&lt;project-name&gt;/accounts/forms.py:
```python
from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
```
&lt;project-name&gt;/templates/login.html:
```html
<h1>Login</h1>

<form action="" method="post"> <!-- Use POST method -->
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Login">
</form>
```
&lt;project-name&gt;/accounts/views.py:
```python
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                messages.success(request, 'User logged in successfully!', extra_tags='alert-success')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password!', extra_tags='alert-danger')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
```
#
