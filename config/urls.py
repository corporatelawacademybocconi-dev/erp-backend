from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "CLA backend is running",
        "routes": ["/admin/", "/api/", "/api/token/"]
    })


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("projects.urls")),
    path("api/", include("contacts.urls")),
    path("api/", include("goals.urls")),
]