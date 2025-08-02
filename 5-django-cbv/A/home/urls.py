from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('<int:year>/<str:name>/<str:owner>/', views.CarDetail.as_view(), name='car_detail'),
]