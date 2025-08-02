from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create/', views.CreateCarView.as_view(), name='car_create'),
]