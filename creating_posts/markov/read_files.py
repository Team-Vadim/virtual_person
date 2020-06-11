import editor


def read_files(dir_path):
    """
    Чтение текстовых файлов

    :param dir_path: str -  путь к директории с файлами
    :return: str
    """

    if type(dir_path) is str:
        text = editor.parse_text(dir_path)
    else:
        raise TypeError
    return text
