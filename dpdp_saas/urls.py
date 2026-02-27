from django.contrib import admin
from django.urls import path, include
from assessments.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("assessments/", include("assessments.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]