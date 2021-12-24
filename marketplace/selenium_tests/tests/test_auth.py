import os
import time

import environ
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By

from marketplace.settings import env


class AuthTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host_url = env("HOST_URL")
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get(f'{self.host_url}{reverse("login")}')
        self.assertTrue(self.driver.find_element(by=By.NAME, value="login"))
        username = self.driver.find_element(by=By.NAME, value="username")
        username.send_keys("testuser")
        password = self.driver.find_element(by=By.NAME, value="password")
        password.send_keys("test1pass")
        buttons = self.driver.find_elements(by=By.TAG_NAME, value="button")
        buttons[-1].click()
        self.assertTrue(self.driver.find_element(by=By.NAME, value="account"))

    def test_register(self):
        logout_link = self.driver.find_element(by=By.NAME, value="logout")
        if logout_link:
            logout_link.click()
        self.driver.get(f'{self.host_url}{reverse("registration")}')
        username = self.driver.find_element(by=By.NAME, value="username")
        username.send_keys(str(time.time()))
        first_name = self.driver.find_element(by=By.NAME, value="first_name")
        first_name.send_keys("test-first-name")
        last_name = self.driver.find_element(by=By.NAME, value="last_name")
        last_name.send_keys("test-last-name")
        password = self.driver.find_element(by=By.NAME, value="password1")
        password.send_keys("test1pass")
        password_confirm = self.driver.find_element(by=By.NAME, value="password2")
        password_confirm.send_keys("test1pass")
        mail = self.driver.find_element(by=By.NAME, value="mail")
        mail.send_keys("test@test.test")
        phone = self.driver.find_element(by=By.NAME, value="phone_number")
        phone.send_keys("89888980008")
        buttons = self.driver.find_elements(by=By.TAG_NAME, value="button")
        buttons[-1].click()
        logout_link = self.driver.find_element(by=By.NAME, value="logout")
        self.assertTrue(logout_link)
