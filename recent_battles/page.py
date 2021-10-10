import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

from constants import *


class PageParser:

    def __init__(self, url):
        self.url = url
        response = requests.get(self.url, timeout=5)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        tab_container = self.soup.find('div', class_='tab-container')
        data = []
        for i, tab in enumerate(tab_container):
            if i in [0, 1, 2, 6, 7]:
                tds = tab.findAll('td', attrs={'class': 'text-right'})
                data.append(tds[2].text)
