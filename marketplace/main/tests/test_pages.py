import os
import socket

import environ
from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from marketplace.settings import BASE_DIR


class MainPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        environ.Env.read_env(os.path.join(BASE_DIR.parent.parent, ".env"))
        env = environ.Env(HOST_URL=(str, "http://teamdiploma.ru"))
        cls.host_url = env("HOST_URL")
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_selenium_start(self):
        self.driver.get(f'{self.host_url}{reverse("main")}')
        self.driver.save_screenshot(filename=f"{BASE_DIR}/main/tests/bip-boooop!.png")
        self.assertEqual(True, True)
