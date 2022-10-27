import time
from abc import ABC
import os

import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from exceptions import *
from core.webdriver_base import WebDriverBase


class WebDriver(WebDriverBase):

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        self.start()
        self.get(*args)

    def start(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_argument('user-data-dir={}'.format("path/user/"))
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def get(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[data-cookiebanner="accept_button"]'))).click()  # accept cookie
        self.login()

    def login(self):
        try:
            username = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
            password = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

            username.clear()
            username.send_keys(os.environ['username'])
            password.clear()
            password.send_keys(os.environ['password'])

            button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            print("login successful")
        except Exception as e:
            raise e

