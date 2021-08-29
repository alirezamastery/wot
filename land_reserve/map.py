import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def load_cookie(driver, path='cookies.json'):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)


url = {
    'login': 'https://eu.wargaming.net/id/signin/',
    'map':   'https://eu.wargaming.net/globalmap/'
}


browser = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
browser.get(url['map'])
load_cookie(browser)
