from django.shortcuts import render, redirect
from .register_forms import UserRegisterForm, LoginForm
from .models import User

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=email, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = LoginForm()
#     return render(request, 'front/login.html', {'avt': form})
#
# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             login(request, form.save())
#             return redirect('home')
#
#     else:
#         form = UserRegisterForm()
#
#     return render(request, 'front/register.html', {'reg': form})
# def logout_view(request):
#     logout(request)
#     return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('home')
            except User.DoesNotExist:
                form.add_error(None, 'Неверная почта или пароль')
    else:
        form = LoginForm()
    return render(request, 'home.html', {
        'avt': form,
        'reg': UserRegisterForm(),
        'open_login_modal': True
    })


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'home.html', {
        'avt': LoginForm(),
        'reg': form,
        'open_register_modal': True
    })


def logout_view(request):
    request.session.flush()
    return redirect('home')