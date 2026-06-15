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

        request.session["register_name"] = register_data["name"]
        del request.session["register_data"]

        return redirect("users:registerUserCommit")

    return render(request, "login/registerUserConfirm.html", {
        "register_data": register_data
    })


def register_commit_view(request):
    register_name = request.session.get("register_name")
    return render(request, "login/registerUserCommit.html", {
        "register_name": register_name,
    })


def user_info_view(request):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    return render(request, "login/userInfo.html", {
        "user": user
    })


def logout_view(request):
    request.session.flush()
    return redirect("shopping:main")


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


def update_user_view(request):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    error_message = ""

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                error_message = "パスワードが一致しません。"
                return render(request, "login/updateUser.html", {
                    "user": user,
                    "error_message": error_message,
                })

            request.session["update_data"] = {
                "name": name,
                "address": address,
                "password": make_password(password),
                "password_changed": True,
            }
        else:
            request.session["update_data"] = {
                "name": name,
                "address": address,
                "password": "",
                "password_changed": False,
            }

        return redirect("users:updateUserConfirm")

    return render(request, "login/updateUser.html", {
        "user": user,
        "error_message": error_message,
    })


def update_user_confirm_view(request):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    update_data = request.session.get("update_data")

    if update_data is None:
        return redirect("users:updateUser")

    if request.method == "POST":
        user.name = update_data["name"]
        user.address = update_data["address"]

        if update_data["password_changed"]:
            user.password = update_data["password"]

        user.save()

        request.session["login_name"] = user.name

        del request.session["update_data"]

        return redirect("users:updateUserCommit")

    return render(request, "login/updateUserConfirm.html", {
        "user": user,
        "update_data": update_data,
    })

def update_user_commit_view(request):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    return render(request, "login/updateUserCommit.html", {
        "user": user
    })

def withdraw_confirm_view(request):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    if request.method == "POST":
        withdraw_name = user.name

        request.session["withdraw_name"] = withdraw_name

        user.delete()

        request.session.pop("login_user_id", None)
        request.session.pop("login_name", None)

        return redirect("users:withdrawCommit")

    return render(request, "login/withdrawConfirm.html", {
        "user": user
    })


def withdraw_commit_view(request):
    withdraw_name = request.session.get("withdraw_name")

    if withdraw_name is None:
        withdraw_name = "会員"

    request.session.pop("withdraw_name", None)

    return render(request, "login/withdrawCommit.html", {
        "withdraw_name": withdraw_name
    })