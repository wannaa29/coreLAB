from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("karyawan/", include("karyawan.urls")),
    path("inventaris/", include("inventaris.urls")),
]
