from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_karyawans, name="list_karyawans"),
    path("add/", views.add_karyawan, name="add_karyawan"),
    path("edit/<int:karyawan_id>/", views.edit_karyawan, name="edit_karyawan"),
    path("delete/<int:karyawan_id>/", views.delete_karyawan, name="delete_karyawan"),
]
