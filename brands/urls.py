from django.urls import path
from . import views

app_name = "brands"

urlpatterns = [
    path("", views.index, name="index"),
    path("save/", views.save_brand, name="save_brand"),
    path("upload/", views.upload_file, name="upload_file"),
    path("api/search/", views.search_db, name="search_db"),
    path("db/<int:pk>/edit/", views.edit_brand, name="edit_brand"),
    path("db/<int:pk>/delete/", views.delete_brand, name="delete_brand"),

]
