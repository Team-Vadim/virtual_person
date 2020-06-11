#!/bin/python3
import sys
sys.path.insert(0, '/home/website/virtual-person')
from interaction_with_VK import methods
sys.path.insert(0, '/home/website/virtual-person/website/bot')
import interaction_with_db


def add_all_new_friends(bot_data):
    """
    Одобряет все запросы в друзья

    :param bot_data: данные бота
    :type bot_data: list
    """
    if bot_data['active_friends'] == 1:
        friends_methods = methods.Friends(login=bot_data['login'], password=bot_data['password'])
        friends_methods.add_all_new_friends()
