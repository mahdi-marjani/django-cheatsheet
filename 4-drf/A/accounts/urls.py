from django.urls import path
from . import views
from rest_framework.authtoken import views as authtoken_views
from rest_framework import routers

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegister.as_view()),
    path('api-token-auth/', authtoken_views.obtain_auth_token),
]

router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet)
urlpatterns += router.urls