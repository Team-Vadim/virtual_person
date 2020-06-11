from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth import password_validation
from .tokens import account_activation_token
from .forms import *
import json
import vk_api
from .models import Bot
from virtualperson.settings import DEBUG
from os import system as shell


def signup(request):
    """
    Страница регистрации. Отправляет письмо на указанную почту со ссылкой для подтверждения

    :param request: запрос Django
    """

    if request.method == 'POST':
        if 'username' in request.POST and 'email' not in request.POST \
                and 'password1' not in request.POST and 'password2' not in request.POST:
            username_occupation = User.objects.filter(username=request.POST['username']).exists()
            return HttpResponse(content_type='json', content=json.dumps({'username_occupation': username_occupation, }))
        if 'email' in request.POST and 'username' not in request.POST \
                and 'password1' not in request.POST and 'password2' not in request.POST:
            email_occupation = User.objects.filter(email=request.POST['email']).exists()
            return HttpResponse(content_type='json', content=json.dumps({'email_occupation': email_occupation, }))

        if 'password1' in request.POST and 'username' not in request.POST \
                and 'email' not in request.POST and 'password2' not in request.POST:
            try:
                password_validation.validate_password(request.POST['password1'])
            except:
                password_incorrect = True
            else:
                password_incorrect = False

            return HttpResponse(content_type='json', content=json.dumps({'is_password_unsafe': password_incorrect, }))

        form = SignUpForm(request.POST)
        if not form.is_valid():
            """
            Реализуется метод захвата ошибки из словаря ошибок Django и вывод ошибки пользователю.
            """
            errors = str(form.errors)
            count = 0
            mess = ''
            for i in errors:
                if i == '>':
                    count += 1
                if count == 4:
                    mess += i
                    if i == '<':
                        break
            mess = mess[1: -1]
            return render(request, 'registration/signup.html', {
                'mess': mess,
                'form': SignUpForm(),
            })

        user = form.save(commit=False)  # это точно нужно?
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Активация аккаунта'
        message = render_to_string('registration/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email],
        )
        email.send()
        return render(request, 'registration/email_activate_message.html')
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {
            'form': SignUpForm(),
        })
    return HttpResponse(status=405)


