from django.urls import path
from . import views

urlpatterns = [
	path('register', views.UserRegisterViewSet.as_view(), name='register'),
	path('login', views.UserLoginViewSet.as_view(), name='login'),
	path('logout', views.UserLogoutViewSet.as_view(), name='logout'),
	path('user', views.UserViewSet.as_view(), name='user'),
]
