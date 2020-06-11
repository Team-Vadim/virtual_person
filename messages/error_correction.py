# -*- coding: utf-8 -*-
import requests
import re
import json

API_URL_BASE = "https://speller.yandex.net/services/spellservice.json/checkText"


def capital(string: str) -> str:
    """
    Возвращает группы, написанные заглавными буквами

    :param string: Строка для обработки
    :type string: str
    :return: Строка, где группы, написанные заглавными буквами
    :rtype: str
    """
    return (string.group(1).upper() + string.group(2).upper())


def orthography(string: str) -> str:
    """
    Убирает пробелы перед знаками препинания и делает буквы после знаков препинания заглавными

    :param string: Строка для обработки
    :type string: str
    :return: Строка с правильной пунктуацией
    :rtype: str
    """
    w_o_spaces = string.capitalize()
    signs = [',', '!', ':', ';']
    for sign in signs:
        w_o_spaces = re.sub(' ' + sign, sign, w_o_spaces)
    w_o_spaces = re.sub(' \.', '.', w_o_spaces)
    w_o_spaces = re.sub(' \?', '?', w_o_spaces)
    return (re.sub('(\. |\? |! )(.)', capital, w_o_spaces))


def correct_spelling(text, options=518):
    """
    Текст с ошибками (без ошибок)
    Подробное апи можно найти тут: https://yandex.ru/dev/speller/doc/dg/concepts/About-docpage/

    :param text: Входной текст
    :type text: str
    :param options: настройки для спеллера
        в переменную записывается сумма нужных значений:
        IGNORE_DIGITS	        2	Пропускать слова с цифрами, например, "авп17х4534".
        IGNORE_URLS	            4	Пропускать интернет-адреса, почтовые адреса и имена файлов.
        FIND_REPEAT_WORDS	    8	Подсвечивать повторы слов, идущие подряд. Например, "я полетел на на Кипр".
        IGNORE_CAPITALIZATION	512 Игнорировать неверное употребление ПРОПИСНЫХ/строчных букв, например, в слове "москва"
    :type options: int
    :return: Исправленный текст
    :rtype: str
    """
    lang = "ru"
    data = {"text": text, "lang": lang, "options": options}
    postfixes_dash = ["то ", "либо ", "нибудь ", "таки", "то.", "либо.", "нибудь.", "таки.", "то,", "либо,", "нибудь,",
                      "то?", "либо?", "нибудь?", "то!", "либо!", "нибудь!", "то:", "либо:", "нибудь:",
                      "то;", "либо;", "нибудь;", "то\"", "либо\"", "нибудь\"", "то/", "либо/", "нибудь/"
                                                                                               "то'", "либо'",
                      "нибудь'"]
    prefix_dash = ["Кое"]
    try:
        response = requests.post(API_URL_BASE, data)  # пост-запрос
        result = response.json()
        for arr in result:
            text = text.replace(arr["word"], arr["s"][0])  # замены исправлений в тексте
        for word in postfixes_dash:
            text = text.replace(" " + word, "-" + word)  # исправление проблем с дефисами
        for word in prefix_dash:
            text = text.replace(word + " ", word + '-')
    except:
        pass
    text = orthography(text)
    return text
