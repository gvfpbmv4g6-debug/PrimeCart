from django.shortcuts import render, redirect
from django.db.models import Max
from .models import ShoppingCategory, ShoppingItem, ShoppingItemsincart, ShoppingPurchase, ShoppingPurchaseDtail
from users.models import LoginUser


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

    selected_category_name = "すべて"

    if category_id:
        items = items.filter(category_id=category_id)

        selected_category = ShoppingCategory.objects.filter(category_id=category_id).first()
        if selected_category is not None:
            selected_category_name = selected_category.name

    if keyword:
        items = items.filter(name__icontains=keyword)

    categories = ShoppingCategory.objects.all()

    return render(request, "shopping/serchResult.html", {
        "items": items,
        "categories": categories,
        "selected_category": category_id,
        "selected_category_name": selected_category_name,
        "keyword": keyword,
        "login_user_id": request.session.get("login_user_id"),
        "login_name": request.session.get("login_name"),
    })

def item_detail(request, item_id):
    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    item = ShoppingItem.objects.filter(item_id=item_id).first()

    if item is None:
        return redirect("shopping:main")

    amount_list = range(1, item.stock + 1)

    if request.method == "POST":
        if login_user_id is None:
            return redirect("users:login")

        user = LoginUser.objects.filter(user_id=login_user_id).first()

        if user is None:
            return redirect("users:login")

        amount = int(request.POST.get("amount"))

        if amount <= 0:
            return redirect("shopping:item_detail", item_id=item.item_id)

        if amount > item.stock:
            return render(request, "shopping/itemDetail.html", {
                "item": item,
                "amount_list": amount_list,
                "login_user_id": login_user_id,
                "login_name": login_name,
                "error_message": "在庫数を超えています。",
            })

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

        item.stock -= amount
        item.save()

        return redirect("shopping:cart")

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

    total_price = 0

    for cart_item in cart_items:
        cart_item.subtotal = cart_item.item.price * cart_item.amount
        total_price += cart_item.subtotal

        max_amount = cart_item.amount + cart_item.item.stock
        cart_item.amount_list = range(1, max_amount + 1)

    return render(request, "shopping/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })

def cart_update(request, cart_id):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    cart_item = ShoppingItemsincart.objects.filter(
        id=cart_id,
        user=user
    ).first()

    if cart_item is None:
        return redirect("shopping:cart")

    if request.method == "POST":
        new_amount = int(request.POST.get("amount"))

        item = cart_item.item
        old_amount = cart_item.amount

        if new_amount <= 0:
            item.stock += old_amount
            item.save()
            cart_item.delete()
            return redirect("shopping:cart")

        diff = new_amount - old_amount

        if diff > 0:
            if diff > item.stock:
                return redirect("shopping:cart")

            item.stock -= diff
            item.save()

        elif diff < 0:
            item.stock += abs(diff)
            item.save()

        cart_item.amount = new_amount
        cart_item.save()

    return redirect("shopping:cart")

def cart_delete(request, cart_id):
    login_user_id = request.session.get("login_user_id")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    cart_item = ShoppingItemsincart.objects.filter(
        id=cart_id,
        user=user
    ).first()

    if cart_item is None:
        return redirect("shopping:cart")

    if request.method == "POST":
        item = cart_item.item

        item.stock += cart_item.amount
        item.save()

        cart_item.delete()

    return redirect("shopping:cart")

def get_next_purchase_id():
    max_id = ShoppingPurchase.objects.aggregate(Max("purchase_id"))["purchase_id__max"]

    if max_id is None:
        return 1

    return max_id + 1


def get_next_purchase_detail_id():
    max_id = ShoppingPurchaseDtail.objects.aggregate(Max("purchase_detail_id"))["purchase_detail_id__max"]

    if max_id is None:
        return 1

    return max_id + 1

def purchase_view(request):
    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    cart_items = ShoppingItemsincart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect("shopping:cart")

    total_price = 0

    for cart_item in cart_items:
        cart_item.subtotal = cart_item.item.price * cart_item.amount
        total_price += cart_item.subtotal

    if request.method == "POST":
        destination = request.POST.get("destination")
        payment_method = request.POST.get("payment_method")

        if not destination:
            return render(request, "shopping/purchase.html", {
                "cart_items": cart_items,
                "total_price": total_price,
                "user": user,
                "login_user_id": login_user_id,
                "login_name": login_name,
                "error_message": "住所を入力してください。",
            })

        purchase = ShoppingPurchase.objects.create(
            purchase_id=get_next_purchase_id(),
            destination=destination,
            payment_method=payment_method,
            user=user,
        )

        for cart_item in cart_items:
            ShoppingPurchaseDtail.objects.create(
                purchase_detail_id=get_next_purchase_detail_id(),
                amount=cart_item.amount,
                item=cart_item.item,
                purchase=purchase,
            )

        cart_items.delete()

        request.session["purchase_id"] = purchase.purchase_id

        return redirect("shopping:purchaseCommit")

    return render(request, "shopping/purchase.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "user": user,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })

def purchase_commit_view(request):
    purchase_id = request.session.get("purchase_id")

    request.session.pop("purchase_id", None)

    return render(request, "shopping/purchaseCommit.html", {
        "purchase_id": purchase_id,
    })

def purchase_history_view(request):
    login_user_id = request.session.get("login_user_id")
    login_name = request.session.get("login_name")

    if login_user_id is None:
        return redirect("users:login")

    user = LoginUser.objects.filter(user_id=login_user_id).first()

    if user is None:
        return redirect("users:login")

    purchases = ShoppingPurchase.objects.filter(
        user=user,
        cancel=False
    ).order_by("-booked_date")

    purchase_histories = []

    for purchase in purchases:
        details = ShoppingPurchaseDtail.objects.filter(purchase=purchase)

        total_price = 0

        for detail in details:
            detail.subtotal = detail.item.price * detail.amount
            total_price += detail.subtotal

        payment_method = getattr(purchase, "payment_method", "")

        if payment_method == "credit":
            payment_method_label = "クレジット"
        elif payment_method == "cash_on_delivery":
            payment_method_label = "代金引換"
        else:
            payment_method_label = "未設定"

        purchase_histories.append({
            "purchase": purchase,
            "details": details,
            "total_price": total_price,
            "payment_method_label": payment_method_label,
        })

    return render(request, "shopping/purchaseHistory.html", {
        "purchase_histories": purchase_histories,
        "login_user_id": login_user_id,
        "login_name": login_name,
    })