from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'Почта',
            'password': 'Пароль',
        }


class UserRegisterForm(forms.ModelForm):
    agreement = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Необходимо дать согласие'}
    )
    class Meta:
        model = User
        fields = 'name', 'email', 'password'
        labels = {
            'name': 'Ник',
            'email': 'Почта',
            'password': 'Пароль',
        }
