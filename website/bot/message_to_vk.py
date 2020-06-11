import sys
import socket
sys.path.insert(0, '/home/website/virtual-person')
from interaction_with_VK import methods
from logger import Logger, get_save_path

port_neural_network = 8667
port_test = 6666

ports = {
    'port_AGE1SEX1': 10000,
    'port_AGE1SEX2': 10001,
    'port_AGE2SEX1': 10002,
    'port_AGE2SEX2': 10003,
    'port_AGE3SEX1': 10004,
    'port_AGE3SEX2': 10005,
    'port_AGE4SEX1': 10006,
    'port_AGE4SEX2': 10007
}


def get_reply(question, port):
    """
    Отдает и принимает данные для опередленного сокета

    :param question: Отдаваемые данные
    :type question: str
    :param port: Порт сокета
    :type port: int
    """
    address_to_server = ('localhost', port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes(question, encoding='UTF-8'))
    answer = str(client.recv(4096).decode(encoding='utf-8'))
    client.close()
    return answer


def message(bot_data):
    """
    Отвечает на сообщения в непрочитанных диалогах. В диалоге отвечает на последнее сообщение.

    :param bot_data: данные бота
    :type bot_data: list
    """
    logger = Logger(get_save_path(bot_data, type_log='messages'))
    log = ''
    if bot_data['active_messages'] == 1:
        all_messages = methods.get_new_messages(login=bot_data['login'], password=bot_data['password'])
        if len(all_messages) != 0:
            for new_message in all_messages:
                pair = new_message[0]
                message= ''
                log += 'Query: ' + pair['text'] + '\n'
                if pair['text'].lower().find('тебя зовут') != -1:
                    message += 'Меня зовут {}. '.format(methods.get_users_name(login=bot_data['login'], password=bot_data['password'])[0]['first_name'])
                if pair['text'].lower().find('тебе лет') != -1:
                    try:
                        message += 'Мне {}'.format(2020 - int((methods.get_users_name(login=bot_data['login'], password=bot_data['password']))[0]['bdate'].split('.')[2]))
                    except IndexError:
                        if bot_data['age'] == 1:
                            message += 'Я зумер)'
                        elif bot_data['age'] == 2 and bot_data['gender'] == 1:
                            message += 'Разменял второй десяток (или третий)'
                        elif bot_data['age'] == 2 and bot_data['gender'] == 2:
                            message += 'Разменяла второй десяток (или третий)'
                        elif bot_data['age'] == 3:
                            message += 'Мне от 35 до 50 ;)'
                        elif bot_data['age'] == 4:
                            message += 'У меня есть книга "50 вещей, которые нужно сделать после 50"'
                else:
                    message = get_reply(pair['text'], port_neural_network)
                if message == 'None':
                    port_generator = 'port_AGE{}SEX{}'.format(bot_data['age'], bot_data['gender'])
                    message = get_reply(pair['text'], ports[port_generator])
                log += 'Answer: ' + message
                logger.save_log(log)   
                methods.send_message(message, pair['id'], bot_data['login'], bot_data['password'])
    else:
        logger.save_log(log_message='flag "active_messages" in mysql: {}'.format(bot_data['active_messages']))
