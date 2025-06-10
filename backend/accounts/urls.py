from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserProfileView.as_view(), name='me'),
    path('', include(router.urls)),

]