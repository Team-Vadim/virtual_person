from deeppavlov import build_model, configs
import socket
import pickle


class SyntaxModel:
    """
    Модель для определения синтаксических связей. Основана на модели deeppavlov syntagrus model
    (см http://docs.deeppavlov.ai/en/master/features/models/syntaxparser.html)
    """
    def __init__(self):
        self.model = build_model(configs.syntax.syntax_ru_syntagrus_bert, download=True)

    def get_structure(self, sentence):
        """
        Возвращает массив зависимостей в предложении. Для каждого слова хранятся:
        ->Порядковый номер (id)
        -> Само слово
        -> То, от чего это слово зависит (id <родителя>)\
        -> Роль в предложении

        :param sentence: Входное предложение
        :type sentence: str
        :return: Массив зависимостей в предложении
        :rtype: list
        """
        sentence_characteristics = []
        for parse in self.model([sentence]):
            characteristic = parse.replace("_", "")
            temporary_array = characteristic.split('\n')
            for char in temporary_array:
                characteristic_to_arr = char.split()
                if characteristic_to_arr:
                    sentence_characteristics.append(characteristic_to_arr)
        return sentence_characteristics


syntax_model = SyntaxModel()

SERVER_ADDRESS = ('localhost', 9988)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print('Сервер запущен, CTRL+С для остановки')

while True:
    connection, address = server_socket.accept()
    print("new connection from {}".format(address))
    data = str(connection.recv(4096).decode(encoding='utf-8'))
    print("Query >", data)
    structure = syntax_model.get_structure(data)
    print("Answer >", structure)
    data = pickle.dumps(structure)
    connection.sendall(data)
    connection.close()
