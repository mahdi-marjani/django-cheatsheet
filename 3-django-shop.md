## Index
- [custom user model (Substituting a custom User model)](#custom-user-model-substituting-a-custom-user-model-)
- [custom user manager](#custom-user-manager)
- [custom user form](#custom-user-form)
- [custom user admin](#custom-user-admin)
- [sessions](#sessions)
- [static files](#static-files)
- [media files](#media-files)
- [cloud storage](#cloud-storage)
- [initialize celery](#initialize-celery)
- [initialize bucket](#initialize-bucket)
- [bucket content](#bucket-content)



### custom user model (Substituting a custom User model) :
&lt;project-name&gt;/accounts/models.py:
```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):                                     # Custom user model
    email = models.EmailField(max_length=255, unique=True)        # Email field, must be unique
    phone_number = models.CharField(max_length=11, unique=True)   # Phone number field, must be unique
    full_name = models.CharField()                                # Full name field (required)
    is_active = models.BooleanField(default=True)                 # Check if the user is active
    is_admin = models.BooleanField(default=False)                 # Check if the user is an admin

    USERNAME_FIELD = 'phone_number'                               # The field used for logging in; this field must be unique
    REQUIRED_FIELDS = ['email', 'full_name']                      # Fields that are required along with the USERNAME_FIELD

    def __str__(self):                                            # String representation of the user object
        return self.email
    
    def has_perm(self, perm, obj=None):                           # Always returns True, allows all permissions
        return True
    
    def has_module_perms(self, app_label):                        # Always returns True, allows all app label permissions
        return True
    
    @property
    def is_staff(self):                                           # If the user is admin, they can access the admin panel
        return self.is_admin
```
#
### custom user manager:
&lt;project-name&gt;/accounts/managers.py:
```python
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):       # Create a regular user
        if not phone_number:
            raise ValueError('Users must have a phone number')             # Phone number is required
        if not email:
            raise ValueError('Users must have an email address')           # Email is required
        if not full_name:
            raise ValueError('Users must have a full name')                # Full name is required
        
        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),                           # Normalize the email
            full_name = full_name
        )

        user.set_password(password)                                        # Hash and set the password
        user.save(using=self._db)                                          # Save the user in the database
        return user

    def create_superuser(self, phone_number, email, full_name, password):  # Create a super user
        user = self.create_user(phone_number = phone_number, email = email, full_name = full_name, password = password)

        user.is_admin = True                                               # Make the user an admin
        user.save(using=self._db)                                          # Save the superuser in the database

        return user
```
&lt;project-name&gt;/accounts/models.py:
```python
...
from .managers import UserManager                                  # Manager 

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()                                        # Connect manager to model
    ...
```
#
### custom user form:
&lt;project-name&gt;/accounts/forms.py:
```python
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)          # Password field
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  # Confirm password

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password']                    # Fields to include in form
    
    def clean_password2(self):                                                         # Check if passwords match
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('Passwords dont match.')
        return cd['password2']
    
    def save(self, commit=True):                                                       # Save user with hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(                                              # Read-only password field
                    help_text='you can change password using <a href="../password/">this form</a>.'
                )  

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'password', 'last_login']      # Fields to include in form
```
#
### custom user admin:
&lt;project-name&gt;/accounts/admin.py:
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm                                   # Form for editing users
    add_form = UserCreationForm                             # Form for creating new users
    list_display = ('email', 'phone_number', 'is_admin')    # Columns in admin list view
    list_filter = ('is_admin',)                             # Filter by admin status

    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'full_name', 'password')}),   # Main user fields
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),       # Permissions section
    )
    
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'full_name', 'password1', 'password2')}),   # Fields for new users
    )
    
    search_fields = ('email', 'full_name')                    # Search by email or full name
    ordering = ('full_name',)                                 # Order by full name in list
    filter_horizontal = ()                                    # No filter horizontal fields
    
admin.site.unregister(Group)                                  # Remove Group model from admin
admin.site.register(User, UserAdmin)                          # Register custom User model in admin
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
AUTH_USER_MODEL = 'accounts.User'   # Use custom User model in the project (app_name.user_model_name)
```
#
### sessions:
create and use session:
```python
>>> request.session[0] = "bar"
>>> request.session[0]  # KeyError
>>> request.session["0"]
'bar'
```
When sessions are saved:
```python
# ✅ Session is modified and saved.
request.session["foo"] = "bar"

# ✅ Session is modified and saved.
del request.session["foo"]

# ✅ Session is modified and saved.
request.session["foo"] = {}

# ❌ Session is NOT modified or saved, because this modifies
# request.session['foo'] instead of request.session
request.session["foo"]["bar"] = "baz"

# ℹ️ To save it, we can set:
request.session.modified = True
```
#
### static files:
**for each app:**

settings file:
```python
STATIC_URL = "static/"
```
tree:
```text
my_app/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
├── static/                    # static files folder
│   └── my_app/
│       └── img/
│           └── example.jpg    # static file
└── templates/
    └── my_app/
        └── template.html      # use static file
```
template.html:
```html
{% load static %}
<img src="{% static 'my_app/example.jpg' %}" alt="My image">
```

**global:**

settings file:
```python
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
```
tree:
```text
my_project
├── db.sqlite3
├── manage.py
├── utils.py
│
├───my_project
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └─── __init__.py
│
├───static                        # global static files folder
│   └───css
│       └─── base_styles.css      # global static file
│
└───templates
    ├── base.html                 # use global static file
    │
    └───inc
        ├── messages.html
        └─── navbar.html
```
base.html:
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Online Shop</title>
    <link rel="stylesheet" href="{% static 'css/base_styles.css' %}">    # use global static file
</head>
```
#
### media files:
settings file:
```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
models.py:
```python
image = models.ImageField(upload_to='products/%Y/%m/%d/')
```
tree:
```text
shop
├── db.sqlite3
├── manage.py
├── utils.py
│
├───shop
│   ├── asgi.py
│   ├── settings.py                        # settings file
│   ├── urls.py
│   ├── wsgi.py
│   └─── __init__.py
│
├───products
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                          # models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └─── __init__.py
│
└───media
    └───products
        └───2025
            └───04
                └───14
                    └─── image.png         # media file
```
#
### cloud storage:
packages:
```bash
pip install django-storages
pip install boto3
```
settings.py:
```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',                        # add storages
]
...
# Arvancloud Storage (like Amazon S3)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = '***'
AWS_SECRET_ACCESS_KEY = '***'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.ir'
AWS_STORAGE_BUCKET_NAME = '***'
AWS_S3_SIGNATURE_VERSION = 's3'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
...
```
#
### initialize celery:
&lt;project-name&gt;/&lt;project-name&gt;/celery_conf.py:
```python
from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

celery_app = Celery('A')
celery_app.autodiscover_tasks()

celery_app.conf.update(
    broker_url='amqp://admin:root@localhost:5672//',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='pickle',
    accept_content=['json', 'pickle'],
    result_expires=timedelta(days=1),
    task_always_eager=False,
    worker_prefetch_multiplier=1,
)
```
&lt;project-name&gt;/&lt;project-name&gt;/\_\_init_\_.py:
```python
from .celery_conf import celery_app
```
#
### initialize bucket:
create a `Bucket` class to connect to AWS S3

&lt;project-name&gt;/bucket.py:
```python
import boto3
from botocore.exceptions import ClientError
from django.conf import settings                # A.settings.py
import logging

class Bucket:
    """
    CDN bucket manager
    
    init method creates connection.

    NOTE:
        none of these methods are async. use public interface in task.py module instead.
    """
    def __init__(self):
        try:
            self.s3_resource = boto3.resource(
                service_name=settings.AWS_S3_SIGNATURE_VERSION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL
            )
        except Exception as exc:
            logging.error(exc)
```
#
### bucket content:
&lt;project-name&gt;/bucket.py:
```python
...
class Bucket:
    ...
    def get_objects(self):
        try:
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            bucket = self.s3_resource.Bucket(bucket_name)
            objects = bucket.objects.all()
            if not objects:
                logging.info(f"No objects found in bucket: {bucket_name}")
                return None
            return objects
        except ClientError as e:
            logging.error(e)


bucket = Bucket()
```

&lt;project-name&gt;/home/tasks.py:
```python
from bucket import bucket


# TODO: Should be made async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result
```
&lt;project-name&gt;/home/templates/home/bucket.html:
```html
{% extends 'base.html' %}

{% block content %}

    <table class="table table-dark">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Size</th>
            <th scope="col">Download</th>
            <th scope="col">Delete</th>
        </tr>
        </thead>
        <tbody>
        {% for obj in objects %}
            <tr>
                <th scope="row">{{ forloop.counter }}</th>
                <td>{{ obj.key }}</td>
                <td>{{ obj.size|filesizeformat }}</td>
                <td>Download</td>
                <td>Delete</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>

{% endblock %}
```
&lt;project-name&gt;/home/urls.py:
```python
path('bucket', views.BucketHome.as_view(), name='bucket'),
```
&lt;project-name&gt;/home/views.py:
```python
from .tasks import all_bucket_objects_task

class BucketHome(View):
    template_name = 'home/bucket.html'
    
    def get(self, request):
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})
```
&lt;project-name&gt;/templates/inc/navbar.html:
```html
{% if user.is_admin %}
    <!-- The management bucket page link for admin in navbar -->
    <a class="nav-link active" href="{% url 'home:bucket' %}">bucket</a>
{% endif %}
```
#
