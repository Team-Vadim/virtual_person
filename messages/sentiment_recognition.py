from deeppavlov import configs, build_model
import socket
import pickle


class SentimentModel:
    """
    Модель для определения эмоционального окраса предложения. Основана на модели deeppavlov rusentiment
    (см https://docs.deeppavlov.ai/en/0.1.6/components/classifiers.html)
    """
    def __init__(self):
        """
        Модель из библиотеки deeppavlov, определяет эмоционыльный окрас русского предложения
        Подробнее на docs.deeppavlov
        """
        self.model = build_model(configs.classifiers.rusentiment_elmo_twitter_cnn, download=True)
        # Параметры в скобках - корпус твиттера, разрешение на докачивание данных

    def get_sentiment(self, argument):
        """
        Возвращает настроение входного предложения (текста)

        :param argument: Предложение (текст)
        :type argument: str
        :return: Настроение
        :rtype: str
        """
        return self.model([argument])


sentiment_model = SentimentModel()

SERVER_ADDRESS = ('localhost', 8899)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(10)
print('Сервер запущен, CTRL+С для остановки')

while True:
    connection, address = server_socket.accept()
    print("new connection from {address}".format(address=address))
    data = str(connection.recv(4096).decode(encoding='utf-8'))
    print("Query >", data)
    sentiment = sentiment_model.get_sentiment(data)
    print("Answer >", sentiment)
    data = pickle.dumps(sentiment)
    connection.sendall(data)
    connection.close()
