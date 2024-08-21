## Index
- [connect app to project (recommended)](#connect-app-to-project-recommended-)
- [project structure with templates (recommended)](#project-structure-with-templates-recommended-)
- [simple class-based view](#simple-class-based-view)
- [PasswordInput widget](#passwordinput-widget)
- [namespaces](#namespaces)
- [form validation](#form-validation)
- [form validation (2 field)](#form-validation-2-field-)
- [dispatch](#dispatch)
- [LoginRequiredMixin](#loginrequiredmixin)
- [customize user model (Log in with username or email)](#customize-user-model-log-in-with-username-or-email-)
- [customize admin](#customize-admin)
- [model methods (get_absolute_url)](#model-methods-get_absolute_url-)
- [setup](#setup-)


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
### dispatch:
override it to add custom logic before processing the request.

e.g. app name is `home`

&lt;project-name&gt;/home/views.py:
```python
from django.shortcuts import render
from django.views import View

class HomeView(View):
    def dispatch(self, request, *args, **kwargs):

        # Custom logic here

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'home/index.html')

    def post(self, request):
        return render(request, 'home/index.html')
```
In this example, `dispatch` is used to run custom code before calling `get` or `post`.
#
### LoginRequiredMixin:

e.g. app name is `accounts`

&lt;project-name&gt;/accounts/views.py:
```python
# If user is logged in, this view works; otherwise, redirect them to login page.
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out successfully', 'success')
        return redirect('home:home')
```
#
### customize user model (Log in with username or email) :
&lt;project-name&gt;/accounts/authenticate.py:
```python
from django.contrib.auth.models import User

class EmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.filter(email=username).first()        # Use email instead of username
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```
&lt;project-name&gt;/&lt;project-name&gt;/settings.py:
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',    # Default model
    'accounts.authenticate.EmailBackend',           # Custom model
]
```
#
### model relationships:
models.py:
```python
from django.db import models
from django.contrib.auth.models import User                     # Another Model

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # ForeignKey to User, links each post to a user
    body = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
#
### customize admin:
admin.py:
```python
from django.contrib import admin
from .models import Post                                                # Post model

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):                                      # Custom admin for Post
    list_display = ('user', 'body', 'slug', 'created_at', 'updated_at') # Show these fields in admin panel
    search_fields = ('body', 'slug')                                    # Search by these fields
    list_filter = ('updated_at',)                                       # Filter by update date
    prepopulated_fields = {'slug': ('body',)}                           # Auto-fill slug from body
    raw_id_fields = ('user',)                                           # Use raw ID for user

```
#
### model methods (get_absolute_url) :
models.py:
```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})  # Returns the post detail URL
```
urls.py:
```python
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # URL pattern for post details
]
```
views.py:
```python
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post

class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)                        # Get post by slug
        return render(request, 'home/post_detail.html', {'post': post})  # Render post detail template
```
use in template:
```html
<a href="{{ post.get_absolute_url }}">Read more</a>  <!-- Use get_absolute_url -->
```
#
### setup :
The `setup` method is used in class-based views to initialize attributes before handling the request.
views.py:
```python
from django.shortcuts import render
from django.views import View

class HomeView(View):
    def setup(self, request, *args, **kwargs):
        self.user = request.user                 # Initialize user attribute
        super().setup(request, *args, **kwargs)  # Call the parent's setup method

    def get(self, request):
        return render(request, 'home/index.html')
```
In this example, the `setup` method initializes the `user` attribute before the request is processed.
#
