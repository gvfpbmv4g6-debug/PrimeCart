from django.db import models
from users.models import LoginUser

class ShoppingCategory(models.Model):
    
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "shopping_category"


class ShoppingItem(models.Model):
    
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    manufacturer = models.CharField(max_length=32)
    color = models.CharField(max_length=16)
    price = models.IntegerField()
    stock = models.IntegerField()
    recommended = models.BooleanField(max_length=1, default=False)
    category = models.ForeignKey(
        ShoppingCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "shopping_item"


class ShoppingItemsincart(models.Model):
    
    amount = models.IntegerField()
    booked_date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(
        ShoppingItem,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        LoginUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "shopping_itemsincart"


class ShoppingPurchase(models.Model):
    
    purchase_id = models.IntegerField(primary_key=True)
    destination = models.CharField(max_length=256)
    booked_date = models.DateTimeField(auto_now_add=True)
    cancel = models.BooleanField(max_length=1, default=False)
    user = models.ForeignKey(
        LoginUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "shopping_purchase"


class ShoppingPurchaseDtail(models.Model):
    
    purchase_detail_id = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    booked_date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(
        ShoppingItem,
        on_delete=models.CASCADE,
    )
    purchase = models.ForeignKey(
        ShoppingPurchase,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "shopping_purchasedetail"
