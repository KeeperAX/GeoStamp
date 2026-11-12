from django.shortcuts import render
from users.register_forms import LoginForm, UserRegisterForm


def home_view(request):
    return render(request, 'home.html', {
        'avt': LoginForm(),
        'reg': UserRegisterForm(),
    })
