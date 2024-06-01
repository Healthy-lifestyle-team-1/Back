"""
URL configuration for HealthyLifeStyle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
# from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from health_app import views

# router = routers.DefaultRouter()
# router.register(r'category', views.CategoryViewSet)
# router.register(r'dishhalf', views.DishHalfViewSet)
# router.register(r'combination', views.CombinationViewSet)
# router.register(r'allergy', views.AllergyViewSet)
# router.register(r'article', views.ArticleViewSet)

from django.urls import re_path

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Подключеие моделей
    path('category/', views.CategoryViewSet.as_view()),
    path('dishhalf/', views.DishHalfViewSet.as_view()),
    path('combination/', views.CombinationViewSet.as_view()),
    path('allergy/', views.AllergyViewSet.as_view()),
    path('article/', views.ArticleViewSet.as_view()),
    path('product/', views.ProductViewSet.as_view()),

    # Документация
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Включение ckeditor5
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('', include('user_app.urls')),
    # path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
