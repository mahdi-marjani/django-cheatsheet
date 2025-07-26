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
- [run celery](#run-celery)
- [initialize bucket](#initialize-bucket)
- [bucket content](#bucket-content)
- [delete bucket object](#delete-bucket-object)
- [download bucket object](#download-bucket-object)
- [upload bucket object](#upload-bucket-object)
- [async send_otp_code](#async-send_otp_code)
- [write custom mixin](#write-custom-mixin)
- [custom management command](#custom-management-command)
- [use celery beat](#use-celery-beat)
- [run celery in background](#run-celery-in-background)
- [context processors](#context-processors)
- [validators](#validators)
- [permissions](#permissions)
- [postgresql](#postgresql)



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
packages:
```bash
pip install celery
```
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
### run celery:
```bash
celery -A A worker -l INFO --pool=solo
```
* `-A A`: Replace `A` with your project name (the folder where `settings.py` is located)
* `-l INFO`: Log level (INFO for standard output)
* `--pool=solo`: Switch to set the pool type to `solo` (required on Windows)
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
### delete bucket object:
&lt;project-name&gt;/bucket.py:
```python
...
class Bucket:
    ...
    def delete_object(self, key):
        self.s3_resource.meta.client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key
        )
        return True
...
```
&lt;project-name&gt;/home/tasks.py:
```python
...
from celery import shared_task

...
@shared_task
def delete_object_task(key):
    bucket.delete_object(key)
```
&lt;project-name&gt;/home/templates/home/bucket.html:
```html
<td><a href="{% url 'home:delete_obj_bucket' obj.key %}">delete</a></td>
```
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'), # delete object bucket path
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
```
&lt;project-name&gt;/home/views.py:
```python
...
from . import tasks
from django.contrib import messages

...
class DeleteBucketObject(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, f"your object {key} will be deleted soon.", 'info')
        return redirect('home:bucket')
```
models.py:
```python
image = models.ImageField()    # without upload_to
```
&lt;project-name&gt;/&lt;project-name&gt;/celery_conf.py:
```python
celery_app.conf.update(
    broker_url='amqp://',    # without additional address (for local celery)
    ...
)
```
#
### download bucket object:
&lt;project-name&gt;/home/urls.py:
```python
bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj_bucket/<str:key>', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'),
    path('download_obj_bucket/<str:key>', views.DownloadBucketObject.as_view(), name='download_obj_bucket'), # download url
]
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
...
AWS_LOCAL_STORAGE = f'{BASE_DIR}/aws/'
```
&lt;project-name&gt;/bucket.py:
```python
...
class Bucket:
    ...
    def download_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
            self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).download_fileobj(key, f)
...
```
&lt;project-name&gt;/home/tasks.py:
```python
...
@shared_task
def download_object_task(key):
    bucket.download_object(key)
```
&lt;project-name&gt;/home/views.py:
```python
...
class DownloadBucketObject(View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, f"your object {key} will be downloaded soon.", 'info')
        return redirect('home:bucket')
```
&lt;project-name&gt;/home/templates/home/bucket.html:
```html
<td><a href="{% url 'home:download_obj_bucket' obj.key %}">download</a></td>
```
#
### upload bucket object:
&lt;project-name&gt;/bucket.py:
```python
...
class Bucket:
    ...
    def upload_object(self, file, obj_name):
        self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            ACL='private',
            Body=file,
            Key=obj_name
        )
...
```
&lt;project-name&gt;/home/tasks.py:
```python
...
@shared_task
def upload_object_task(filepath, obj_name):
    with open(filepath, "rb") as f:
        bucket.upload_object(f, obj_name)
    os.remove(filepath)
```
&lt;project-name&gt;/home/forms.py:
```python
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
```
&lt;project-name&gt;/home/templates/home/bucket.html:
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Upload">
</form>
```
&lt;project-name&gt;/home/views.py:
```python
...
from .forms import UploadFileForm
from django.conf import settings # A.settings.py
import os

...
class BucketHome(View):
    template_name = 'home/bucket.html'
    
    def get(self, request):
        form = UploadFileForm()
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects, 'form': form})
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            filename = file.name
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

            with open(path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            tasks.upload_object_task.delay(path, filename)
            messages.success(request, f"Uploading {filename} ...", 'info')
            return redirect('home:bucket')
...
```
#
### async send_otp_code:
&lt;project-name&gt;/accounts/tasks.py:
```python
from celery import shared_task
from utils import send_otp_code

@shared_task
def send_otp_code_task(phone, random_code):
    send_otp_code(phone, random_code)
```
&lt;project-name&gt;/accounts/views.py:
```python
# send_otp_code(phone, random_code)
tasks.send_otp_code_task.delay(phone, random_code)                            # New: async version
...
# send_otp_code(user_session['phone_number'], random_code)
tasks.send_otp_code_task.delay(user_session['phone_number'], random_code)     # New: async version
```
#
### write custom mixin:
&lt;project-name&gt;/utils.py:
```python
from django.contrib.auth.mixins import UserPassesTestMixin

...

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
```
&lt;project-name&gt;/home/views.py:
```python
...
from utils import IsAdminUserMixin

...
class BucketHome(IsAdminUserMixin, View):
...
class DeleteBucketObject(IsAdminUserMixin, View):
...
class DownloadBucketObject(IsAdminUserMixin, View):
```
#
### custom management command:
tree:
```text
accounts/                                 # app
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── remove_expired_otps.py        # custom management command
```
&lt;project-name&gt;/accounts/management/commands/remove_expired_otps.py:
```python
from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "remove all expired otp codes"

    def handle(self, *args, **options):
        expired_time = timezone.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write(
            self.style.SUCCESS('all expired otp codes removed.')
        )
```
run custom management command:
```bash
python manage.py remove_expired_otps
```
#
### use celery beat:
packages:
```bash
pip install django-celery-beat
```
settings.py:
```python
INSTALLED_APPS = (
    ...
    'django_celery_beat',
)
```
migrate:
```bash
python manage.py migrate
```
&lt;project-name&gt;/accounts/tasks.py:
```python
...
from celery import shared_task
from accounts.models import OtpCode
from django.utils import timezone
from datetime import timedelta

...
@shared_task
def remove_expired_otps():
    expired_time = timezone.now() - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()
```
Go to the `admin panel`, add a new periodic task, and set the schedule (like every minute) for `accounts.tasks.remove_expired_otps`

run celery beat:
```bash
celery -A A beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
* `-A A`: Replace `A` with your project name (the folder where `settings.py` is located)
#
### run celery in background:
1. install supervisor:
```bash
sudo apt-get install supervisor
```
2. all supervisor processes goes here:
`/etc/supervisor/conf.d`
3. create project's celery configuration file for supervisor:
```bash
touch /etc/supervisor/conf.d/project_name.conf
```
4. write supervisor configuration:
```ini
[program:project_name]
user=user
directory=/var/www/myproject/src/
command=/var/www/myproject/bin/celery -A myproject worker -l info
numprocs=1
autostart=true
autorestart=true
stdout_logfile=/var/log/myproject/celery.log
stderr_logfile=/var/log/myproject/celery.err.log
```
5. create log files:
```bash
touch /var/log/myproject/celery.log
```
```bash
touch /var/log/myproject/celery.err.log
```
6. update supervisor configuration:
```bash
supervisorctl reread
```
```bash
supervisorctl update
```
7. done:
```bash
supervisorctl {status|start|stop|restart} project_name
```
#
### context processors:
&lt;project-name&gt;/orders/cart.py:
```python
...

class Cart:
    ...
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())    # Returns the total quantity of all items in the cart

    ...
```
&lt;project-name&gt;/orders/context_processors.py:
```python
from .cart import Cart

def cart_func(request):                # Makes the Cart object globally available to all templates
    return {'cart': Cart(request)}
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'orders.context_processors.cart_func'    # Add 'cart' to context of all templates via cart_func
            ],
        },
    },
]
```
&lt;project-name&gt;/templates/inc/navbar.html:
```html
<nav class="navbar navbar-expand-lg text-bg-info">
    <div class="container-fluid">
        <div class="navbar-nav">
            ...

            <!-- ✅ Show cart link with item count using the globally available 'cart' object -->
            <a class="nav-link active" href="{% url 'orders:cart' %}">Cart {{ cart|length }}</a>


        </div>
    </div>
</nav>
```
#
### validators:
&lt;project-name&gt;/orders/models.py:
```python
...
from django.core.validators import MinValueValidator, MaxValueValidator    # import built-in validators to limit value range
from django.db import models

...
class Coupon(models.Model):
    ...

    # ✅ ensure discount is between 0% and 90%
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])

    ...
```
#
### permissions:
&lt;project-name&gt;/accounts/models.py:
```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):    # Inherit from PermissionsMixin to enable groups & permissions
    ...

    # def has_perm(self, perm, obj=None):          # has_perm / has_module_perms handled by PermissionsMixin
    #     return True
    # def has_module_perms(self, app_label):
    #     return True

    @property
    def is_staff(self):                            # Allow admin panel access if the user is admin
        return self.is_admin
```
&lt;project-name&gt;/accounts/admin.py:
```python
class UserAdmin(BaseUserAdmin):
    ...

    fieldsets = (
        ...

        
        (
            'Permissions',
            {'fields':
                (... 'is_superuser', 'groups', 'user_permissions', ...)}    # Show is_superuser and group and permissions
        ),

)

    ...

    filter_horizontal = ('groups', 'user_permissions')    # Enable horizontal filter UI for permissions and groups

# admin.site.unregister(Group)                            ← remove this line if you had it before
...
```
check user permissions in templates:
```html
{% if perms.app_name.can_do_something %}                  <!-- check user permission -->
    <form here>
{% endif %}
```
`can_do_something` is a **permission codename**.

Django auto-creates: `add_model`, `change_model`, `delete_model`, `view_model`.

**Example**:
For `Product` model in `home` app:
```text
home.add_product        # lowercase model name
home.change_product
home.delete_product
home.view_product
```
check user permissions in views:
```python
class MyView(View):
    def get(self, request):
        if request.user.has_perm('app_name.can_do_something'):      # check user permission
            ...
        else:
            return HttpResponseForbidden()
```
or:
```python
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

class MyView(PermissionRequiredMixin, View):                        # check user permission using mixin
    permission_required = 'app_name.can_do_something'               # required permission codename

    def get(self, request):
        ...
```
readonly_fields in admin panel:
```python
...

class UserAdmin(BaseUserAdmin):
    ...
    readonly_fields = ('last_login',)    # show-only (not editable in admin)
    ...
```
disable is_superuser field for non-superusers:
```python
...

class UserAdmin(BaseUserAdmin):
    ...

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser and 'is_superuser' in form.base_fields:    # check superuser status
            form.base_fields['is_superuser'].disabled = True           # make read-only for non-superusers
        return form
```
#
### postgresql:
packages:
```bash
# for development
pip install psycopg2-binary

# for production (recommended)
pip install psycopg2
```
settings.py:
```python
...
from pathlib import Path
import os
import platform

BASE_DIR = Path(__file__).resolve().parent.parent

...

HOME_DIR = Path.home()

if platform.system() == "Windows":
    os.environ["PGSERVICEFILE"] = str(HOME_DIR / ".pg_service.conf")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "OPTIONS": {
            "service": "my_service",
            "passfile": HOME_DIR / ".my_pgpass",
        },
    }
}

...
```
in linux/macOS:
```python
export PGSERVICEFILE=$HOME/.pg_service.conf
source ~/.bashrc
```
- in windows:
`C:\Users\<username>\.pg_service.conf`
- in linux/macOS:
` ~/.pg_service.conf`

.pg_service.conf:
```ini
[my_service]
host=127.0.0.1
user=postgres
dbname=shopdata
port=5432
```

- in windows:
`C:\Users\<username>\.my_pgpass`
- in linux/macOS:
` ~/.my_pgpass`

.my_pgpass:
```text
127.0.0.1:5432:shopdata:postgres:root
```
then:
```bash
python manage.py migrate
```
#
