from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new", views.new, name="new"),
    path("wiki/<str:name>", views.entries, name="entries")
]