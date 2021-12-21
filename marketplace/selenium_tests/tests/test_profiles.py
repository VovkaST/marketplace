import os
import time
from unittest import TestCase

import environ
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_tests.utils import login_as_test_user

from marketplace.settings import BASE_DIR


class ProfilesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        environ.Env.read_env(os.path.join(BASE_DIR.parent.parent, ".env"))
        env = environ.Env(HOST_URL=(str, "http://teamdiploma.ru"))
        cls.host_url = env("HOST_URL")
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_profile_update(self):
        login_as_test_user(self.host_url, self.driver)
        self.driver.get(f'{self.host_url}{reverse("profile")}')
        patronymic = self.driver.find_element(by=By.NAME, value="patronymic")
        old_patronymic = patronymic.get_attribute("value")
        patronymic.send_keys(str(time.time()))
        buttons = self.driver.find_elements(by=By.TAG_NAME, value="button")
        buttons[-1].click()
        new_patronymic = self.driver.find_element(by=By.NAME, value="patronymic")
        self.assertNotEqual(old_patronymic, new_patronymic.get_attribute("value"))
