import os
import sys

import MySQLdb
import django
from django.db.models import Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virtualperson.settings')
django.setup()
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from . import views, forms, models
from .models import Bot
from .forms import BotSettings


class WebsiteViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username='test_user', email='test@mail.ru', password='Pr0mpr0g')
        user = User.objects.create_user(username='another_test', email='test1@mail.ru', password='pr0mpr0g')
        user.save()
        self.client = Client()
        self.client.login(username='test_user', password='Pr0mpr0g')
        self.bot = models.Bot(owner=self.user, name='test', age='1', gender='1', social_network='VK', time='*/10 * * '
                                                                                                           '* *',
                              login='test', password='pr0mpr0g')
        self.bot.save()

    def test_main(self):
        request = self.factory.get('')
        request.user = self.user
        response = views.main(request)
        self.assertEqual(response.status_code, 200)

    def test_registration_get_anonymus(self):
        request = self.factory.get('accounts/signup/')
        request.user = AnonymousUser()
        response = views.signup(request)
        self.assertEqual(response.status_code, 200)

    def test_registration_get_logged_in(self):
        request = self.factory.get('accounts/signup/')
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        request = self.factory.post('accounts/signup/', {'username': 'test_user_5', 'email': 'test.promprog@gmail.com',
                                                         'password1': 'Pr0mpr0g', 'password2': 'Pr0mpr0g'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.status_code, 200)

    def test_check_non_exist_login(self):
        request = self.factory.post('accounts/signup/', {'username': 'test_user_5'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"username_occupation": false}')

    def test_check_exist_login(self):
        request = self.factory.post('accounts/signup/', {'username': 'test_user'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"username_occupation": true}')

    def test_check_non_exist_email(self):
        request = self.factory.post('accounts/signup/', {'email': 'test.promprog@gmail.com'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"email_occupation": false}')

    def test_check_exist_email(self):
        request = self.factory.post('accounts/signup/', {'email': 'test@mail.ru'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"email_occupation": true}')

    def test_check_unsafe_password(self):
        request = self.factory.post('accounts/signup/', {'password1': 'qwerty'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"is_password_unsafe": true}')

    def test_check_safe_password(self):
        request = self.factory.post('accounts/signup/', {'password1': 'Qwerty_123'})
        request.user = self.user
        response = views.signup(request)
        self.assertEqual(response.content, b'{"is_password_unsafe": false}')

    def test_right_id_for_lk(self):
        request = self.factory.get('accounts/<int:user_id>/')
        request.user = self.user
        self.client = Client()
        response = views.lk(request, request.user.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        request = self.factory.delete('accounts/<int:user_id>/')
        request.user = self.user
        self.client = Client()
        response = views.lk(request, request.user.id)
        self.assertEqual(response.status_code, 200)

    def test_bot_view_get_method_if_bots_doesnotexist(self):
        request = self.factory.get('bot/<int:pk>/')
        request.user = self.user
        self.client = Client()
        response = views.bot_view(request, self.bot.id + 3)
        self.assertEqual(response.status_code, 404)

    def test_bot_view_get_method_if_bots_are(self):
        request = self.factory.get('bot/<int:pk>/')
        request.user = self.user
        self.client = Client()
        response = views.bot_view(request, self.bot.id)
        self.assertEqual(response.status_code, 200)

    def test_all_bots_get_method(self):
        request = self.factory.get('bot/')
        request.user = self.user
        self.client = Client()
        response = views.all_bots(request)
        self.assertEqual(response.status_code, 200)

    def test_all_bots_create_bot_form_not_valid(self):
        request = self.factory.post('bot/')
        request.user = self.user
        self.client = Client()
        response = views.all_bots(request)
        self.assertEqual(response.status_code, 400)

    def test_edit_bot_does_not_exist(self):
        bot_id = self.bot.id + 3
        request = self.factory.get('edit/<int:bot_id>')
        request.user = self.user
        self.client = Client()
        response = views.edit_bot(request, bot_id)
        self.assertEqual(response.status_code, 404)

    def test_edit_bot_exists(self):
        bot_id = self.bot.id
        request = self.factory.get('edit/<int:bot_id>')
        request.user = self.user
        self.client = Client()
        response = views.edit_bot(request, bot_id)
        self.assertEqual(response.status_code, 200)

    def test_edit_bot_post_invalid(self):
        bot_id = self.bot.id
        request = self.factory.post('edit/<int:bot_id>',
                                    {'age': 'age', 'gender': '1', 'social_network': 'VK', 'time': '*/10 * * * *',
                                     'login': 'test', 'password': 'pr0mpr0g'})
        request.user = self.user
        self.client = Client()
        response = views.edit_bot(request, bot_id)
        self.assertEqual(response.status_code, 400)

    def test_form_bot_pass_min_len(self):
        form = BotSettings()
        self.assertEqual(form.fields['password'].min_length, 1)

    def test_form_bot_name_is_required(self):
        form = BotSettings()
        self.assertFalse(form.fields['name'].required)

    def test_form_bot_name_min_len(self):
        form = BotSettings()
        self.assertEqual(form.fields['name'].min_length, 1)

    def test_form_bot_login_min_len(self):
        form = BotSettings()
        self.assertEqual(form.fields['login'].min_length, 1)

    def test_form_bot_mess_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['active_messages'].label, 'Отвечать на сообщения')

    def test_form_bot_friend_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['active_posts'].label, 'Писать посты')

    def test_form_bot_posts_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['active_friends'].label, 'Принимать в друзья')

    def test_form_bot_mess_is_required(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_messages'].required)

    def test_form_bot_friends_is_required(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_friends'].required)

    def test_form_bot_posts_is_required(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_posts'].required)

    def test_form_bot_mess_is_initial(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_messages'].initial)

    def test_form_bot_friends_is_initial(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_friends'].initial)

    def test_form_bot_posts_is_initial(self):
        form = BotSettings()
        self.assertFalse(form.fields['active_posts'].initial)

    def test_form_bot_age_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['age'].label, "Возраст")

    def test_form_bot_gender_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['gender'].label, "Пол")

    def test_form_bot_social_network_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['social_network'].label, "Социальная сеть")

    def test_form_bot_time_label(self):
        form = BotSettings()
        self.assertEqual(form.fields['time'].label, "Постить раз в")


class WebsiteFormsTestCase(TestCase):
    def test_signup(self):
        form_data = {'username': 'testuser', 'email': 'test@mail.ru', 'password1': 'Pr0mpr0g', 'password2': 'Pr0mpr0g'}
        form = forms.SignUpForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_vk_account(self):
        form_data = {'login': '+79108887654', 'password': 'pr0mpr0g'}
        form = forms.VkAccount(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_bot_form(self):
        form_data = {'age': '1', 'gender': '1', 'social_network': 'VK', 'time': '*/10 * * * *',
                     'login': 'test', 'password': 'pr0mpr0g'}
        form = forms.BotSettings(data=form_data)
        self.assertEqual(form.is_valid(), True)
