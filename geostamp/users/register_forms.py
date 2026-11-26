from django import forms
from .models import User

class LoginForm(forms.Form):                                                #Форма входа (Не привязана к сохранению в БД из-за Form)
    email = forms.EmailField()                                              #Поле ввода почты (автоматическая форма)
    password = forms.CharField(widget=forms.PasswordInput)                  #Поле ввода пароля (автоматическая форма)
    class Meta:                                                             #Вложенный класс метаданных (для обычной forms.Form он не работает Meta используется только в ModelForm)
        model = User                                                        #Указатель модели (игнорируют Forms.Form)
        fields = ('email', 'password')                                      #Список полей модели (также игнорируется в forms.Form)
        labels = {                                                          #Словарь полей
            'email': 'Почта',
            'password': 'Пароль',
        }


class UserRegisterForm(forms.ModelForm):                                    #Создает форму регистрации, напрямую связанную с моделью БД
    agreement = forms.BooleanField(                                         #Поле чек бокса
        label='Согласие на обработку персональных данных',
        required=True,                                                      #Делаем это поле обязательным
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
        labels = {
            'password': 'Новый пароль',
        }