from time import sleep
import json
import ast
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions

chrome_driver = 'E:/Python/wot/development/driver/chromedriver.exe'

URL = 'https://eu.wargaming.net/clans/wot/500071718/players/#players&offset=0&limit=25&order=-personal_rating&timeframe=7&battle_type=global_map'

chrome_options = ChromeOptions()
chrome_options.headless = False
# make chrome log requests
capabilities = DesiredCapabilities.CHROME

# capabilities['loggingPrefs'] = {'performance': 'ALL'}  # chromedriver < ~75
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}  # chromedriver 75+

driver = webdriver.Chrome(desired_capabilities=capabilities,
                          executable_path=chrome_driver,
                          options=chrome_options)

# fetch a site that does xhr requests
driver.get(URL)
sleep(1)  # wait for the requests to take place

# extract requests from logs
logs_raw = driver.get_log('performance')
logs = [json.loads(lr['message'])['message'] for lr in logs_raw]


def log_filter(log_):
    return (log_['method'] == 'Network.responseReceived'  # is an actual response
            and 'json' in log_['params']['response']['mimeType']  # and json
            and log_['params']['type'] == 'XHR'
            )


if __name__ == '__main__':
    for log in filter(log_filter, logs):
        request_id = log['params']['requestId']
        resp_url = log['params']['response']['url']
        print(f'Caught {resp_url}')
        print(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id}))

    players_data = None
    for log in logs:
        if log['method'] == 'Network.responseReceived' and \
                'json' in log['params']['response']['mimeType'] and \
                log['params']['type'] == 'XHR':
            
            request_id = log['params']['requestId']
            data_as_str = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            data = json.loads(data_as_str['body'])
            players_data = data['items']
            break

    for p in players_data:
        print(p)
