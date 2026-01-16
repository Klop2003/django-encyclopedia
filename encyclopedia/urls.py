from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("set-theme/<str:theme>/", views.set_theme, name="set_theme"),
    path("settings/", views.save_settings, name="save_settings"),

]
