import requests
from bs4 import BeautifulSoup


url = 'http://www.wotinfo.net/en/efficiency?server=EU&playername=hajj_abbas'
source = requests.get(url).text
page = BeautifulSoup(source, 'lxml')
# print(page.prettify())
wn8_div = page.find('div', {'class': 'hero-widget well well-sm'})
wn8 = wn8_div.find_all('var')
print(wn8[1].text.strip())
