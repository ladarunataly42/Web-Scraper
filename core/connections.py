from werkzeug.security import generate_password_hash, check_password_hash

from core.models.people import People
from core.models.user import Users
from core.mongo_repo import MongoRepository
from web_driver import WebDriver

class UserService:
    def __init__(self):
        self.repo = MongoRepository(collection=Users)

    def login(self, email, password):
        try:
            user = self.repo.find_one(email)
            if check_password_hash(user['password'], password):
                return 200  # OK
            else:
                return 400  # Bad Request
        except Exception as e:
            return 404  # Not Found

    def register(self, email, password):
        try:
            self.repo.insert_one(email, generate_password_hash(password))
        except Exception as e:
            print(e)

    def search(self, email):
        try:
            return self.repo.find_one(email)
        except:
            return False


class PersonScraped:
    def __init__(self):
        self.repo = MongoRepository(collection=People)

    def take_data(self, link):
        scraper = WebDriver()
        scraper()
