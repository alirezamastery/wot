import requests


CONNECTION_EXCEPTION_MSG = 'There was an error in connection to the server'
APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'


def get_clan_member_ids():
    url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
    response = requests.get(url).json()
    if not response['status'] == 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return response['data']['500071718']['members']


def get_player_vehicles(account_id):
    url = f'https://api.worldoftanks.eu/wot/account/tanks/?application_id={APPLICATION_ID}&account_id={account_id}'
    response = requests.get(url).json()
    if response['status'] != 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return response['data'][str(account_id)]


def get_player_stats(account_id):
    url = f'https://api.worldoftanks.eu/wot/account/info/?application_id={APPLICATION_ID}&account_id={account_id}'
    response = requests.get(url).json()
    if response['status'] != 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return response['data'][str(account_id)]


def flatten_tank_tiers(tank_tiers: dict):
    result = dict()
    for tier in tank_tiers.values():
        for group in tier['groups'].values():
            for tank_id, tank_name in group['tanks'].items():
                result[tank_id] = tank_name
    return result


def filter_player_tanks(player_tanks: dict, required_tanks: dict):
    filtered_tanks = list()
    for tank in player_tanks:
        if str(tank['tank_id']) in required_tanks:
            filtered_tanks.append(tank)
    return filtered_tanks
