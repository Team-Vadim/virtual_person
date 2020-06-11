"""
Методы для работы с vk
"""
import json
import random
import urllib.request
from pydub import AudioSegment
import speech_recognition

import requests
import vk_api
import vk_messages

import sys
sys.path.insert(0, '/home/website/virtual-person')
from interaction_with_VK import settings


def auth_code():
    """
    Функция для обработки двухфакторной аутентификации

    :return: Код для двухфакторной аутентификации
    :rtype: tuple(str, bool)
    """
    tmp = input('Введи код: ')
    return tmp, True


def client_auth(login=settings.LOGIN, password=settings.PASSWORD):
    """
    Авторизация

    :param login: Логин от аккаунта во Вконтакте
    :type login: str
    :param password: Пароль от аккаунта во Вконтакте
    :type password: str
    :rtype: class VkApiMethod
    """
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_code)
    try:
        vk_session.auth(token_only=True)  # token_only - оптимальная стратегия авторизации (?)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return None
    vk_session.auth()
    return vk_session.get_api()


def get_big_wall(vk_session, user_id=1):
    """
    Метод для скачивания стены во Вконтакте

    :param vk_session: Передаём авторизованную сессию VkApi
    :type vk_session: class VkApi
    :param user_id: Передаём ID пользователя, чью стенку надо получить
    :type user_id: int
    :return: Возвращается стена пользователя. Записи - 'items', кол-во - 'count'
    :rtype: dict
    """
    tools = vk_api.VkTools(vk=vk_session)
    # Работа с Big Data в vk_api: https://vk-api.readthedocs.io/en/latest/tools.html
    wall = tools.get_all(method='wall.get', max_count=settings.MAX_COUNT,
                         values={'owner_id': user_id}, limit=None)
    return wall


def get_users_list(vk_session, vk_q="", sex=0, age_from=1, age_to=99, country=1,
                   has_photo=1, limit=100000, max_count=1000):
    """
    Метод для получения списка пользователей со схожими параметрами

    :param vk_session: Передаём авторизованную сессию VkApi
    :type vk_session: class VkApi
    :param vk_q:
    :type vk_q: str
    :param sex: Пол человека. 0 - неважно, 1 -  Женщина, 2 - Мужской
    :type sex: int
    :param age_from: Начало диапазона просматриваемого возраста
    :type age_from: int
    :param age_to: Конец диапазона просматриваемого возраста
    :type age_to: int
    :param country: 
    :type country: int
    :param has_photo:
    :type has_photo: int
    :param limit:
    :type limit: int
    :param max_count: Максимальное количесво получаемых пользователей
    :type max_count: int
    :return: Возвращается список словарей {'id':id, 'sex': sex, 'age':age}
    :rtype: list
    """
    tools = vk_api.VkTools(vk=vk_session)
    users_json = tools.get_all(method='users.search', max_count=max_count, limit=limit,
                               values={'q': vk_q, 'sex': sex, 'country': country,
                                       'age_from': age_from, 'age_to': age_to,
                                       'has_photo': has_photo})
    print(users_json)
    result = []
    for user in users_json['items']:
        result.append(user['id'])
    return result


def download_users_json(users_json, path):
    """
    Обработка списка пользователей

    :param users_json:
    :type users_json: list
    :param path:
    :type path: str
    """
    user_file = open(path, 'a', encoding='utf-8')
    for user in users_json:
        user_file.write(str(user) + '\n')
    user_file.close()


