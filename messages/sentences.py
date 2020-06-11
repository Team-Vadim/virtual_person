from pymorphy2 import MorphAnalyzer
from nltk.tokenize import sent_tokenize
# from sentiment_recognition import sentiment_model
# from syntax_characteristics import syntax_model
from error_correction import correct_spelling
import pickle
import socket

port_sentiment_recognition = 8899
port_syntax_characteristics = 9988


class Message:
    """
    Объект сообщения для получения связи слов
    """
    def __init__(self, message_input):
        """
        Инициализация объекта для обработки сообщения

        :param message_input: полученнойе сообщение
        :type message_input: str
        """
        self.message_input = message_input
        self.message = correct_spelling(message_input)  # Исправленные входные данные
        self.sentences = []
        self.sentences_characteristics = []
        self.message_sentiment = ''
        self.sentence_structure_arr = []
        self.message_relations_list = []
        self.morph = MorphAnalyzer()

    def recognize_sentiment(self):
        """
        Эмоциональный окрас сообщения будет определен с точностью до таких категорий:
        1) positive
        2) negative
        3) neutral
        4) speech
        5) skip - невозможно определить окрас из-за отсутствия контекста
        """
        self.message_sentiment = get_reply(self.message, port_sentiment_recognition)

    def parse_into_sentences(self):
        """
        Разбиение текста на предложения. Замены с частицой не. Определение типов предложений
        """
        self.sentences = sent_tokenize(self.message)
        for sentence in self.sentences:  # тип предложения (повествовательное/ восклицательное/ вопрос)
            sentence = sentence.replace("не ", "не+")
            sentence = sentence.replace("Не ", "Не+")
            sentence = sentence.replace("НЕ ", "НЕ+")
            temporary_dictionary = {}
            if '?' in sentence:
                sentence_type = 'question'
            elif '!' in sentence:
                sentence_type = 'exclamation'
            else:
                sentence_type = 'narration'
            temporary_dictionary['sentence_type'] = sentence_type
            self.sentences_characteristics.append(temporary_dictionary)

    def find_sentences_structure(self):
        """
        Структура предложения из syntax_characteristics.py
        """
        for sentence in self.sentences:
            sent_structure = get_reply(sentence, port_syntax_characteristics)
            self.sentence_structure_arr.append(sent_structure)

    def get_relation(self):
        """
        Определение зависимостей слов по id их <родителей> (тех, от кого они зависят)
        """
        for sent in self.sentence_structure_arr:
            sent_array = []
            for word in sent:
                dictionary = {'word': word[1], 'role': word[3]}
                sent_array.append([dictionary])
            for word in sent:
                if word[3] != "punct" and word[3] != "cc" and word[3] != "case":
                    sent_array[int(word[2]) - 1].append(word[1])
            self.message_relations_list.append(sent_array)

    def delete_punctuation(self):
        """
        Удаление пунктуации, союзов, предлогов
        """
        for sent in self.message_relations_list:
            for word in sent:
                if word[0]["role"] == "punct" or word[0]["role"] == "cc" \
                        or word[0]["role"] == "case":
                    sent.remove(word)
            last_word = sent[len(sent) - 1]
            if last_word[0]["role"] == "punct" or last_word[0]["role"] == "cc" \
                    or last_word[0]["role"] == "case":
                sent.remove(last_word)

    def get_result(self):
        """
        Возвращяется распарсенный текст

        :return:
        1) Эмоциональный окрас сообщения
        2) Если в сообщении 1 предложение, то возвращается список из типа предложения и списка зависимостей слов
                -> Словарь с текущим словом, с ключами "word" (само слово) и "role" - функция в предложении
                    -> Подлежащее обозначается как "nsubj"
                -> Если есть, слова, зависящие от данного слова
            Если в предложении более 1 предложения, возвращается такой список для последнего
        :rtype: tuple
        """
        self.recognize_sentiment()
        self.parse_into_sentences()
        self.find_sentences_structure()
        self.get_relation()
        self.delete_punctuation()
        res_array = []
        for i in range(0, len(self.message_relations_list)):
            res_array.append(self.sentences_characteristics[i])
            res_array.append(self.message_relations_list[i])
        if len(res_array) > 1:
            return self.message_sentiment, res_array[len(res_array) - 2: len(res_array)]
        return self.message_sentiment, res_array


def get_message_attributes():
    """
    Получение аттрибутов сообщения

    :return: Список характиристик и список слов
    :rtype: tuple(list, list)
    """
    aaa = Message(input())
    sentiment, characteristics = aaa.get_result()
    print("эмоциональный окрас предложения", sentiment)
    words = []
    chars = []
    for i in range(0, len(characteristics)):
        if i == 0:
            print(characteristics[i])
            chars.append(characteristics)
        else:
            print("Зависимости слов")
            for j in characteristics[i]:
                print(j)
                words.append(j)
    return chars, words


def get_reply(question, port):
    """
    Получение ответа

    :param question: Вопрос
    :type question: str
    :param port: Порт генератора
    :type port: int
    :return: Ответ
    :rtype: str
    """
    data = bytearray()
    address_to_server = ('localhost', port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address_to_server)
    client.send(bytes(question, encoding='UTF-8'))
    data += client.recv(8192)
    res = pickle.loads(data)
    client.close()
    return res
