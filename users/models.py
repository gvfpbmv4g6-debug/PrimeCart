from django.db import models


class LoginUser(models.Model):
    
    user_id = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "account_user"


class AdministratorAdmin(models.Model):
    
    admin_id = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = "administrator_admin"