import os

from werkzeug.security import generate_password_hash, check_password_hash

from core.beautiful_soup import BeautifulSoupScrape
from core.models.people import People
from core.models.user import Users
from core.mongo_repo import MongoRepository
from core.web_driver import WebDriver
from facebook_scraper import get_posts


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
        self.page_sources = {}

    def take_data(self, link_fb):
        scraper = WebDriver()
        scraper.start()
        link_fb = link_fb[:-1] if link_fb[-1] == "/" else link_fb

        links = ['/about_places', '/about_work_and_education', '/about_contact_and_basic_info',
                 '/about_family_and_relationships', '/about_details', '/about_life_events']

        for link in links:
            source = scraper.redirect_link(link_fb + link)
            self.page_sources[link[1:]] = source

        beautiful_soup = BeautifulSoupScrape(self.page_sources, link_fb)
        person_detail = beautiful_soup.about()
        self.repo.insert_people(person_detail)

    def search_data(self, name):
        try:
            return self.repo.find_people(name)
        except:
            return False

    def find_url(self, url):
        return self.repo.find_url(url)
