import datetime as dt
import requests
from pprint import pprint


APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'
URL_EXTEND = f'https://api.worldoftanks.eu/wot/auth/prolongate/'
URL_RESERVE_ACTIVATION = 'https://api.worldoftanks.eu/wot/stronghold/activateclanreserve/'


class Activator:

    def __init__(self):
        self.access_token = self.load_token()
        self.extend_token()
        print(self.access_token)

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
        pprint(response)
        if response['status'] == 'ok':
            self.access_token = response['access_token']
            self.save_token(self.access_token)

    def run(self):
        current_datetime = dt.datetime.now()
        current_time = current_datetime.time()
        while True:
            command = sef
            if current_time > dt.time(18, 0, 0):
                pass

    def activate_reserve(self, reserve_type, reserve_level):
        payload = {
            'application_id': APPLICATION_ID,
            'access_token':   self.access_token,
            'reserve_level':  reserve_level,
            'reserve_type':   reserve_type,
        }
        res = requests.post(url=URL_RESERVE_ACTIVATION, data=payload)
        response = res.json()
        pprint(response)
    def get_current_status(self):
        current_datetime = dt.datetime.now()
        current_time = current_datetime.time()


if __name__ == '__main__':
    activator = Activator()
