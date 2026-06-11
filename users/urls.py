from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("register/confirm/", views.register_confirm_view, name="registerUserConfirm"),
    path("success/", views.success_view, name="success"),
]