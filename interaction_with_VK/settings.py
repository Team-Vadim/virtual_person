# Данные для входа

LOGIN = "логин"
PASSWORD = "пароль"

# Некоторые параметры API
MAX_COUNT = 100     # Максимальное кол-во записей, которое можно получить по *.wall.get, деленное на 25.
LIMIT = 500
AGE1 = 14
AGE2 = 20
AGE3 = 35
AGE4 = 50
"""
LIMIT - Максимальное кол-во записей, скачиваемое со страницы по *wall.get (выходит 5 запросов по 100 в каждом).
Больше лучше не брать, чтобы не словить бан на кол-во запросов (в будущем изменить на None).
"""

STOP_WORDS = ['блять', 'http', 'сука', "хуй", "ебать", "ебанина", "ебанько", "]", "ебля", "ебаный", "еблан",
              "епта", "ебливый", "блядь", "блядство", "блядина", "мудила", "дрочила", "пидор", "пидорас", "пидорасина",
              "ебучий", "хуеплет", "ебырь", "ебанутый", "пизда", "пиздец", "пиздюк", "пиздопроебина", "пиздуй",
              "распиздяй", "хуйня", "нахуй", "выблядок", "ебучка", "охуел", "Блять", "Http", "Сука", "Хуй", "Ебать",
              "Ебанина", "Ебанько", "[", "Ебля", "Ебаный", "Еблан", "Епта", "Ебливый", "Блядь", "Блядство", "Блядина",
              "Мудила", "Дрочила", "Пидор", "Пидорас", "Пидорасина", "Ебучий", "Хуеплет", "Ебырь", "Ебанутый", "Пизда",
              "Пиздец", "Пиздюк", "Пиздопроебина", "Пиздуй", "Распиздяй", "Хуйня", "Нахуй", "Выблядок", "Ебучка",
              "Охуел"]