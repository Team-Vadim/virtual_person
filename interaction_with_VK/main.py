import vk_api
from settings import *
from methods import *
import os, time

vk = client_auth()


def download_wall(vk=vk, id=1, no_repost=False, path="data/default.txt"):
    """
    Тестовая функция, демонстрирующая возможность скачивать стену пользователя.
    Если вы получили "vk_api.exceptions.ApiError: [29] Rate limit reached", или любую другую ошибку -
    то попробуйте запустить код завтра
    Что с этим делать, пока неясно.
    -------
    ВНИМАНИЕ, ВЫЗЫВАЯ ЭТОТ МЕТОД - ВЫ ТЕРЯЕТЕ СОДЕРЖИМОЕ ФАЙЛА
    -------
    """
    wall = get_big_wall(vk_session=vk, user_id=id)
    f = open(path, 'a', encoding='utf-8')
    for post in wall['items']:
        if no_repost:
            if 'copy_history' not in post and post['text'] != '':  # Поле 'copy_history' возвращается только с репостом. Нет поля - не репост.
                ok_status = True # переменая, определяющая, записываем ли мы текст поста в файл
                for i in STOP_WORDS:
                    if i in post['text']:
                        ok_status = False
                if ok_status:
                    string = post['text'].replace("\n", "")
                    f.write(string + ' ')
        else:
            #f.write('\n' + ': ' + post['text'])
            """
            Здесь будет выполнять код, который будет исполняться в случае, если нам необходимо будет скачать все со стены,
            включать репосты. На данный момент эта возможность не нужна.
            """
            pass
    f.close()


while True:
    """
    Данные от аккаунта берутся из settings.py
    Отправка сообщения:
    логин пароль 0 id_кому_отправляем сообщение
    
    Получение новых сообщений:
    логин пароль 1
    Новые сообщения оказываются в файле messages.txt
    
    Пост:
    логин пароль 2 Текст_поста
    """
    action = str(input())
    login = action[:action.find(' ')]
    action = action[(action.find(' ') + 1):]
    password = action[:action.find(' ')]
    action = action[(action.find(' ') + 1):]
    if action[0] == '0':
        action = action[2:]
        id, message = action[:action.find(' ')], action[(action.find(' ') + 1):]
        send_message(message=message, user_id=id, login=login, password=password)
    elif action[0] == '1':
        get_new_messages(login=login, password=password)
    elif action[0] == '2':
        action = action[2:]
        message = action[(action.find(' ') + 1):]
        create_post(message=message, login=login, password=password)
    else:
        pass
