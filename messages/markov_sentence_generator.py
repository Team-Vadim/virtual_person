from histograms import Dictogram
#from database_interaction import database
import random
from collections import deque
import re
import sys


class MarkovModel:
	"""
	Модель цепи Маркова
	"""
	def __init__(self, order, data):
		"""
		:param order: 
                :type order: int
		:param data: Корпус
                :type data: list
		"""
		self.order = order
		self.model = self.make_markov_model(order, data)

	def make_markov_model(self, order, data):
		"""
		Создание модели

		:param order:
                :type order: int
		:param data: Корпус
                :type data: list
		:return: Марковская модель
                :rtype: dict
		"""
		markov_model = dict()
		print(len(data))
		for i in range(0, len(data)-order):
			window = tuple(data[i: i+order])
			if i % 100000 == 0:
				print(i/100000)
			if window in markov_model:
				markov_model[window].update([data[i+order]])
			else:
				markov_model[window] = Dictogram([data[i+order]])
		return markov_model 


class SentenceGenerator:
	"""
	Класс генератора сообщений
	"""
	# Марковские модели вгружаются из бд, на ходу генерация для тестов
	def __init__(self, data=None):
		"""
		:param data: Корпус
                :type data: list
		"""
		# if data:
		#     self.markov_model_order_1 = MarkovModel(1, data)
		# self.markov_model_order_1 = "DB.download(markov_model_order_1)"
		# if data:
		self.markov_model_order_2 = MarkovModel(2, data)
		# self.markov_model_order_2 = "DB.download(markov_model_order_2)"
		# if data:
		#     self.markov_model_order_3 = MarkovModel(3, data)
		# self.markov_model_order_3 = "DB.download(markov_model_order_3)"

	def update_markov_models(self, new_data):
		"""
		Замена старых марковских моделей на обновлённые.

		:param new_data: Новый корпус
                :type new_data: list
		"""
		self.markov_model_order_1 = MarkovModel(1, new_data)
		self.markov_model_order_2 = MarkovModel(2, new_data)
		self.markov_model_order_3 = MarkovModel(3, new_data)
		self.update_DB()

	# Cохранение марковских моделей в БД после их обновления
	def update_DB(self):
		pass

	def check_substring(self, main_str, checked_str, window_size=4):
		"""
		Проверка подстроки

		:param main_str: Главная строка
                :type main_str: str
		:param checked_str: Cтрока, которую надо проверить в главной
                :type checked_str: str
		:param window_size: Ширина окна
                :type window_size: int
		:rtype: bool
		"""
		main_str = main_str.strip()
		main_str = main_str.lower()
		checked_str = checked_str.strip()
		checked_str = checked_str.lower()
		tmp_str = ''
		if len(main_str) < window_size:
			if main_str.lower() == checked_str.lower():
				return True
			else:
				return False
		else:
			window_index = 0
			for i in range(window_index, window_size + window_index):
				tmp_str += main_str[i]

			for i in range(len(main_str) - window_size + 1):
				if tmp_str.lower() in checked_str.lower():
					return True
				window_index += 1
				new_tmp_str = ''
				for i in range(window_index, window_size + window_index):
					if i < len(main_str):
						new_tmp_str += main_str[i]
				tmp_str = new_tmp_str

			return False

	'''and (key[1] == added_word or key[2] == added_word)'''
	def generate_start_part(self, order, markov_model, start_word, added_word, previous_sent):
		# return random.choice(list(markov_model.keys()))
		"""
		Генерация начальной части

		:param order:
                :type order: int
		:param markov_model: Марковская модель
                :type markov_model: dict
		:param start_word: Стартовое слово
                :type start_word: str
		:param added_word: Добавленное слово
                :type added_word: str
		:param previous_sent:
		:rtype: int
		"""
		all_keys = list(markov_model.keys())
		acceptable_keys = []
		if order == 1:
			for key in all_keys:
				if self.check_substring(key[0], start_word):
					acceptable_keys.append(key)
		elif order == 2:
			for key in all_keys:
				if self.check_substring(key[0], start_word) and self.check_substring(key[1], added_word):
					acceptable_keys.append(key)
		elif order == 3:
			for key in all_keys:
				if key[0] == start_word and (key[1] == added_word or key[2] == added_word):
					acceptable_keys.append(key)
		'''chosen_key = random.choice(acceptable_keys)
		start_word = markov_model[chosen_key].return_weighted_random_word()
		acceptable_keys = []
		for key in all_keys:
			if key[0] == start_word:
				acceptable_keys.append(key)'''
		start_part = random.choice(acceptable_keys)  
		return start_part

	def generate_better_start_part(self, order, markov_model, start_w, added_word, previous_end):
		"""
		Генерация улучшенное начальной части

		:param order:
                :type order: int
		:param markov_model: Марковская модель
                :type markov_model: dict
		:param start_w: Стартовое слово
                :type start_w: str
		:param added_word: Добавленное слово
                :type added_word: str
		:param previous_end:
		:rtype: int
		"""
		all_keys = list(markov_model.keys())
		acceptable_keys = []
		prior_acceptable_keys = []
		'''for key in all_keys:
			for i in range(order):
				if i == 0: 
					if not self.check_substring(start_w, key[i]):
						all_keys.remove(key)
				else:
					if not self.check_substring(added_word, key[i]):
						all_keys.remove(key)

				if i == order-1:
					acceptable_keys.append(key)'''
		if start_w:
			if order == 3:
				for key in all_keys:
					if added_word:
						if key[0] == start_w and (added_word in  key[1] or added_word in key[2]):
							prior_acceptable_keys.append(key)
					else:
						if start_w in key[0]:
							acceptable_keys.append(key)
			elif order == 2:
				for key in all_keys:
					if added_word:
						if start_w.lower() == key[0].lower() and self.check_substring(added_word, key[1]):
							prior_acceptable_keys.append(key)
					else:
						if start_w.lower() == key[0].lower():
							acceptable_keys.append(key)
			elif order == 1:
				for key in all_keys:
					if self.check_substring(start_w, key[0]):
						prior_acceptable_keys.append(key)

			all_keys = []
			all_keys = list(markov_model.keys()) 
			if prior_acceptable_keys:
				return random.choice(prior_acceptable_keys)
			elif acceptable_keys:
				return random.choice(acceptable_keys)
			else:
				return random.choice(all_keys)
		else:
			return random.choice(all_keys)

	def make_next_part(self, order, old_window, next_word):
		"""
		Создание следующей части

		:param order:
                :type order: int
		:param old_window: Старое окно
                :type old_window: int
		:param next_word: Следующее слово
                :type next_word: str
		:return: Список новых окон
                :rtype: list
		"""
		new_window = []
		for i, item in enumerate(old_window):
			if i != 0:
				new_window.append(item)
		new_window.append(next_word)
		return tuple(new_window)

	def make_final_part(self, order, markov_model, first_word, ending):
		"""
		Создание следующей части

		:param order:
                :type order: int
		:param markov_model: Марковская модель
                :type markov_model: dict
		:param first_word: Первое слово
                :type firts_word: str
		:param ending: Последнее слово
                :type ending: str
		:rtype: list
		"""
		all_keys = list(markov_model.keys())
		acceptable_keys = []
		for item in all_keys:
			if item[0] == first_word and item[order-1] == ending:
				acceptable_keys.append(item)
		if not acceptable_keys:
			for item in all_keys:
				if item[order-1] == ending:
					acceptable_keys.append(item)
		return list(random.choice(acceptable_keys))

	def make_appended_part (self, order, current_part):
		"""
		Создание добавочной части

		:param order:
                :type order: int
		:param current_part: Текущая часть
                :type current_part: list
		:rtype: list
		"""
		appended_part = []
		appended_part.append(current_part[order-1])
		return tuple(appended_part)

	def generate_random_sentence(self, order, length, start_word, ending, added_words, previous_end):
		"""
		Генерация рандомного предложения

		:param order:
                :type order: int
		:param length: Длина предложения
                :type length: int
		:param start_word: Первое слово
                :type start_word: str
		:param ending: Последнее слово
                :type ending: str
		:param added_words: Список добавленных слов
                :type added_words: list
		:param previous_end:
		:return: Список частей предложения
                :rtype: list
		"""
		if order == 1:
			markov_model = self.markov_model_order_1.model
		elif order == 2:
			markov_model = self.markov_model_order_2.model
		elif order == 3:
			markov_model = self.markov_model_order_3.model
		added_word_num = 0
		if added_words:
			current_part = self.generate_better_start_part(order, markov_model, start_word, added_words[added_word_num], previous_end)
		else:
			current_part = self.generate_better_start_part(order, markov_model, start_word, None, previous_end)
		added_word_num += 1
		sentence = [current_part]
		for i in range(0, length):
			if current_part in markov_model:
				if i < length - order - 1:	
					current_dictogram = markov_model[current_part]
					if added_word_num >= len(added_words):
						next_word_made = current_dictogram.return_weighted_random_word()
					else:
						next_word_made = current_dictogram.return_weighted_random_word(added_words[added_word_num])
					if next_word_made[1] == 'random_word':
						next_word = next_word_made[0]
					elif next_word_made[1] == 'added_word':
						next_word = next_word_made[0]
						added_word_num += 1
					if next_word == ending or next_word == '.' or next_word == '!' or next_word == '?':
						sentence.append(ending)
						return sentence
					next_part = self.make_next_part(order, current_part, next_word)
					current_part = next_part
					appended_part = self.make_appended_part(order, current_part)
					sentence.append(appended_part)
				else:
					current_dictogram = markov_model[current_part]
					next_word = current_dictogram.return_weighted_random_word()
					final_part = self.make_final_part(order, markov_model, next_word, ending)
					sentence.append(final_part)
					break
		return sentence

	def generate_question(self, order):
		if order == 1:
			markov_model = self.markov_model_order_1.model
		elif order == 2:
			markov_model = self.markov_model_order_2.model
		elif order == 3:
			markov_model = self.markov_model_order_3.model

	def generate_exzlamation(self):
		pass

	def generate_narrative(self):
		pass

	def print(self, order, sentence):
		"""
		Возврат предложения

		:param order:
                :type order: int
		:param sentence: Список частей предложения
                :type sentence: list
		:return: Список слов в предложении
                :rtype: list
		"""
		sent = []
		for part in sentence:
			for word in part:
				sent.append(word)
		return sent


def parce_input():
	"""
	Обработка корпуса

	:return: Корпус
        :rtype: list
	"""
	file = open('/home/website/virtual-person/messages/korpus.txt', "r", encoding="utf8")
	data = file.read()
	data = data.replace('\n', ' ')
	data = data.replace('$', ' ')
	korpus = data.split(' ')
	korpus = list(filter(('').__ne__, korpus))
	print('*')
	return korpus


def main():
	data = parce_input()  # Обучающий корпус
	ORDER = 3
	LENGTH = 7
	START_WORD = 'привет'
	ENDING = '?'
	ADDED_WORDS = ['как', 'дела', 'ура']
	PREVIOUS_END = '.'
	sent_gen = SentenceGenerator(data)  # Создание модели.
	print('*')
	# database.insert_data(sent_gen.markov_model_order_2.model)
	# print('*')
	# sent_gen.markov_model_order_1/2/3.model - извлечь модель
	# print(sys.getsizeof(sent_gen))
	for i in range(20):
		sent = sent_gen.generate_random_sentence(ORDER, LENGTH, START_WORD, ENDING, ADDED_WORDS, PREVIOUS_END)
		sent_gen.print(ORDER, sent)

