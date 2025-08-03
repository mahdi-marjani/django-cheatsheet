from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('<int:pk>/', views.Home.as_view()),
]