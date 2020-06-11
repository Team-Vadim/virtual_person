import re


def capital(string: str) -> str:
    """
    Возвращает группы, написанные заглавными буквами

    :param string: str - Строка для обработки
    :return: str - Строка, где группы, написанные заглавными буквами
    """
    return(string.group(1).upper() + string.group(2).upper())


def orthography(string: str) -> str:
    """
    Убирает пробелы перед знаками препинания и делает буквы после знаков препинания заглавными

    :param string: str - Строка для обработки
    :return: str - Строка с правильной пунктуацией
    """
    w_o_spaces = string.capitalize()
    signs = [',', '!', ':', ';']
    for sign in signs:
        w_o_spaces = re.sub(' ' + sign, sign, w_o_spaces)
    w_o_spaces = re.sub(' \.', '.', w_o_spaces)
    w_o_spaces = re.sub(' \?', '?', w_o_spaces)
    return(re.sub('(\. |\? |! )(.)', capital, w_o_spaces))

