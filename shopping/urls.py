from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    path("", views.main, name="main"),
    path("search/", views.search_result, name="search_result"),
]