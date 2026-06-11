from django.db import models


class LoginUser(models.Model):
    db_table = "users"
    user_id = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id