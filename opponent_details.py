import requests
import json

APPLICATION_ID = 'a833e8d1821776e7a529b934963bd019'
CHIEFTAIN_ID = 57937


def get_clan_name(clan_id):
    URL = 'https://api.worldoftanks.eu/wot/globalmap/claninfo/'
    payload = {
        'application_id': APPLICATION_ID,
        'clan_id':        clan_id
    }
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    if data['status'] != 'ok':
        print(data)
    return data['data'][str(clan_id)]


def get_battles():
    URL = 'https://api.worldoftanks.eu/wot/globalmap/clanbattles/'
    payload = {
        'application_id': APPLICATION_ID,
        'clan_id':        500071718
    }
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    battles = list()

    if data['status'] != 'ok':
        print(data)
        return None

    for d in data['data']:
        d['clan_details'] = get_clan_name(d['competitor_id'])
        battles.append(d)

    return battles


def get_player_pr(account_id):
    URL = 'https://api.worldoftanks.eu/wot/account/info/'
    payload = {
        'application_id': APPLICATION_ID,
        'account_id':     account_id
    }
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    if data['status'] != 'ok':
        print(data)
        return None
    return data['data'][str(account_id)]['global_rating']


def get_clan_members(clan_id):
    URL = 'https://api.worldoftanks.eu/wot/clans/info/'
    payload = {
        'application_id': APPLICATION_ID,
        'clan_id':        clan_id
    }
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    if data['status'] != 'ok':
        print(data)
        return None
    return data['data'][str(clan_id)]['members']


def get_player_has_chieftain(account_id):
    URL = 'https://api.worldoftanks.eu/wot/account/info/'
    payload = {
        'application_id': APPLICATION_ID,
        'account_id':     account_id,
        'tank_id':        CHIEFTAIN_ID
    }
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    if data['status'] != 'ok':
        print(data)
        return None
    return bool(len(data['data'][str(account_id)]))


if __name__ == '__main__':
    # with open('clan_battles.json', 'r') as file:
    #     data = json.load(file)
    # for d in data['data']:
    #     d['clan_details'] = get_clan_name(d['competitor_id'])
    #     battles.append(d)
    battles = get_battles()

    print('List of Battles:')
    for i, bat in enumerate(battles):
        print(f'{i + 1:<2}- Province: {bat["province_name"]:<20} | '
              f'Clan: {bat["clan_details"]["tag"]:<6} {bat["clan_details"]["name"]}')

    battle_number = int(input('\nEnter battle number from the list:'))
    if battle_number - 1 not in [i for i in range(len(battles))]:
        battle_number = int(input('dorost vared kon!:'))
    print('fetching data...')

    clan_index = battle_number - 1
    members_pr = {
        '10000': 0,
        '9000':  0,
        '8000':  0,
        '7000':  0,
    }
    chieftains = 0
    members = get_clan_members(battles[clan_index]['competitor_id'])
    for member in members:
        player_id = member['account_id']
        pr = get_player_pr(player_id)
        if pr >= 10000:
            members_pr['10000'] += 1
        elif 9000 <= pr < 10000:
            members_pr['9000'] += 1
        elif 8000 <= pr < 9000:
            members_pr['8000'] += 1
        elif 7000 <= pr < 8000:
            members_pr['7000'] += 1
        if get_player_has_chieftain(player_id):
            chieftains += 1

    print(f'\n{"clan details":*^50}')
    print(f'elo: {battles[clan_index]["clan_details"]["ratings"]["elo_10"]}')
    print(f'total players: {len(members)}')
    for k, v in members_pr.items():
        print(f'{k:<5} players: {v}')
    print(f'Chieftains: {chieftains}')
