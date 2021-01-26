from time import sleep
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions

from .api_call import get_player_has_chieftain


class Browser:
    CHROME_DRIVER = 'E:/Python/wot/development/driver/chromedriver.exe'

    def __init__(self, headless=True, active_only=True):
        self.headless = headless
        self.active_only = active_only
        self.URL = ''

        chrome_options = ChromeOptions()
        chrome_options.headless = headless
        # make chrome log requests
        capabilities = DesiredCapabilities.CHROME

        # capabilities['loggingPrefs'] = {'performance': 'ALL'}  # chromedriver < ~75
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}  # chromedriver 75+

        self.driver = webdriver.Chrome(desired_capabilities=capabilities,
                                       executable_path=self.CHROME_DRIVER,
                                       options=chrome_options)
        self.players_data = None

    def get_url(self, clan_id):
        if self.active_only:
            return f'https://eu.wargaming.net/clans/wot/{clan_id}/players/' \
                   f'#players&offset=0&limit=25&order=-personal_rating&timeframe=7&battle_type=global_map'
        else:
            return f'https://eu.wargaming.net/clans/wot/{clan_id}/players/' \
                   f'#players&offset=0&limit=25&order=-personal_rating&timeframe=all&battle_type=random'

    def fetch(self, clan_id):
        print('fetching data...')
        # fetch the page site which does xhr requests
        url = self.get_url(clan_id)
        self.driver.get(url)
        sleep(1)  # wait for the requests to take place

        # legal = self.driver.find_element_by_xpath('//a[@class="legal-notice_close js-legal-notice-close"]')
        # legal.click()

        # extract requests from logs
        logs_raw = self.driver.get_log('performance')
        logs = [json.loads(lr['message'])['message'] for lr in logs_raw]

        self.players_data = None
        # extract the json file that contains the players data and read its content:
        for log in logs:
            if log['method'] == 'Network.responseReceived' and \
                    'json' in log['params']['response']['mimeType'] and \
                    log['params']['type'] == 'XHR':
                # print(log['params']['response']['url'])
                request_id = log['params']['requestId']
                data_as_str = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                data = json.loads(data_as_str['body'])
                self.players_data = data['items']
                break
        if self.players_data is None:
            raise RuntimeError('could not fetch players data')

        return self.players_data

    def filter_data(self):
        if self.players_data is None:
            raise RuntimeError('fetch players data first')
        result = dict()
        result['count'] = 0
        result['personal_rating'] = {'12000': 0,
                                     '11000': 0,
                                     '10000': 0,
                                     '9000':  0,
                                     '8000':  0,
                                     '7000':  0,
                                     'other': 0
                                     }
        result['chieftains'] = 0
        for i, player in enumerate(self.players_data):
            if player['battles_count'] == 0:
                continue
            print(f'{i + 1:>2}- {player["role"]["localized_name"]:<22}{player["name"]}')
            result['count'] += 1
            pr = player['personal_rating']
            if pr > 12000:
                result['personal_rating']['12000'] += 1
            if 11000 <= pr < 12000:
                result['personal_rating']['11000'] += 1
            elif 10000 <= pr < 11000:
                result['personal_rating']['10000'] += 1
            elif 9000 <= pr < 10000:
                result['personal_rating']['9000'] += 1
            elif 8000 <= pr < 9000:
                result['personal_rating']['8000'] += 1
            elif 7000 <= pr < 8000:
                result['personal_rating']['7000'] += 1
            elif pr < 7000:
                result['personal_rating']['other'] += 1

            if get_player_has_chieftain(player['id']):
                result['chieftains'] += 1

            # attempt to get player details from the page itself:
            # player_row = self.driver.find_element_by_xpath(f"//div[@data-account_id={player['id']}]")
            # player_row.click()
            # sleep(0.1)
            # logs_raw = self.driver.get_log('performance')
            # logs = [json.loads(lr['message'])['message'] for lr in logs_raw]
            # request_id = None
            # for log in logs:
            #     # for k, v in log['params'].items():
            #     #     print(f'{k:<20} | {v}')
            #     # print('-' * 200)
            #     try:
            #         if log['params']['request']['url'] == \
            #                 f'https://eu.wargaming.net/clans/wot/vehicles/account/{player["id"]}/' \
            #                 f'?offset=0&limit=7&order=&battle_type=default':
            #             request_id = log['params']['requestId']
            #             break
            #     except:
            #         continue
            # print(request_id)
            # data_as_str = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            # print(data_as_str)
            # data = json.loads(data_as_str['body'])
            # print(data)

        return result


