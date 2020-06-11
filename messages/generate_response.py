from markov_sentence_generator import MarkovModel
from markov_sentence_generator import SentenceGenerator
from error_correction import API_URL_BASE, correct_spelling
from sentences import Message
from itertools import chain
import random
import os
import socket
import sys


def parce_input():
	"""
	Чтение копуса сообщений

	:return: Корпус сообщений
        :rtype: list
	"""
	file = open('/home/website/virtual-person/messages/korpus.txt', "r", encoding="utf8")
	data = file.read()
	data = data.replace('\n', '')
	korpus = data.split(' ')
	file.close()
	return korpus


def get_message(message):
	"""
	Получение сообщений

	:param message: Сообщение
        :type message: str
	:return: Список характеристик и список слов
        :rtype: tuple(list, list)
	"""
	analised_message = Message(message)
	sentiment, characteristics = analised_message.get_result()
	words = []
	chars = []
	for i in range(0, len(characteristics)):
		if i == 0:
			chars.append(characteristics[i])
		else:
			for j in characteristics[i]:
				words.append(j)
	return chars, words


def get_data_for_answer(words):
	"""
	Получение информации из сообщения для ответа

	:param words:Список слов
        :type words: list
	:return: Начальное слово и список добавленных слов
        :rtype: tuple(str, list)
	"""
	start_word = None
	added_words = []
	if len(words) > 1:
		for word in words:
			actual_word = word[0]['word'].lower()
			if word[0]['role'] == 'nsubj':
				if actual_word == 'я':
					start_word = 'Ты'
				elif actual_word == 'ты':
					start_word = 'Я'
				elif actual_word == 'мы':
					start_word = 'Мы'
				elif actual_word == 'вы':
					start_word = 'Я'
				else:
					start_word = actual_word
		for word in words:
			actual_word = word[0]['word'].lower()
			if word[0]['role'] == 'root':
				if start_word == None:
					start_word = actual_word
				else:
					added_words.append(actual_word)
		for word in words:
			actual_word = word[0]['word'].lower()
			if word[0]['role'] != 'root' and word[0]['role'] != 'nsubj':
				if start_word == None:
					start_word = actual_word
				else:
					added_words.append(actual_word)
	return start_word, added_words


def get_data_for_narrative(words):
	"""
	Получение информации из сообщения для повествования

	:param words: Список слов
        :type words: list
	:return: Начальное слово и список добавленных слов
        :rtype: tuple(str, list)
	"""
	start_word = None
	added_words = []
	for word in words:
		actual_word = word[0]['word']
		if word[0]['role'] == 'nsubj':
			start_word = actual_word
	for word in words:
		actual_word = word[0]['word']
		if word[0]['role'] == 'root':
			if start_word == None:
				start_word = actual_word
			else:
				added_words.append(actual_word)
	for word in words:
		actual_word = word[0]['word']
		if word[0]['role'] != 'root' and word[0]['role'] != 'nsubj':
			if start_word == None:
				start_word = actual_word
			else:
				added_words.append(actual_word)
	return start_word, added_words


def analize_message(chars, words):
	"""
	Анализ сообщения

	:param chars: Список характеристик
        :type chars: list
	:param words: Список слов
        :type words: list
	:returns: Начальное слово и список добавленных слов
        :rtype: tuple(str, list)
	"""
	start_word = ''
	added_words = []
	if chars['sentence_type'] == 'question':
		start_word, added_words = get_data_for_answer(words)
	elif chars['sentence_type'] == 'narration':
		start_word, added_words = get_data_for_narrative(words)
	elif chars['sentence_type'] == 'exclamation':
		start_word, added_words = get_data_for_narrative(words)
	return start_word, added_words


def main():
        """
        Функция main
        """
        data = parce_input()  # Обучающий корпус
        ORDER = 3
        LENGTH = 20
        START_WORD = 'Я'
        ENDING = '.'
        ADDED_WORDS = ['пришёл', 'домой', 'ура']
        PREVIOUS_END = '.'
        sent_gen = SentenceGenerator(data)  # Создание модели.
        # sent_gen.markov_model_order_1/2/3.model - извлечь модель
        print(sys.getsizeof(sent_gen))
        # запуск сокетов
        stop = False
        # ip, port
        SERVER_ADDRESS = ('localhost', 6666)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen(10)
        print('Сервер запущен, CTRL+С для остановки')
        # запуск сокетов
        ORDER = 2
        # for i in range(20):
        #     sent = sent_gen.generate_random_sentence(ORDER, LENGTH, START_WORD, ENDING, ADDED_WORDS, PREVIOUS_END)
        #     sent_gen.print(ORDER, sent)
        while True:
                connection, address = server_socket.accept()
                print("new connection from {address}".format(address=address))
                # message = input()
                message = str(connection.recv(4096).decode(encoding='utf-8'))
                print("Query >", message)
                if len(message) == 0:
                        print('ERROR: Kakojto debil vvel pustuyu stroku')
                        continue
                inp_length = len(message)
                chars, words = get_message(message)
                chars = chars[0]
                start_word, added_words = analize_message(chars, words)
                ending = None
                previous_end = None
                if chars['sentence_type'] == 'question':
                        previous_end = '?'
                        ending = '.'
                else:
                        previous_end = '.'
                        ending = '.'
                LENGTH = inp_length + random.randint(0, 3)
                sent = sent_gen.generate_random_sentence(ORDER, LENGTH, start_word, ending, added_words, previous_end)
                answer = sent_gen.print(ORDER, sent)
                answer = correct_spelling(' '.join(answer))
                print("Answer >", answer)
                connection.send(bytes(answer, encoding='UTF-8'))
                connection.close()


main()
