from django import forms
from .models import LoginUser


class RegisterForm(forms.Form):
    user_id = forms.CharField(
        label="ユーザーID",
        max_length=32,
        required=True
    )

    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        required=True
    )

    confirm_password = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        required=True
    )

    name = forms.CharField(
        label="名前",
        max_length=100,
        required=True
    )

    address = forms.CharField(
        label="住所",
        max_length=255,
        required=True
    )

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")

        if LoginUser.objects.filter(user_id=user_id).exists():
            raise forms.ValidationError("このユーザーIDは既に使われています。")

        return user_id

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("パスワードが一致しません。")

        return cleaned_data