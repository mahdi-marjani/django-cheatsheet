## Index
- [initialize django rest framework](#initialize-django-rest-framework)
- [create api](#create-api)
- [request object](#request-object)
- [serializers](#serializers)



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
        ser_data = PersonSerializer(instance=persons, many=True)
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