def activate(request, uidb64, token):
    """
    Этот метод нужен для подтверждения адреса электронной почте. При переходе по ссылке из письма, адрес подтверждается.

    :param request: Запрос Django
    :param uidb64:
    :param token: токен, отправленный в письме
    :return: страница 'Email подтверждён' / HTTP 409 'Conflict'
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'registration/email_confirmed.html', {})

    return HttpResponse('Activation link is invalid!',
                        status=409)  # 409 'Conflict' - запрос конфликтует с текущим состоянием сервера


def main(request):
    """
    Главная страница
    
    :param request: Запрос Django
    """
    max_bot_id = Bot.objects.count()
    # max_user_id = User.objects.aggregate(Max('id')).get('id__max')
    max_user_id = User.objects.count()
    if max_bot_id is None: max_bot_id = 0
    if max_user_id is None: max_user_id = 0
    count_bot_active = 0
    for bot in Bot.objects.all():
        if bot.active_posts or bot.active_messages or bot.active_friends:
            count_bot_active += 1
    return render(request, 'startpage.html', {
        'user': request.user.id,
        'count_bot_all': max_bot_id,
        'count_user': max_user_id,
        'count_bot_active': count_bot_active,
    })


@login_required
def lk(request, user_id):
    """
    Личный кабинет

    :param request: Запрос Django
    :param user_id: ID пользователя
    """
    if request.user.id != user_id:
        return render(request, 'error_account.html')

    if request.method == 'GET':
        list_of_bots = Bot.objects.filter(owner=request.user)

        bots_one_by_three = []

        for i in range(0, len(list_of_bots), 3):
            tmp_arr = [list_of_bots[i]]
            if i + 1 < len(list_of_bots):
                tmp_arr.append(list_of_bots[i + 1])
            if i + 2 < len(list_of_bots):
                tmp_arr.append(list_of_bots[i + 2])
            bots_one_by_three.append(tmp_arr)

        return render(request, 'lk.html', {
            'id': request.user.id,
            'bots': bots_one_by_three,
        })
    elif request.method == 'DELETE':
        user = User.objects.get(pk=request.user.pk)
        user.delete()
        return HttpResponse(status=200, content='Пользователь удалён')
    return HttpResponse(status=405)


@login_required
def bot_view(request, pk):
    """
    Информация о боте

    :param request: Запрос Django
    :param pk: ID бота
    """
    if request.method == 'GET':
        try:
            bot = Bot.objects.get(pk=pk)
            pass_for_bot = '*' * len(bot.password)  # security xD
            bot.password = 'Nothing!'  # security xD
            bot.age = str(Bot.AGE_CHOICES[bot.age - 1][1])  # надо тестить
            bot.gender = Bot.SEX_CHOICES[bot.gender - 1][1]
            for crontime, label in Bot.TIME_CHOICES:
                if crontime == bot.time:
                    bot.time = label
                    break

            bot.active_posts = 'Да' if bot.active_posts else 'Нет'
            bot.active_messages = 'Да' if bot.active_messages else 'Нет'
            bot.active_friends = 'Да' if bot.active_friends else 'Нет'

            return render(request, 'bot.html', {
                'bot': bot,
                'user_id': request.user.id,
                'hidden_pass': pass_for_bot,
                'bot_form': BotSettings,
            })
        except Bot.DoesNotExist:
            return HttpResponse(status=404)
    if request.method == 'DELETE':
        bot = Bot.objects.get(pk=pk)
        bot_deactivate_vk_posts(pk=pk)
        bot.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)


def bot_activate_vk_posts(time: str, pk: int):
    """
    Функция активации бота

    :param time: Время запуска бота
    :type time: str
    :param pk: ID бота
    :type pk: int
    """
    activate_venv = '/home/$(whoami)/virtual-person/venv/bin/python'
    command = 'echo "{time} $(whoami) {activate_venv} /home/$(whoami)/virtual-person/website/bot/posts_to_vk.py {id}" ' \
              '> /home/$(whoami)/virtual-person/website/bot/cron/{id}.cron'.format(time=time, id=pk,
                                                                                   activate_venv=activate_venv)
    shell(command)


def bot_deactivate_vk_posts(pk: int):
    """
    Функция деактивации бота

    :param pk: ID бота
    :type pk: int
    """
    shell('rm /home/$(whoami)/virtual-person/website/bot/cron/{pk}.cron'.format(pk=pk))


@login_required()
def all_bots(request):
    """
    Добавление нового бота

    :param request: Запрос Django
    """
    if request.method == 'GET':
        return render(request, 'add_bot.html', {
            'bots': Bot.objects.filter(owner=request.user),
            'form': BotSettings(),
            'mess': '',
        })
    if request.method == 'POST':
        data = BotSettings(request.POST)
        if not data.is_valid():
            print(data.errors)
            return HttpResponse(status=400)

        owner = request.user
        age = data.cleaned_data['age']
        gender = data.cleaned_data['gender']
        social_network = data.cleaned_data['social_network']
        login = data.cleaned_data['login']
        name = login
        password = data.cleaned_data['password']
        active_messages = data.cleaned_data['active_messages']
        active_posts = data.cleaned_data['active_posts']
        time = data.cleaned_data['time']
        active_friends = data.cleaned_data['active_friends']
        if Bot.objects.filter(
                login=login,
                social_network=social_network
        ).exists():
            return render(request, 'add_bot.html', {
                'bots': Bot.objects.filter(owner=request.user),
                'form': BotSettings,
                'mess': 'Бот с данными параметрами уже существует!',
            })

        # Условие для проверки валидности данных для аккаунта ВК
        if not DEBUG and client_auth(login=login, password=password):
            return render(request, 'add_bot.html', {
                'bots': Bot.objects.filter(owner=request.user),
                'form': BotSettings,
                'mess': 'Неправильный логин и пароль от Вконтакте',
            })

        bot = Bot(
            name=name,
            owner=owner,
            age=age,
            social_network=social_network,
            gender=gender,
            login=login,
            password=password,
            active_messages=active_messages,
            active_posts=active_posts,
            time=time,
            active_friends=active_friends
        )
        bot.save()
        if active_posts:
            bot_activate_vk_posts(time, bot.pk)

        return render(request, 'bot_saved.html', {
            'bot': bot,
            'user_id': request.user.id,
            'new_bot': True,
        })
    return HttpResponse(status=405)


def edit_bot(request, bot_id):
    """
    Редактирования существующего бота.

    :param request: Запрос Django.
    :param bot_id: ID редактируемого бота.
    """
    try:
        bot = Bot.objects.get(id=bot_id)
        form = BotSettings(initial={
            'name': str(bot.name),
            'age': str(bot.age),
            'gender': str(bot.gender),
            'social_network': bot.social_network,
            'login': bot.login,
            'password': bot.password,
            'active_messages': bot.active_messages,
            'active_posts': bot.active_posts,
            'active_friends': bot.active_friends,
            'time': bot.time,
        }, auto_id=False)
    except Bot.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        return render(request, 'edit_bot.html', {
            'bots': Bot.objects.filter(owner=request.user),
            'form': form,
            'mess': '',
        })

    if request.method == 'POST':
        data = BotSettings(request.POST)
        if not data.is_valid():
            return HttpResponse(status=400)

        active_posts = data.cleaned_data['active_posts']
        time = data.cleaned_data['time']
        login = data.cleaned_data['login']
        password = data.cleaned_data['password']
        bot.name = data.cleaned_data['name']
        bot.age = data.cleaned_data['age']
        bot.gender = data.cleaned_data['gender']
        bot.social_network = data.cleaned_data['social_network']
        bot.login = login
        bot.password = password
        bot.active_messages = data.cleaned_data['active_messages']
        bot.active_posts = active_posts
        bot.active_friends = data.cleaned_data['active_friends']
        bot.time = time
        if not DEBUG and client_auth(login=login, password=password):
            return HttpResponse(status=400)
        try:
            bot.save()
        except:
            return render(request, 'edit_bot.html', {
                'bots': Bot.objects.filter(owner=request.user),
                'form': form,
                'mess': 'Бот с данными параметрами уже существует!',
            })
        if active_posts:
            bot_activate_vk_posts(time, bot.pk)
        else:
            bot_deactivate_vk_posts(bot.pk)

        return render(request, 'bot_saved.html', {
            'bot': bot,
            'user_id': request.user.id,
            'new_bot': False,
        })
    return HttpResponse(status=405)


def client_auth(login, password):
    """
    Проверка подлиности логина и пароля от Вконтакте

    :param login: Логин пользователя Вконтакте
    :type login: str
    :param password: Пароль пользователя Вконтакте
    :type password: str
    """
    vk_session = vk_api.VkApi(login=login, password=password)
    try:
        vk_session._vk_login()
        return 0
    except:
        return -1
