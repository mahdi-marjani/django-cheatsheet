from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view()),
    path('create/', views.CarCreate.as_view()),
    path('delete/<str:car_name>/', views.CarDelete.as_view()),
    path('update/<int:pk>/', views.CarUpdate.as_view()),
]