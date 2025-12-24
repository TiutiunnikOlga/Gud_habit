from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("habit.urls")),
    path("user", include("user.urls")),
    path("shema/", SpectacularAPIView.as_view(), name="shema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="shema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
