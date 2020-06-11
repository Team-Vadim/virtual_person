!Версия на google colab -- https://colab.research.google.com/drive/18GrzjnGqd09l61lF0LtbIjCnveam-OL_ !

в файле sentiment_recognition.py находится класс, который определяет эмоциональный окрас предложения 
(с точностью до таких категорий:
        1) positive
        2) negative
        3) neutral
        4) speech
        5) skip - невозможно определить окрас из-за отсутствия контекста). Реализовано с помощью библиотеки deeppavlov
в файле sentences.py находится класс messages, который обрабатывет предложение(я). 
Результат работы - эмоциональный окрас всего сообщения + массив (массивы) со списком смежностей предложений
        В каждом массиве есть тип предложения (повест/ воскл/ вопр) +  массивы, соответствующие словам
        В массивах по словам лежат --
            -> словарь, где лежит само слово
                -> 'word' -- слово
                -> 'role' -- роль в предложении
                    -> nsubj -- подлежащее
            -> зависимые слова, если есть
Из-за того, что пока неясно, как именно это будет встроено в дальнейший проект, пока что нужно вручную ввести предложение, которое будет обработано
!! запускать нужно только sentences.py !!
установить dependency-decoding (если есть такая ошибка) pip install git+https://github.com/andersjo/dependency_decoding


как работать с базой данных:
1) Установка (версия для windows)
    <<https://stackoverflow.com/questions/20796714/how-do-i-start-mongo-db-from-windows>>
    1. скачать ПО отсюда -> https://www.mongodb.com/download-center/community
    2. зайти в папку, куда mongodb установилоась (по умолчанию C:\Program Files\MongoDB\Server\<version>\bin>)
    3. в cmd  из этой папки запустить "mongod"
2) В файле markov_sentence_generation импортируем из database_interaction database
3) Записать модель model в БД - database.insert_data(model)
4) Извлечь модель из БД - database.extract_data()

Про скрипты генерации ответов:
1) Их 8 штук, они лежат в messages\gen_scripts
2) Они уже подключены к нужным файлам для обучения
3) Номера портов: от 10000 до 10007 соответственно в том порядке, в котором они лежат в папке