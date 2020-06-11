#!/bin/python3
import add_friends
from threading import Thread
import interaction_with_db


def main(table_name='accounts_bot'):
    """
    Запускает add_friends.add_all_new_friends() для каждого бота в отдельном потоке

    :param table_name: Имя таблицы с ботами в БД
    :type table_name: str
    """
    cur = interaction_with_db.get_cursor()
    cur.execute("SELECT id FROM {}".format(table_name))
    id_bots = (cur.fetchall())
    threads = []

    for id_bot in id_bots:
        threads.append(Thread(target=add_friends.add_all_new_friends, args=(interaction_with_db.get_bot_data(cur, id_bot['id']),)))
        threads[-1].start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()

