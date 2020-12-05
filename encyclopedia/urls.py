from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("error/wrong_entry/<str:title>", views.wrong_entry, name="wrong_entry"),
    path("search", views.search, name="search"),
    path("add", views.addentry, name="add"),
    path("edit/<str:title>", views.editentry, name="edit"),
    path("random", views.random, name="random"),
]
