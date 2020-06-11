from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Bot


class SignUpForm(UserCreationForm):
    """
    Форма регистрации
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'reg_input', 'placeholder': " "}))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={'class': 'reg_input',
                                                                                                 'type': 'email',
                                                                                                 'placeholder': " "}))
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'reg_input', 'autocomplete': 'new-password', 'placeholder': " "}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'reg_input', 'autocomplete': 'new-password', 'placeholder': " "}),
        strip=False,
    )

    def clean_password2(self):
        """
        Проверка, что поля ввода для паролей совподают

        :return: пароль
        :rtype: str
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def clean_email(self):
        """
        Проверка на свободность почты

        :return: почтовый адрес email
        :rtype: str
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    class Meta:
        """
        Вспомогательный класс
        """
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class VkAccount(forms.Form):
    """
    Форма для ввода логина и пароля от аккаунта во Вконтакте
    """
    login = forms.CharField(label='Логин', max_length=500, min_length=1, widget=forms.PasswordInput)
    password = forms.CharField(label='Пароль', max_length=500, min_length=1, widget=forms.PasswordInput)


class BotSettings(forms.Form):
    """
    Форма создания и редактирования бота
    """
    age = forms.ChoiceField(label='Возраст', choices=Bot.AGE_CHOICES,widget=forms.Select(attrs={'class':'select-selected'}))
    gender = forms.ChoiceField(label='Пол', choices=Bot.SEX_CHOICES,widget=forms.Select(attrs={'class':'select-selected'}))
    social_network = forms.ChoiceField(label='Социальная сеть', choices=Bot.SOCIAL_NETWORK_CHOICES,widget=forms.Select(attrs={'class':'select-selected'}))
    time = forms.ChoiceField(label='Постить раз в', choices=Bot.TIME_CHOICES,widget=forms.Select(attrs={'class':'select-selected'}))
    name = forms.CharField(min_length=1, required=False)
    login = forms.CharField(min_length=1)
    password = forms.CharField(min_length=1)
    active_messages = forms.BooleanField(label='Отвечать на сообщения', initial=False, required=False)
    active_posts = forms.BooleanField(label='Писать посты', initial=False, required=False)
    active_friends = forms.BooleanField(label='Принимать в друзья', initial=False, required=False)
