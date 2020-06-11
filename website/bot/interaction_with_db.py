import pymysql
from pymysql.cursors import DictCursor


DATABASE_NAME = 'virtualperson_db'
USER = 'virtualperson_user'
PASSWORD = 'v1rtualpers0n_pa55'
HOST = '127.0.0.1'
PORT = '3306'


def get_cursor():
    con = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE_NAME,
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    cur = con.cursor()
    return cur


def get_bot_data(cur=get_cursor(), id_bot=None, table_name='accounts_bot'):
    """
    Возвращает id, login, password, age, gender, active_posts, active_messages, active_friends для бота из БД

    :param cur: Курсор БД
    :param id_bot: id бота
    :type id_bot: int
    :param table_name: Имя таблицы с ботами в БД
    :type table_name: str
    """
    cur.execute("SELECT id, login, password, age, gender, active_posts, active_messages, active_friends FROM {} WHERE id={}".format(table_name, id_bot))
    data = cur.fetchall()
    return data[0]
