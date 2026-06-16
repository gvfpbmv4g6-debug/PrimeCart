from django.urls import path
from . import views

app_name = "shopping"

urlpatterns = [
    path("", views.main, name="main"),
    path("search/", views.search_result, name="search_result"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/update/<int:cart_id>/", views.cart_update, name="cart_update"),
    path("cart/delete/<int:cart_id>/", views.cart_delete, name="cart_delete"),
    path("purchase/", views.purchase_view, name="purchase"),
    path("purchase/commit/", views.purchase_commit_view, name="purchaseCommit"),
]