# karyawan/urls.py (file ini belum ada, jadi buat baru)
from django.urls import path
from . import views

urlpatterns = [
    path("", views.daftar_karyawan, name="daftar_karyawan"),
    path("tambah/", views.tambah_karyawan, name="tambah_karyawan"),
    path("edit/<int:pk>/", views.edit_karyawan, name="edit_karyawan"),
    path("hapus/<int:pk>/", views.hapus_karyawan, name="hapus_karyawan"),
]
