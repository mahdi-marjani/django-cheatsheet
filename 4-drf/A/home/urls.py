from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),    # endpoint
    path('questions/', views.QuestionListView.as_view()),                     # GET
    path('question/create/', views.QuestionCreateView.as_view()),             # POST
    path('question/update/<int:pk>/', views.QuestionUpdateView.as_view()),    # PUT
    path('question/delete/<int:pk>/', views.QuestionDeleteView.as_view())     # DELETE
]