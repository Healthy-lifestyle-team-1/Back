from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.UserLoginViewSet.as_view(), name='login'),
 	path('verify/', views.VerifyCodeViewSet.as_view(), name='verify'),
	path('logout/', views.UserLogoutViewSet.as_view(), name='logout'),
	path('user/', views.UserViewSet.as_view(), name='user'),
]
