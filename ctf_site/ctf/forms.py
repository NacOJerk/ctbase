from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='שם משתמש')
    password = forms.CharField(label='סיסמא')


class Empty(forms.Form):
    pass
