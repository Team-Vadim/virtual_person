import random


class Dictogram(dict):
    def __init__(self, iterable=None):
        # Инициализируем наше распределение как новый объект класса, 
        # добавляем имеющиеся элементы

        super(Dictogram, self).__init__()
        self.types = 0  # число уникальных ключей в распределении
        self.tokens = 0  # общее количество всех слов в распределении
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        """
        Обновляем распределение элементами из имеющегося итерируемого набора данных

        :param iterable: optional
        """
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.types += 1
                self.tokens += 1

    def count(self, item):
        """
        Возвращаем значение счетчика элемента, или 0

        :param item: значение
        :return: значение счетчика
        :rtype: int
        """
        if item in self:
            return self[item]
        return 0

    def return_random_word(self):
        """
        Вернуть случайное слово

        :return: случайное слово
        :rtype: str
        """
        random_key = random.sample(self, 1)
        # Другой способ:
        # random.choice(histogram.keys())
        return random_key[0]

    def check_substring(self, main_str, checked_str, window_size=4):
        """
        Проверка подстроки

        :param main_str: Главная строка
        :type main_str: str
        :param checked_str: Строка, которую надо проверить в главной
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
            tmp_str = main_str
            if tmp_str == checked_str:
                return True
            else:
                return False
        else:
            window_index = 0
            for i in range(window_index, window_size + window_index):
                tmp_str += main_str[i]
            for i in range(len(main_str) - window_size + 1):
                if tmp_str in checked_str:
                    return True
                window_index += 1
                new_tmp_str = ''
                for i in range(window_index, window_size + window_index):
                    if i < len(main_str):
                        new_tmp_str += main_str[i]
                tmp_str = new_tmp_str
            return False

    def return_weighted_random_word(self, added_word=None, priority=None):
        """
        Генерация псевдослучайного числа из диапозона от 0 до n-1, где n - общее число слов

        :param added_word: Добавленное слова
        :type added_word: str
        :param priority: Нужен ли приоритет
        :type priotiry: bool
        :return: Список из числа и его статутса
        :rtype: list
        """
        random_int = random.randint(0, self.tokens-1)
        index = 0
        list_of_keys = list(self.keys())
        acceptable_keys = []
        if added_word:
            if priority:
                for key in list_of_keys:
                    if added_word.lower() == key.lower():
                        acceptable_keys.append(key)
                if acceptable_keys:
                    output = [random.choice(acceptable_keys), 'added_word']
                    return output
            else:
                for key in list_of_keys:
                    if self.check_substring(added_word, key) or added_word.lower() in key.lower():
                        acceptable_keys.append(key)
                if acceptable_keys:
                    output = [random.choice(acceptable_keys), 'added_word']
                    return output
        # вывести 'случайный индекс:', random_int
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            # вывести индекс
            if index > random_int:
                # вывести list_of_keys[i]
                output = [list_of_keys[i], 'random_word']
                return output
