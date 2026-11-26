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


def login_view(request):                                                #Функция для обработки входа пользователя
    if request.method == 'POST':                                        #Проверяет, была ли отправлена форма (метод POST)
        form = LoginForm(request.POST)                                  #Создает экземпляр входа и заполняет его данными, пришедшими от пользователя
        if form.is_valid():                                             #Валидация формы
            email = form.cleaned_data['email']                          #проверяем форму и проверяем отчищенное значение
            password = form.cleaned_data['password']
            try:                                                        #Проверка если пользователь не найден
                user = User.objects.get(email=email, password=password) #Ищет в БД ровно одного пользователя с точным совпадением почты и пароля
                request.session['user_id'] = user.id                    #Сохраняет id пользователя в сессию
                request.session['user_name'] = user.name                #Сохраняет имя пользователя в сессию
                return redirect('home')                                 #перенаправляет на главную страницу
            except User.DoesNotExist:
                form.add_error(None, 'Неверная почта или пароль')
    else:
        form = LoginForm()                                              # Создает пустую форму входа
    return render(request, 'home.html', {           #Для рендеринга
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


def logout_view(request):   # Функцияе для выхода из аккаунта
    request.session.flush() # Полностью очищает данные текущей сессии
    return redirect('home') # Перенаправляет пользователя на главную страницу