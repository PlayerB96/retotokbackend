from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet,
    ChallengeViewSet,
    validate_user,
    get_challenges_by_detail_id,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"challenges", ChallengeViewSet, basename="challenge")

schema_view = get_schema_view(
    openapi.Info(
        title="Retotok API",
        default_version="v1.0.0",
        description="Descripción de tu API",
        terms_of_service="URL de tus términos de servicio",
        contact=openapi.Contact(email="tu@email.com"),
        license=openapi.License(name="Tu Licencia"),
    ),
    public=True,
)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("validate-user/", validate_user, name="validate-user"),
    path(
        "get_challenges_by_detail_id/",
        get_challenges_by_detail_id,
        name="get_challenges_by_detail_id",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
