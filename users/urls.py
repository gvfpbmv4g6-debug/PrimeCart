from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("register/confirm/", views.register_confirm_view, name="registerUserConfirm"),
    path("userInfo/", views.user_info_view, name="userInfo"),
    path("logout/", views.logout_view, name="logout"),
]