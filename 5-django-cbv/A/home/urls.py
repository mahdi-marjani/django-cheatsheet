from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view()),
    # path('<int:pk>/', views.CarDelete.as_view())
    path('<str:car_name>/', views.CarDelete.as_view())
]