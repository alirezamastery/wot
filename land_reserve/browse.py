import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def save_cookie(driver, path='cookies.json'):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)


url = {
    'login': 'https://eu.wargaming.net/id/signin/',
    'map':   'https://eu.wargaming.net/globalmap/'
}

USERNAME = 'alireza_mastery_farahani@yahoo.com'
PASSWORD = 'Af_331372'
browser = webdriver.Chrome(executable_path='../drivers/chromedriver.exe')
browser.get(url['map'])
delay = 20  # seconds
try:
    myElem = WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/div[12]/div/div[3]/div/div/a')
        )
    )
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

login_link = browser.find_element_by_xpath('/html/body/div[12]/div/div[3]/div/div/a')
browser.execute_script("arguments[0].click();", login_link)

try:
    myElem = WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located(
            (By.ID, 'id_login')
        )
    )
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

username_field = browser.find_element_by_id('id_login')
username_field.send_keys(USERNAME)
password_field = browser.find_element_by_id('id_password')
password_field.send_keys(PASSWORD)
login_btn = browser.find_element_by_xpath(
    '/html/body/div[1]/div/div[3]/div/div/div/div[1]/span/form/div/fieldset[2]/span[1]/button')
login_btn.click()

try:
    myElem = WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located(
            (By.ID, 'common_menu')
        )
    )
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

save_cookie(browser)
