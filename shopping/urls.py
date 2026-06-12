from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    path("", views.main, name="main"),
    path("search/", views.search_result, name="search_result"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),
]