def send_message(message, user_id, login=settings.LOGIN, password=settings.PASSWORD,
                 have_two_factor_authentication=False):
    """
    Функция для отправки сообщения

    :param message: Сообщение
    :type message: str
    :param user_id: ID пользователя получателя во Вконтакте
    :type user_id: int
    :param login: Логин пользователя отправителя во Вконтакте
    :type login: str
    :param password: Пароль пользователя отправителя во Вконтакте
    :type password: str
    :param have_two_factor_authentication: Есть ли двухфакторная ауетефикация
    :type have_two_factor_authentication: bool
    """
    if len(message) == 0 or len(message) > 4096:
        return
    messages = vk_messages.MessagesAPI(login=login, password=password,
                                       two_factor=have_two_factor_authentication,
                                       cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
    messages.method('messages.send', user_id=str(user_id),
                    message=message, random_id=random.randint(1, 1000000000))


def get_messages(count, user_id, login=settings.LOGIN, password=settings.PASSWORD,
                 have_two_factor_authentication=False):
    """
    Функция для получения новых сообщений из вк

    :param count: Количество сообщений выгружаемых из диалога
    :type count: int
    :param user_id: ID пользователя получателя во Вконтакте
    :type user_id: int
    :param login: Логин пользователя отправителя во Вконтакте
    :type login: str
    :param password: Пароль пользователя отправителя во Вконтакте
    :type password: str
    :param have_two_factor_authentication: Есть ли двухфакторная ауетефикация
    :type have_two_factor_authentication: bool
    :return: Список сообщений
    :rtype: list
    """

    messages = vk_messages.MessagesAPI(login=login, password=password,
                                       two_factor=have_two_factor_authentication,
                                       cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
    history = messages.method('messages.getHistory', user_id=str(user_id), count=count)

    return parse_messages(history)


def create_post(message, login=settings.LOGIN, password=settings.PASSWORD):
    """
    Публикация поста на стену во Вконтакте

    :param message: Текст поста
    :type message: str
    :param login: Логин пользователя во Вконтакте
    :type login: str
    :param password: Пароль пользователя во Вконтакте
    :type password: str
    :return: Список ID непрочитаных диалогов
    :rtype: list
    """
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_code)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_session.auth()
    vk_session.method(method='wall.post', values={'message': message})


def get_unread_dialogs(count=200, login=settings.LOGIN, password=settings.PASSWORD,
                       have_two_factor_authentication=False):
    """
    Получение ID непрочитаных диалогов

    :param count: Количесво получаемых диалогов
    :type count: inr
    :param login: Логин пользователя во Вконтакте
    :type login: str
    :param password: Пароль пользователя во Вконтакте
    :type password: str
    :param have_two_factor_authentication: Есть ли двухфакторная аутентификация
    :type have_two_factor_authentication: bool
    :return: Список ID непрочитаных диалогов
    :rtype: list
    """
    messages = vk_messages.MessagesAPI(login=login, password=password,
                                       two_factor=have_two_factor_authentication,
                                       cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
    history = messages.method('messages.getConversations', filter='unread', count=count)
    id_list = []
    if 'items' in history:
        for conversation in history['items']:
            id_list.append({"id": conversation['conversation']['peer']['id'],
                            "count": conversation['conversation']['unread_count']})

    return id_list


def get_new_messages(login=settings.LOGIN, password=settings.PASSWORD,
                     have_two_factor_authentication=False):
    """
    Получение новых сообщений

    :param login: Логин пользователя во Вконтакте
    :type login: str
    :param password: Пароль пользователя во Вконтакте
    :type password: str
    :param have_two_factor_authentication: Есть ли двухфакторная аутентификация
    :type have_two_factor_authentication: bool
    :return: Список новых сообщение
    :rtype: list
    """
    messages = []
    id_list = get_unread_dialogs(login=login, password=password,
                                 have_two_factor_authentication=have_two_factor_authentication)

    for ids in id_list:
        user_id = ids["id"]
        unread_count = ids["count"]
        if unread_count <= 200:
            messages.append(get_messages(count=str(unread_count), user_id=user_id,
                                         login=login, password=password,
                                         have_two_factor_authentication
                                         =have_two_factor_authentication))
        else:
            messages.append(get_messages(count=200, user_id=user_id,
                                         login=login, password=password,
                                         have_two_factor_authentication
                                         =have_two_factor_authentication))
    return messages


def get_users_name(login=settings.LOGIN, password=settings.PASSWORD):
    """
    Получение информации пользователя во Вконтакте

    :param login: Логин пользователя во Вконтакте
    :type login: str
    :param password: Пароль пользователя во Вконтакте
    :type password: str
    :return: Возвращает вот такой список [{'uid': id пользователя, 'first_name': имя, 'second_name': фамилия, 'bdate': дата рождения}]
    :rtype: list
    """
    vk_session = vk_api.VkApi(login=login, password=password, auth_handler=auth_code)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_session.auth()
    names = (vk_session.method(method='users.get', values={'fields': 'uid, first_name, last_name, bdate'}))
    return names


def parse_messages(history):
    """
    Преобразование словоря сообщений в список

    :param history: Словарь сообщений вк
    :type hidtory: dict
    :return: Список сообщений
    :rtype: list
    """
    message_list = []
    for message in history['items']:
        if message['attachments']:
            if 'audio_message' in message['attachments'][0]:
                audio_url = message['attachments'][0]['audio_message']['link_ogg']
                duration = message['attachments'][0]['audio_message']['duration']
                session = requests.Session()
                data = session.get(audio_url)
                with open('voice.ogg', 'wb') as audio_file:
                    audio_file.write(data.content)
                if int(duration) >= 30:
                    src = "voice.ogg"  # Путь к файлу, который надо конвертировать
                    dst = "voice.wav"  # Путь к итоговому файлу

                    sound = AudioSegment.from_ogg(src)
                    sound.export(dst, format="wav")
                    recog = speech_recognition.Recognizer()
                    sample_audio = speech_recognition.AudioFile('voice.wav')
                    with sample_audio as audio_file:
                        audio_content = recog.record(audio_file)

                    message_list.append({"id": message['from_id'],
                                         "text": recog.recognize_google(audio_content,
                                                                        language='ru')})
                else:
                    data = '{"yandexPassportOauthToken":"Yandex Cloud Token"}'

                    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                                             data=data)
                    token = response.text[16:]
                    token = token[:token.find('"')]
                    folder_id = "Каталог"  # Идентификатор каталога
                    iam_token = token  # IAM-токен

                    with open("voice.ogg", "rb") as audio_file:
                        data = audio_file.read()

                    params = "&".join([
                        "topic=general",
                        "folderId=%s" % folder_id,
                        "lang=ru-RU"
                    ])
                    yandex_url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s'
                    url = urllib.request.Request(yandex_url % params,
                                                 data=data)
                    url.add_header("Authorization", "Bearer %s" % iam_token)

                    response_data = urllib.request.urlopen(url).read().decode('UTF-8')
                    decoded_data = json.loads(response_data)

                    if decoded_data.get("error_code") is None:
                        message_list.append({"id": message['from_id'],
                                             "text": decoded_data.get("result")})
        else:
            message_list.append({"id": message['from_id'], "text": message['text']})

    return message_list


class Friends:
    """
    Класс для обработки заявок в друзья пользователя
    """
    def __init__(self, login=settings.LOGIN, password=settings.PASSWORD,
                 have_two_factor_authentication=False):
        """
        :param login: Логин пользователя во Вконтакте
        :type login: str
        :param password: Пароль пользователя во Вконтакте
        :type password: str
        :param have_two_factor_authentication: Есть ли двухфакторная аунтефикация
        :type have_two_factor_authentication: bool
        """
        self.login = login
        self.password = password
        self.have_two_factor_authentication = have_two_factor_authentication

    def add_friend(self, user_id):
        """
        Метод добавляющий конкретного пользователя

        :param user_id: ID добавляемого человека
        :type user_id: int
        """
        messages = vk_messages.MessagesAPI(login=self.login, password=self.password,
                                           two_factor=self.have_two_factor_authentication,
                                           cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
        messages.method('friends.add', user_id=str(user_id))

    def get_new_friends_list(self):
        """
        Метод получающий список всех заявок в друзья пользователя

        :return: Список ID пользователей
        :rtype: list
        """
        messages = vk_messages.MessagesAPI(login=self.login, password=self.password,
                                           two_factor=self.have_two_factor_authentication,
                                           cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
        return messages.method('friends.getRequests')['items']

    def add_all_new_friends(self):
        """
        Метод одобрающий все заявки в друзья
        """
        new_friends = self.get_new_friends_list()
        for i in new_friends:
            self.add_friend(i)


class Group:
    """
    Класс для работы с сообществом вк
    """
    def __init__(self, group_id, login=settings.LOGIN, password=settings.PASSWORD,
                 have_two_factor_authentication=False):
        """
        :param group_id: ID сообщества во Вконтакте
        :type group_id: int
        :param login: Логин пользователя во Вконтакте
        :type login: str
        :param password: Пароль пользователя во Вконтакте
        :type password: str
        :param have_two_factor_authentication: Есть ли двузфакторная аунтефикация
        :type have_two_factor_authentication: bool
        """
        self.group_id = group_id
        self.login = login
        self.password = password
        self.have_two_factor_authentication = have_two_factor_authentication

    def create_post(self, message):
        """
        Публикация поста на стену сообщества

        :param message: Сообщение на стену сообщества
        :type message: str
        """
        vk_session = vk_api.VkApi(login=self.login, password=self.password, auth_handler=auth_code)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        vk_session.auth()
        vk_session.method(method='wall.post',
                          values={'owner_id': -self.group_id, 'message': message})

    def send_message(self, user_id, message):
        """
        Отправка сообщений сообществу

        :param user_id: ID получателя сообщения
        :type user_id: int
        :param message: Сообщение
        :type message: str
        """
        if len(message) == 0 or len(message) > 4096:
            return
        messages = vk_messages.MessagesAPI(login=self.login, password=self.password,
                                           two_factor=self.have_two_factor_authentication,
                                           cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
        messages.method('messages.send', user_id=str(user_id), group_id=self.group_id,
                        message=message, random_id=random.randint(1, 1000000000))

    def get_unread_dialogs(self, count=200):
        """
        Получение непрочитанных сообщение от сообществ

        :param count: Количество диалогов
        :type count: int
        :return: Возвращает список вот таких словарей {"id": id, "count": количество неспрочитанных сообщений}
        :rtype: list
        """
        messages = vk_messages.MessagesAPI(login=self.login, password=self.password,
                                           two_factor=self.have_two_factor_authentication,
                                           cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
        history = messages.method('messages.getConversations', filter='unread',
                                  count=count, group_id=self.group_id)
        id_list = []
        if 'items' in history:
            for conversation in history['items']:
                id_list.append({"id": conversation['conversation']['peer']['id'],
                                "count": conversation['conversation']['unread_count']})

        return id_list

    def get_messages(self, user_id, count):
        """
        Получение сообщений

        :param user_id: ID переписки
        :type user_id: int
        :param count: Получаемое количество сообщение
        :type count: int
        :return: Список сообщений
        :rtype: list
        """
        messages = vk_messages.MessagesAPI(login=self.login, password=self.password,
                                           two_factor=self.have_two_factor_authentication,
                                           cookies_save_path='/home/website/virtual-person/website/bot/sessions/')
        history = messages.method('messages.getHistory', user_id=str(user_id),
                                  count=count, group_id=self.group_id)

        return parse_messages(history)

    def get_new_messages(self):
        """
        Получение новых сообщений

        :return: Список сообщений
        :rtype: list
        """
        messages = []
        id_list = self.get_unread_dialogs()
        for ids in id_list:
            user_id = ids["id"]
            unread_count = ids["count"]
            if unread_count <= 200:
                messages.append(self.get_messages(count=str(unread_count), user_id=user_id))
            else:
                messages.append(get_messages(count=200, user_id=user_id))
        return messages
