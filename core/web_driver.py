import os
import sys
import time
from abc import ABC

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.webdriver_base import WebDriverBase
from core.constants import LINK_FB


class WebDriver(WebDriverBase):

    def __init__(self):
        super().__init__()

    def start(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.connect()

    def connect(self):
        self.driver.get(LINK_FB)
        self.get('button[data-cookiebanner="accept_button"]', 2, click=1)  # accept cookie
        self.login()

    def login(self):
        try:
            username = self.get("input[name='email']", 10)
            password = self.get("input[name='pass']", 10)

            username.clear()
            username.send_keys(os.environ['user'])
            password.clear()
            password.send_keys(os.environ['pass'])

            self.get("button[type='submit']", 2, click=1)
            print("login successful")
        except Exception as e:
            raise e

    def get(self, html_str, sec, click=0):
        if click == 1:
            return WebDriverWait(self.driver, sec).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, html_str))).click()
        elif click == 0:
            return WebDriverWait(self.driver, sec).until(EC.element_to_be_clickable((By.CSS_SELECTOR, html_str)))

    def redirect_link(self, link):
        WebDriverWait(self.driver, 5).until(EC.url_changes(link))
        self.driver.get(link)
        return self.driver.page_source




