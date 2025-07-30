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
- [custom permissions](#custom-permissions)
- [serializer relations](#serializer-relations)
- [viewset](#viewset)
- [throttling](#throttling)
- [jwt](#jwt)



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
```python
{
    "username": "pavel",
    "email": "pavel@email.com"
    # "password" is hidden because it's write_only in the serializer
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
```python
[
    {
        "id": 1,
        "title": "first question",
        "slug": "first-question",
        "body": "this is first question",
        "created": "2025-07-29T11:37:03.756944Z",
        "user": 15                                    # related user `id`
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
&lt;project-name&gt;/home/urls.py:
```python
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    ...
    path('questions/', views.QuestionListView.as_view()),                     # GET
    path('question/create/', views.QuestionCreateView.as_view()),             # POST
    path('question/update/<int:pk>/', views.QuestionUpdateView.as_view()),    # PUT
    path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view())     # DELETE
]
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
### custom permissions:
&lt;project-name&gt;/permissions.py:
```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'permission denied, you are not the owner'

    def has_permission(self, request, view):                            # check before any object is accessed
        return request.user.is_authenticated and request.user           # user must be authenticated

    def has_object_permission(self, request, view, obj):                # check for each object separately
        if request.method in SAFE_METHODS:                              # read-only access to everyone (GET, HEAD, OPTIONS)
            return True
        return obj.user == request.user                                 # only owner can edit/delete
```
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly

...

class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated,]                 # only authenticated users can create

    ...

class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]               # only owner can update

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)

        self.check_object_permissions(request, question)    # check object-level permission

        ...

class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly,]               # only owner can delete

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        
        self.check_object_permissions(request, question)    # check object-level permission

        ...
```
#
### serializer relations:
&lt;project-name&gt;/home/serializers.py:
```python
...
from rest_framework import serializers

...

class QuestionSerializer(serializers.ModelSerializer):
    ...

    user = serializers.PrimaryKeyRelatedField(read_only=True)    # user ID (default)

    ...

...
```

**GET** `http://127.0.0.1:8000/questions/`


response:
```python
[
    {
        ...
        "user": 1        # id
    },
    {
        ...
        "user": 15
    }
]
```
&lt;project-name&gt;/home/serializers.py:
```python
...
from rest_framework import serializers

...

class QuestionSerializer(serializers.ModelSerializer):
    ...

    user = serializers.StringRelatedField(read_only=True)    # __str__ value of user

    ...

...
```

**GET** `http://127.0.0.1:8000/questions/`


response:
```python
[
    {
        ...
        "user": "root"        # username
    },
    {
        ...
        "user": "mahdi"
    }
]
```
&lt;project-name&gt;/home/serializers.py:
```python
...
from rest_framework import serializers

...

class QuestionSerializer(serializers.ModelSerializer):
    ...

    user = serializers.SlugRelatedField(read_only=True, slug_field='email')    # user's email (using slug_field)

    ...

...
```

**GET** `http://127.0.0.1:8000/questions/`


response:
```python
[
    {
        ...
        "user": "root@email.com"        # email
    },
    {
        ...
        "user": "mahdi@email.com"
    }
]
```
&lt;project-name&gt;/home/custom_relational_fields.py:
```python
from rest_framework import serializers

class UserEmailNameRelationalField(serializers.RelatedField):
    def to_representation(self, value):                            # custom output for related user (rarely used)
        return f'{value.username} - {value.email}'
```
&lt;project-name&gt;/home/serializers.py:
```python
...
from rest_framework import serializers
from .custom_relational_fields import UserEmailNameRelationalField

...

class QuestionSerializer(serializers.ModelSerializer):
    ...

    user = UserEmailNameRelationalField(read_only=True)                # custom user display (rarely used)

    ...

...
```

**GET** `http://127.0.0.1:8000/questions/`


response:
```python
[
    {
        ...
        "user": "root - root@email.com"        # username - email
    },
    {
        ...
        "user": "mahdi - mahdi@email.com"
    }
]
```
#
### viewset:
&lt;project-name&gt;/accounts/serializers.py:
```python
from rest_framework import serializers
from django.contrib.auth.models import User

...

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```
&lt;project-name&gt;/accounts/views.py:
```python
...
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

...

class UserViewSet(viewsets.ViewSet):                            # custom viewset for managing User model
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()                               # base queryset for all methods

    def list(self, request):                                    # GET /accounts/user/
        srz_data = UserSerializer(
            instance=self.queryset,
            many=True
        )
        return Response(srz_data.data)

    def retrieve(self, request, pk=None):                       # GET /accounts/user/<id>/
        user = get_object_or_404(self.queryset, pk=pk)
        srz_data = UserSerializer(instance=user)
        return Response(srz_data.data)

    def partial_update(self, request, pk=None):                 # PATCH /accounts/user/<id>/
        user = get_object_or_404(self.queryset, pk=pk)

        if user != request.user:                                # only the owner can update
            return Response(
                {'permission denied': 'you are not the owner'}
            )

        srz_data = UserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data)
        return Response(srz_data.errors)
        

    def destroy(self, request, pk=None):                        # DELETE /accounts/user/<id>/
        user = get_object_or_404(self.queryset, pk=pk)

        if user != request.user:                                # only the owner can deactivate
            return Response(
                {'permission denied': 'you are not the owner'}
            )

        user.is_active = False                                  # soft delete: deactivate user
        user.save()
        return Response({'message': 'user deactivated'})
```
&lt;project-name&gt;/accounts/urls.py:
```python
...
from . import views
from rest_framework import routers

app_name = 'accounts'
urlpatterns = [
    ...
]

router = routers.SimpleRouter()                    # connect user endpoints to the viewset
router.register(r'user', views.UserViewSet)        # /accounts/user/
urlpatterns += router.urls
```

**GET** `http://127.0.0.1:8000/accounts/user/`


headers:
```json
{
  "Authorization": "Token ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
response:
```python
[
    {
        "id": 1,
        "password": "...",
        "username": "root",
        ...
    },
    {
        "id": 15,
        "password": "...",
        "username": "mahdi",
        ...
    }
]
```

**GET** `http://127.0.0.1:8000/accounts/user/1/`


headers:
```json
{
  "Authorization": "Token ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
response:
```python
{
    "id": 1,
    "password": "...",
    "username": "root",
    ...
}
```

**PATCH** `http://127.0.0.1:8000/accounts/user/15/`


headers:
```json
{
  "Authorization": "Token ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
body:
```python
{
    "username": "mahdi-dev"
}
```
response:
```python
{
    "id": 15,
    "password": "...",
    "username": "mahdi-dev",
    ...
}
```

**DELETE** `http://127.0.0.1:8000/accounts/user/15/`


headers:
```json
{
  "Authorization": "Token ff7bfb5b86bd1306dc37fabd745bfc015b63f5db"
}
```
response:
```python
{
    "message": "user deactivated"
}
```
#
### throttling:
**Global throttling**:

settings.py:
```python
...

REST_FRAMEWORK = {
    ...
    'DEFAULT_THROTTLE_CLASSES': [                        # apply throttling to all views by default
        'rest_framework.throttling.AnonRateThrottle',    # limit anonymous users
        'rest_framework.throttling.UserRateThrottle',    # limit authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/hour',                                # anonymous: max 3 requests per hour
        'user': '10/hour',                               # authenticated: max 10 requests per hour
    }
}
```

**Per-view throttling**:

settings.py:
```python
...

REST_FRAMEWORK = {
    ...
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/hour',            # anonymous: max 3 requests per hour
        'user': '10/hour',           # authenticated: max 10 requests per hour
    }
}
```
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

...

class QuestionListView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]                # apply per-view throttling

    ...

...
```

**Scoped throttling**:

settings.py:
```python
...

REST_FRAMEWORK = {
    ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle'    # enable throttling scopes
    ],
    'DEFAULT_THROTTLE_RATES': {
        'questions': '5/minute',                          # limit for views with scope="questions"
    }
}
```
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.views import APIView

...

class QuestionListView(APIView):
    throttle_scope = 'questions'                # link this view to "questions" scope

    ...

...
```
#
### jwt:
packages:
```bash
pip install djangorestframework-simplejwt
```
settings.py:
```python
...
from datetime import timedelta

...

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',    # use JWT for authentication
    ],
    ...
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),                      # default
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),                        # default
    ...
}

```
&lt;project-name&gt;/accounts/urls.py:
```python
...
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,                        # returns access + refresh tokens
    TokenRefreshView,                           # returns new access token using refresh
)

app_name = 'accounts'
urlpatterns = [
    ...
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # login endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # refresh endpoint
]

...
```
&lt;project-name&gt;/home/views.py:
```python
...
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class Home(APIView):
    permission_classes = [IsAuthenticated,]                # only allow access with valid JWT token

    ...

...
```

**POST** `http://127.0.0.1:8000/accounts/token/`


body:
```json
{
    "username": "root",
    "password": "root"
}
```
response:
```python
{
    "refresh": "....",      # long-lived token (use to get new access token)
    "access": "...."        # short-lived token (use for authenticated requests)
}
```

**GET** `http://127.0.0.1:8000/`


headers:
```python
{
    "Authorization": "Bearer <access_token>"    # send access token in Authorization header
}
```
response:
```python
{
    "data": [
        ...
    ]
}
```

**POST** `http://127.0.0.1:8000/accounts/token/refresh/`


body:
```python
{
    "refresh": "..."    # valid refresh token
}
```
response:
```python
{
    "access": "..."    # new access token
}
```
#
