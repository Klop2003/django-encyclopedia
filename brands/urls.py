from django.urls import path
from . import views

app_name = "brands"

urlpatterns = [
    path("", views.index, name="index"),
    path("save-json/", views.save_json, name="save_json"),
    path("save-xml/", views.save_xml, name="save_xml"),
    path("upload/", views.upload_file, name="upload_file"),
]
