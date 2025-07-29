from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # endpoint
    path('questions/', views.QuestionListView.as_view()),           # GET
    path('questions/', views.QuestionCreateView.as_view()),           # POST
    path('questions/<int:pk>', views.QuestionUpdateView.as_view()),    # PUT
    path('questions/<int:pk>', views.QuestionDeleteView.as_view())    # DELETE
]