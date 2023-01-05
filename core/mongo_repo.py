import os
import urllib.parse

from mongoengine import connect

db_orm = None


class MongoRepository:
    __db_orm = None

    def __init__(self, **kwargs):
        self.__connect()
        self.collection = kwargs['collection']

    def __connect(self):
        global db_orm
        db_orm = connect(
            host=f'''mongodb+srv://{os.environ['USER_DB']}:{os.environ['PASS_DB']}@{os.environ['CLUSTER']}/{os.environ['DATABASES']}?retryWrites=true&w=majority''')
        MongoRepository.__db_orm = db_orm

    def set_collection(self, collection):
        self.collection = collection

    def insert_one(self, email, password):
        try:
            user = self.collection(email=email)
            user.password = password
            user.save()
        except Exception as e:
            raise e

    def find_one(self, email):
        try:
            return self.collection.objects.get(email=email)
        except Exception as e:
            raise e

    def find_people(self, name):
        try:
            dict_data = {}
            data = self.collection.objects.get(name=name).__dict__
            for item in data.items():
                if item[0] not in ['_cls', '_dynamic_lock', '_fields_ordered']:
                    dict_data.update({item[0]: item[1]})
            return dict_data
        except Exception as e:
            raise e

    def find_url(self, url):
        try:
            var = self.collection.objects.get(url_fb=url).__dict__
            return True
        except Exception as e:
            return False

    def insert_people(self, person):
        try:
            obj = self.collection()
            for key in person.keys():
                setattr(obj, key, person[key])
            self.collection.objects.insert(obj)
        except Exception as e:
            print(e)
