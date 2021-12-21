from django.urls import reverse
from selenium.webdriver.common.by import By


def login_as_test_user(host_url, driver):
    driver.get(f'{host_url}{reverse("login")}')
    username = driver.find_element(by=By.NAME, value="username")
    username.send_keys("testuser")
    password = driver.find_element(by=By.NAME, value="password")
    password.send_keys("test1pass")
    buttons = driver.find_elements(by=By.TAG_NAME, value="button")
    buttons[-1].click()
