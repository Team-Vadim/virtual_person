import pymongo
from ast import literal_eval as make_tuple


class DbModelInteraction:
    def __init__(self, database_name):
        """
        Подключение к базе данных

        :param database_name: название БД на сервере
	:type database_name: str
        """
        self.last_id = -1
        if type(database_name) == str:
            client = pymongo.MongoClient("mongodb://virtualperson:genious@virtual-person.ru:27017/?authSource=admin"
                                         "&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false")
            self.db = client[database_name]
        else:
            self.db = database_name

    def insert_data(self, model):
        """
        Запись модели в базу данных

        :param model:  модель для записи
        :type model: dict
        """
        self.last_id += 1
        self.db['messages_model'].insert_one({
            "id": self.last_id,
            'model': {'temporary': 1}})
        for item in model:
            key = str(item).replace('.', '-dotkey-')
            key = key.replace('$', '-dollarkey-')
            self.db['messages_model'].update({"id": self.last_id},
                                 {"$set": {"model." + key: model[item]}})

    def extract_data(self):
        """
        Чтение модели из базы данных. Работает с последней записанной моделью

        :return: последняя записанная в БД модель
        :rtype: dict
        """
        model = self.db['messages_model'].find_one({'id': self.last_id})['model']
        print(model)
        model_final = {}
        del model["temporary"]
        for item in model:
            item_copy = item.replace('-dotkey-', '.')
            item_copy = item.replace('-dollarkey-', '$')
            item_tuple = make_tuple(item_copy)
            model_final[item_tuple] = model[item]
        return model_final


database = DbModelInteraction('messages_database')
