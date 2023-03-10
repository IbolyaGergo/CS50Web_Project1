from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.show_entry, name="show_entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page")
]
