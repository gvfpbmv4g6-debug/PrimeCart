from django.shortcuts import render
from django.db.models import Q

from .models import ShoppingCategory, ShoppingItem


def main(request):
    categories = ShoppingCategory.objects.all()

    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    return render(request, "shopping/main.html", {
        "categories": categories,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })


def search_result(request):
    category_id = request.GET.get("category")
    keyword = request.GET.get("keyword")

    items = ShoppingItem.objects.all()

    # カテゴリ検索
    if category_id:
        items = items.filter(category_id=category_id)

    # キーワード検索：商品名で検索
    if keyword:
        items = items.filter(name__icontains=keyword)

    categories = ShoppingCategory.objects.all()

    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    return render(request, "shopping/serchResult.html", {
        "items": items,
        "categories": categories,
        "selected_category": category_id,
        "keyword": keyword,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })