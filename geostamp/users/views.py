from django.shortcuts import render, redirect
from .register_forms import UserRegisterForm, LoginForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.core import signing
from django.http import HttpResponse
from .email_verification import create_verification_token, read_verification_token


def verify_email(request, token):
    try:
        data = read_verification_token(token)

    except signing.SignatureExpired:
        return HttpResponse('Срок действия ссылки истёк.')

    except signing.BadSignature:
        return HttpResponse('Недействительная ссылка.')

    user = User.objects.filter(
        id=data.get('user_id'),
        email=data.get('email'),
        password=data.get('password')
    ).first()

    if user is None:
        return HttpResponse('Недействительная ссылка.')

    if user.email_confirmed:
        return HttpResponse('Почта уже подтверждена.')

    if request.method == 'POST':
        user.email_confirmed = True
        user.save(update_fields=['email_confirmed'])

        request.session.cycle_key()
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session.pop('pending_email', None)

        return redirect('home')

    return render(request, 'front/style/verify_email.html')

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

            user = User.objects.filter(email=email).first()

            if user and check_password(password, user.password):
                if not user.email_confirmed:
                    form.add_error(
                        None,
                        'Сначала подтвердите электронную почту.'
                    )
                else:
                    request.session.cycle_key()
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('home')
            else:
                form.add_error(None, 'Неверная почта или пароль')

    else:
        form = LoginForm()

    return render(request, 'front/login.html', {'avt': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(
                form.cleaned_data['password']
            )
            user.email_confirmed = False
            user.save()

            token = create_verification_token(user)

            url = request.build_absolute_uri(
                reverse('verify_email', args=[token])
            )

            send_mail(
                'Подтверждение почты GeoStamp',
                f'Перейдите по ссылке:\n{url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            print('Ссылка подтверждения:', url)

            request.session['pending_email'] = user.email

            return redirect('home')

    else:
        form = UserRegisterForm()

    return render(request, 'front/register.html', {'reg': form})

def logout_view(request):
    request.session.flush()
    return redirect('home')