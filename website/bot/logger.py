import datetime
import sys
sys.path.insert(0, '/home/website/virtual-person')
from interaction_with_VK import methods


def get_save_path(bot_data, type_log):
    """
    Возвращает персональный путь для сохранения логов для каждого бота
    """
    user_info = methods.get_users_name(login=bot_data['login'], password=bot_data['password'])[0]
    user_name = user_info['first_name'] + user_info['last_name']
    save_path = '/home/website/virtual-person/website/bot/logs/{type_log}/log-posts_vk-name-{name}_vk-id-{id}'.format(type_log=type_log, name=user_name, id=user_info['id'])
    return save_path


class Logger():
    """
    Сохраняет сообщение(лог) в определенный файл
    """
    def __init__(self, save_path='~/virtual-person/website/bot/logs'):
        """
        :param save_path: Путь для сохранения лога
        :type save_path: str
        """
        self.save_path = save_path
        self.time_now = datetime.datetime.now()

    def save_log(self, log_message):
        """
        :param log_message: Содержимое лога
        :type log_message: str
        """
        log = '\n*-------*****-------*\nLOG:\n {log}\nTIME: {time}\n*-------------------*'.format(log=log_message, time=str(self.time_now))
        log_file = open(self.save_path, 'a')
        log_file.write(log)
        log_file.close()


