## Index
- [initialize django rest framework](#initialize-django-rest-framework)
- [create api](#create-api)
- [request object](#request-object)
- [serializers](#serializers)
- [register](#register)
- [custom serializer validator](#custom-serializer-validator)
- [ModelSerializer (like ModelForm)](#ModelSerializer-like-ModelForm)
- [model serializer create method](#model-serializer-create-method)
- [status codes](#status-codes)
- [authentication](#authentication)



### initialize django rest framework:
packages:
```bash
pip install djangorestframework
```
settings.py:
```python
INSTALLED_APPS = [
    ...
    
    # Local apps
    ...

    # Third-party apps
    'rest_framework',        # add rest_framework to INSTALLED_APPS
]
```
#
### create api:
&lt;project-name&gt;/home/views.py:
```python
from rest_framework.response import Response
from rest_framework.views import APIView


class Home(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})
```
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home')        # endpoint
]
```
**GET** `http://127.0.0.1:8000/`

json response:
```json
{
    "message": "Hello, world!"
}
```
#
### request object:
request.query_params:
```python
class Home(APIView):
    def get(self, request):
        message = request.query_params['msg']    # get query parameter "msg"
        return Response({"message": message})
```
**GET** `http://127.0.0.1:8000/?msg=hi`

response:
```json
{
    "message": "hi"
}
```
request.data:
```python
class Home(APIView):
    ...

    def post(self, request):
        message = request.data['msg']            # get "msg" from JSON body
        return Response({"message": message})
```
**POST** `http://127.0.0.1:8000/`

request json body:
```json
{
    "msg":"hello"
}
```
response:
```json
{
    "message": "hello"
}
```

<br/>

Also available: `request.user`, `request.method`, `request.session`, etc.

#
### serializers:
&lt;project-name&gt;/home/models.py:
```python
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField()
```
&lt;project-name&gt;/home/serializers.py:
```python
from rest_framework import serializers

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    email = serializers.EmailField()
```
&lt;project-name&gt;/home/views.py:
```python
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer


class Home(APIView):
    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True)    # use 'instance' to convert model/queryset to JSON
        return Response({"data": ser_data.data})
```
**GET** `http://127.0.0.1:8000/`

response:
```json
{
    "data": [
        {
            "name": "amir",
            "age": 12,
            "email": "amir@email.com"
        },
        {
            "name": "kevin",
            "age": 4,
            "email": "kevin@email.com"
        }
    ]
}
```
#
### register:
&lt;project-name&gt;/accounts/serializers.py:
```python
from rest_framework import serializers

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
```
&lt;project-name&gt;/accounts/views.py:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer

class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)        # use 'data' to convert JSON input to model
        if ser_data.is_valid():
            User.objects.create_user(
                username=ser_data.validated_data['username'],
                email=ser_data.validated_data['email'],
                password=ser_data.validated_data['password']
            )
            return Response(ser_data.data)
        return Response(ser_data.errors)
```
&lt;project-name&gt;/accounts/urls.py:
```python
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegister.as_view()),
]
```
**POST** `http://127.0.0.1:8000/accounts/register/`

body:
```json
{
    "username":"pavel",
    "email":"pavel@email.com",
    "password":"pavel"
}
```
response:
```javascript
{
    "username": "pavel",
    "email": "pavel@email.com"
    // "password" is hidden because it's write_only in the serializer
}
```
#
### custom serializer validator:
&lt;project-name&gt;/accounts/serializers.py:
```python
from rest_framework import serializers

def clean_email(value):                                                        # custom function-level validator
    if 'admin' in value:
        raise serializers.ValidationError("admin can't be in email")

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[clean_email])    # use custom validator to this field
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):                                    # field-level validation: runs for username field
        if value == 'admin':
            raise serializers.ValidationError("username can't be `admin`")
        return value
    
    def validate(self, data):                                              # object-level validation: compare multiple fields
        if data['password'] != data['password2']:
            raise serializers.ValidationError("password must match")
        return data
```
#
### ModelSerializer (like ModelForm):
&lt;project-name&gt;/accounts/serializers.py:
```python
from rest_framework import serializers
from django.contrib.auth.models import User

def clean_email(value):
    if 'admin' in value:
        raise serializers.ValidationError("admin can't be in email")

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)        # extra field (not in model)

    class Meta:
        model = User

        # exclude specific fields (can't use both 'fields' and 'excludes')
        # excludes = ('username')

        fields = ('username', 'email', 'password', 'password2')              # specify included fields
        extra_kwargs = {
            'password': {'write_only': True},                                # hide password in output
            'email': {'validators': [clean_email]},                          # use custom field-level validator
        }

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError("username can't be `admin`")
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("password must match")
        return data
```
#
### model serializer create method:
&lt;project-name&gt;/accounts/serializers.py:
```python
from rest_framework import serializers
from django.contrib.auth.models import User

...

class UserRegisterSerializer(serializers.ModelSerializer):
    ...

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        ...
    
    def create(self, validated_data):                                # override to customize model instance creation
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    ...
```
&lt;project-name&gt;/accounts/views.py:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer

class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)                 # use custom create method
            return Response(ser_data.data)
        return Response(ser_data.errors)
```
#
### status codes:
&lt;project-name&gt;/accounts/views.py:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework import status

class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)        # 201: created successfully
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)      # 400: bad input
```
#
### authentication:
settings.py:
```python
...

INSTALLED_APPS = [
    ...
    
    # Local apps
    ...

    # Third-party apps
    ...
    'rest_framework.authtoken',                                    # enable token-based authentication
]

...

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',       # use TokenAuthentication
    ]
}
```
&lt;project-name&gt;/accounts/urls.py:
```python
...
from rest_framework.authtoken import views as authtoken_views

app_name = 'accounts'
urlpatterns = [
    ...
    path('api-token-auth/', authtoken_views.obtain_auth_token),    # return auth token for valid user
]
```
**POST** `http://127.0.0.1:8000/accounts/api-token-auth/`

body:
```json
{
    "username":"root",
    "password":"root"
}
```
response:
```json
{
    "token": "ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
#
