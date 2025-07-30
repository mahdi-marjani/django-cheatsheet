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
- [permissions](#permissions)
- [read (GET)](#read-GET)
- [create (POST) update (PUT) delete (DELETE)](#create-POST-update-PUT-delete-DELETE)
- [clean question view](#clean-question-view)
- [method fields](#method-fields)



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
### permissions:
&lt;project-name&gt;/home/views.py:
```python
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class Home(APIView):
    permission_classes = [IsAuthenticated,]                            # only authenticated users can access this view

    def get(self, request):
        persons = Person.objects.all()
        ser_data = PersonSerializer(instance=persons, many=True)
        return Response({"data": ser_data.data})

```
**GET** `http://127.0.0.1:8000/`

headers:
```json
{
  "Authorization": "Token ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
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
### read (GET):
&lt;project-name&gt;/home/models.py:
```python
from django.db import models
from django.contrib.auth.models import User

...

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.title[:20]}'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.question.title[:20]}'
```
&lt;project-name&gt;/home/serializers.py:
```python
from rest_framework import serializers
from .models import Question, Answer

...

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
```
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import QuestionSerializer
from rest_framework import status

...

class QuestionView(APIView):
    def get(self, request):                                             # GET: return list of all questions
        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)

    def post(self, request):                                            # POST: create new question
        pass

    def put(self, request, pk):                                         # PUT: update existing question
        pass

    def delete(self, request, pk):                                      # DELETE: remove question
        pass
```
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    ...
    path('questions/', views.QuestionView.as_view()),           # for GET and POST
    path('questions/<int:pk>/', views.QuestionView.as_view())    # for PUT and DELETE
]
```
**GET** `http://127.0.0.1:8000/questions/`


response:
```javascript
[
    {
        "id": 1,
        "title": "first question",
        "slug": "first-question",
        "body": "this is first question",
        "created": "2025-07-29T11:37:03.756944Z",
        "user": 15                                    // related user `id`
    }
]
```
#
### create (POST) update (PUT) delete (DELETE):
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import QuestionSerializer
from rest_framework import status

...

class QuestionView(APIView):
    ...

    def post(self, request):                                                    # POST: create new question
        srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):                                                 # PUT: update existing question
        question = Question.objects.get(pk=pk)
        srz_data = QuestionSerializer(
            instance=question,
            data=request.data,
            partial=True                                                        # only send fields you want to update
        )
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):                                              # DELETE: remove question
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(
            {'message': 'question deleted'},
            status=status.HTTP_200_OK
        )
```
**POST** `http://127.0.0.1:8000/questions/`

body:
```json
{
    "title": "second",
    "slug": "second-question",
    "body": "this is second question",
    "user": 15
}
```
response:
```json
{
    "id": 2,
    "title": "second",
    "slug": "second-question",
    "body": "this is second question",
    "created": "2025-07-29T13:49:42.947137Z",
    "user": 15
}
```

**PUT** `http://127.0.0.1:8000/questions/2/`

body:
```json
{
    "title": "Second Question"
}
```
response:
```json
{
    "id": 2,
    "title": "Second Question",
    "slug": "second-question",
    "body": "this is second question",
    "created": "2025-07-29T14:19:37.749296Z",
    "user": 15
}
```

**DELETE** `http://127.0.0.1:8000/questions/2/`

response:
```json
{
    "message": "question deleted"
}
```
#
### clean question view:
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import QuestionSerializer
from rest_framework import status

...

class QuestionListView(APIView):                                                # GET: return list of all questions
    def get(self, request):
        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)

class QuestionCreateView(APIView):                                              # POST: create new question
    def post(self, request):
        srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionUpdateView(APIView):                                              # PUT: update existing question
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        srz_data = QuestionSerializer(
            instance=question,
            data=request.data,
            partial=True
        )
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDeleteView(APIView):                                              # DELETE: remove question
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(
            {'message': 'question deleted'},
            status=status.HTTP_200_OK
        )
```
#
### method fields:
&lt;project-name&gt;/home/serializers.py:
```python
from rest_framework import serializers
from .models import Question, Answer

...

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()                    # custom field: show related answers

    class Meta:
        model = Question
        fields = '__all__'
    
    def get_answers(self, obj):                                      # return answers related to this question
        result = obj.answers.all()
        return AnswerSerializer(instance=result, many=True).data

...
```
**GET** `http://127.0.0.1:8000/questions/`


response:
```json
[
    {
        "id": 1,
        "answers": [
            {
                "id": 1,
                "body": "this is first answer",
                "created": "2025-07-29T11:37:27.472129Z",
                "user": 1,
                "question": 1
            },
            {
                "id": 2,
                "body": "answer for first",
                "created": "2025-07-29T17:47:54.811042Z",
                "user": 15,
                "question": 1
            }
        ],
        "title": "first question",
        "slug": "first-question",
        "body": "this is first question",
        "created": "2025-07-29T11:37:03.756944Z",
        "user": 15
    },
    {
        "id": 2,
        "answers": [
            {
                "id": 3,
                "body": "answer for second",
                "created": "2025-07-29T17:48:10.828477Z",
                "user": 15,
                "question": 5
            }
        ],
        "title": "second question",
        "slug": "second-question",
        "body": "this is second question",
        "created": "2025-07-29T17:47:06.196358Z",
        "user": 15
    }
]
```
#
