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