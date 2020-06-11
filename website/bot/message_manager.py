#!/bin/python3
import message_to_vk
from threading import Thread
import interaction_with_db


def main(table_name='accounts_bot'):
    """
    Запускает message_to_vk.message() для каждого бота в отдельном потоке
    """
    cur = interaction_with_db.get_cursor()
    cur.execute("SELECT id FROM {}".format(table_name))
    id_bots = (cur.fetchall())
    threads = []

    for id_bot in id_bots:
        threads.append(Thread(target=message_to_vk.message, args=(interaction_with_db.get_bot_data(cur, id_bot['id']),)))
        threads[-1].start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
    from os import system
    system('echo OK > ~/test.txt')
