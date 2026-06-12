from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import LoginUser


def login_view(request):
    error_message = ""

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        user = LoginUser.objects.filter(user_id=user_id).first()

        if user is not None and check_password(password, user.password):
            request.session["login_user_id"] = user.user_id
            request.session["login_name"] = user.name
            return redirect("shopping:main")
        else:
            error_message = "ユーザーIDまたはパスワードが違います。"

    return render(request, "login/login.html", {
        "error_message": error_message
    })


def register_view(request):
    error_message = ""

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        name = request.POST.get("name")
        address = request.POST.get("address")

        
        if password != confirm_password:
            error_message = "パスワードが一致しません。"

        elif LoginUser.objects.filter(user_id=user_id).exists():
            error_message = "このユーザーIDは既に使われています。"
        else:
            request.session["register_data"] = {
                "user_id": user_id,
                "password": make_password(password),
                "name": name,
                "address": address,
            }
            return redirect("users:registerUserConfirm")

    return render(request, "login/register.html", {
        "error_message": error_message
    })


def register_confirm_view(request):
    register_data = request.session.get("register_data")

    if register_data is None:
        return redirect("users:register")

    if request.method == "POST":
        if LoginUser.objects.filter(user_id=register_data["user_id"]).exists():
            return render(request, "login/registerUserConfirm.html", {
                "register_data": register_data,
                "error_message": "このユーザーIDは既に使われています。"
            })

        LoginUser.objects.create(
            user_id=register_data["user_id"],
            password=register_data["password"],
            name=register_data["name"],
            address=register_data["address"]
        )

        del request.session["register_data"]

        return redirect("users:login")

    return render(request, "login/registerUserConfirm.html", {
        "register_data": register_data
    })


def success_view(request):
    login_name = request.session.get("login_name")

    if login_name is None:
        return redirect("users:login")

    return render(request, "login/success.html", {
        "login_name": login_name
    })

def logout_view(request):
    request.session.flush()
    return redirect("shopping:main")