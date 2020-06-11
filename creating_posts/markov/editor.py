import os


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяQWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'
special_symbols = '.,-:;()!?"*'
end_symbols = '.!?'


def parse_text(dir_path):
    """
    Обработка текстовых файлов

    :param dir_path: Путь до директории с тектсами
    :type dir_path: str
    :return: текст
    :rtype: str
    """
    texts = os.listdir(dir_path)

    text = list()
    for item in texts:
        with open(dir_path + '/' + item, 'r', encoding='utf-8') as file:
            text += file.read().split()

    text_edited = []

    flag_symbol = True
    for word in text:
        word_edited = []
        if word in special_symbols and flag_symbol is False:
            flag_symbol = False
        else:
            flag_symbol = True
        for symbol in word:
            if symbol in alphabet:
                word_edited.append(symbol)
            elif symbol in special_symbols and flag_symbol:
                if len(word_edited) <= 30:
                    text_edited.append(''.join(word_edited))
                text_edited.append(symbol)
                if symbol in end_symbols:
                    text_edited.append('end\n')
                word_edited.clear()
                flag_symbol = False
        if len(word_edited) <= 30:
            text_edited.append(''.join(word_edited))
    return ' '.join(text_edited)
