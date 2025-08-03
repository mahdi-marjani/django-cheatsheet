from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view()),
    # path('<int:pk>/', views.SingleCar.as_view())
    path('<str:name>/', views.SingleCar.as_view())
]