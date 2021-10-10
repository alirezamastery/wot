import datetime as dt
import requests
from pprint import pprint
from utils.logging import plogger,logger

# APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'
APPLICATION_ID = 'a833e8d1821776e7a529b934963bd019'
URL_EXTEND = f'https://api.worldoftanks.eu/wot/auth/prolongate/'
URL_RESERVE_ACTIVATION = 'https://api.worldoftanks.eu/wot/stronghold/activateclanreserve/'
COMMAND_MAP = {
    'credit': 'func',
    'xp':     'func',
}


class Activator:

    def __init__(self):
        self.access_token = self.load_token()
        logger(self.access_token)
        self.extend_token()
        logger(self.access_token)

    @staticmethod
    def load_token():
        with open('token.txt', 'r') as f:
            return f.read()

    @staticmethod
    def save_token(new_token):
        with open('token.txt', 'w') as f:
            f.write(new_token)

    def extend_token(self):
        payload = {
            'application_id': APPLICATION_ID,
            'access_token':   self.access_token
        }
        res = requests.post(url=URL_EXTEND, data=payload)
        response = res.json()
        plogger(response)
        if response['status'] == 'ok':
            self.access_token = response['data']['access_token']
            self.save_token(self.access_token)

    def run(self):
        self.activate_reserve('ADDITIONAL_BRIEFING', 10)
        # current_datetime = dt.datetime.now()
        # current_time = current_datetime.time()
        # while True:
        #     command = self.get_current_status()
        #     if current_time > dt.time(18, 0, 0):
        #         pass

    def activate_reserve(self, reserve_type, reserve_level):
        payload = {
            'application_id': APPLICATION_ID,
            'access_token':   self.access_token,
            'reserve_level':  reserve_level,
            'reserve_type':   reserve_type,
        }
        res = requests.post(url=URL_RESERVE_ACTIVATION, data=payload)
        response = res.json()
        plogger(response)

    def get_current_status(self):
        current_datetime = dt.datetime.now()
        current_time = current_datetime.time()
        hour_18 = dt.time(18, 0)
        hour_20 = dt.time(20, 0)
        hour_22 = dt.time(22, 0)
        hour_24 = dt.time(23, 59)
        current_datetime.timestamp()
        if hour_18 <= current_time < hour_20:
            return 'credit'
        elif hour_20 <= current_time < hour_22:
            return 'xp'


if __name__ == '__main__':
    activator = Activator()
    activator.run()
