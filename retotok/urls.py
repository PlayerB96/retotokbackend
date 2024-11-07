from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("authentication.urls")),
]
