from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("register/confirm/", views.register_confirm_view, name="registerUserConfirm"),
    path("register/commit/", views.register_commit_view, name="registerUserCommit"),
    path("userInfo/", views.user_info_view, name="userInfo"),
    path("updateUser/", views.update_user_view, name="updateUser"),
    path("updateUser/confirm/", views.update_user_confirm_view, name="updateUserConfirm"),
    path("updateUser/commit/", views.update_user_commit_view, name="updateUserCommit"),
    path("logout/", views.logout_view, name="logout"),
    path("withdraw/confirm/", views.withdraw_confirm_view, name="withdrawConfirm"),
    path("withdraw/commit/", views.withdraw_commit_view, name="withdrawCommit"),
]