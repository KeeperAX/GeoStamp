from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password, identify_hasher
from django.utils.crypto import constant_time_compare
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
    if request.method != 'POST':
        return render(request, 'front/login.html', {'avt': LoginForm()})

    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.filter(email=email).first()
        if user is not None:
            try:
                identify_hasher(user.password)
                password_ok = check_password(password, user.password)
                legacy_password = False
            except ValueError:
                # Совместимость с ранее сохранёнными паролями в открытом виде.
                legacy_password = True
                password_ok = constant_time_compare(password, user.password)
            if password_ok:
                if legacy_password:
                    user.password = make_password(password)
                    user.save(update_fields=['password'])
                request.session.cycle_key()
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('home')
        error = 'Неверная почта или пароль.'
    else:
        error = None

    return render(request, 'home.html', {'avt': form, 'login_error': error}, status=400)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            request.session.cycle_key()
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('home')
    else:
        form = UserRegisterForm()
    if request.method == 'POST':
        return render(request, 'home.html', {
            'reg': form,
            'avt': LoginForm(),
            'register_modal_open': True,
        }, status=400)

    return render(request, 'front/register.html', {'reg': form})


def logout_view(request):
    request.session.flush()
    return redirect('home')

