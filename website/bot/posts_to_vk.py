#!/bin/python3
import sys
from random import randint
sys.path.insert(0, '/home/website/virtual-person/creating_posts/markov')
import markov
sys.path.insert(0, '/home/website/virtual-person')
from interaction_with_VK import methods
from sys import argv
sys.path.insert(0, '/home/website/virtual-person/website/bot')
import interaction_with_db
import orthography
from logger import Logger, get_save_path


def post(size_sent, bot_data):
    """
    Вызывает генератор постов

    :param size_sent: Количесвто предложений в посте
    :type size_sent: int
    :param bot_data: данные бота
    :type bot_data: list
    """
    logger = Logger(get_save_path(bot_data, type_log='posts'))
    if bot_data['active_posts'] == 1:
        database = 'AGE{}SEX{}'.format(bot_data['age'], bot_data['gender'])
        generator = markov.MarkovGenerator(markov.MarkovGenerator.GenerateStrategy(database=database, window_size=3))
        tmp_post = generator.generate_sentence(size_sent=size_sent)
        post = orthography.orthography(tmp_post)
        logger.save_log(log_message=post)
        methods.create_post(post, login=bot_data['login'], password=bot_data['password'])
    else:
        logger.save_log(log_message='flag "active_posts" in mysql: {}'.format(bot_data['active_posts']))


def main():
    size_post = (int(argv[2]) if len(argv) > 2 else randint(1, 2))
    post(size_sent=size_post, bot_data=interaction_with_db.get_bot_data(id_bot=int(argv[1])))


if __name__ == '__main__':
    main()
