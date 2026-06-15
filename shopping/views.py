from django.shortcuts import render, redirect
from .models import ShoppingCategory, ShoppingItem, ShoppingItemsincart, LoginUser


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

def item_detail(request, item_id):
    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    item = ShoppingItem.objects.filter(item_id=item_id).first()

    if item is None:
        return redirect("shopping:main")

    if request.method == "POST":
        amount = int(request.POST.get("amount"))

        cart_item = ShoppingItemsincart.objects.filter(
            user=user,
            item=item
        ).first()

        if cart_item is None:
            ShoppingItemsincart.objects.create(
                user=user,
                item=item,
                amount=amount
            )
        else:
            cart_item.amount += amount
            cart_item.save()

        return redirect("shopping:cart")

    amount_list = range(1, item.stock + 1)

    return render(request, "shopping/itemDetail.html", {
        "item": item,
        "amount_list": amount_list,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })

def cart_view(request):
    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    cart_items = ShoppingItemsincart.objects.filter(user=user)

    for cart_item in cart_items:
        cart_item.subtotal = cart_item.item.price * cart_item.amount

    return render(request, "shopping/cart.html", {
        "cart_items": cart_items,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })