from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # endpoint
    path('questions/', views.QuestionView.as_view()),           # for GET and POST
    path('questions/<int:pk>', views.QuestionView.as_view())    # for PUT and DELETE
]