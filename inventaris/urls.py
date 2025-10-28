from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_inventaris, name="list_inventaris"),
    path("add/", views.add_inventaris, name="add_inventaris"),
    path("edit/<int:inventaris_id>/", views.edit_inventaris, name="edit_inventaris"),
    path(
        "delete/<int:inventaris_id>/", views.delete_inventaris, name="delete_inventaris"
    ),
    path("import/", views.import_inventaris, name="import_inventaris"),
]
