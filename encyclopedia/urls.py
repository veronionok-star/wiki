from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new", views.new, name="new"),
    path("wiki/add", views.add, name="add"),
    path("wiki/randomentry", views.random_entry, name="random_entry"),
    path("wiki/save", views.save, name="save"),
    path("wiki/edit/<str:name>", views.edit, name="edit"),
    path("wiki/<str:name>", views.entries, name="entries")
]