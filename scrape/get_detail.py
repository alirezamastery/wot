import json
from assets.browser import Browser
from assets.api_call import get_clan_name, show_battles, get_battles


def print_pretty(data):
    print(f'{"result":-^50}')
    print(f'player count: {data["count"]}')
    print('Personal Ratings:')
    for k, v in data['personal_rating'].items():
        print('\t' + f'{k:<5}: {v}')
    print(f'chieftains: {data["chieftains"]}')
    print('-' * 50)


LOOP = False

if __name__ == '__main__':
    browser = Browser(headless=False, active_only=True)
    while True:

        battles = list()

        with open('clan_battles.json', 'r') as file:
            data = json.load(file)
        for d in data['data']:
            d['clan_details'] = get_clan_name(d['competitor_id'])
            battles.append(d)
        # battles = get_battles()

        clan_index = show_battles(battles)
        clan_id = battles[clan_index]['competitor_id']
        players_data = browser.fetch(clan_id)
        filtered_data = browser.filter_data()
        print_pretty(filtered_data)

        if not LOOP:  # the second time the page is loaded json file con not be found so we can't loop!
            break

        while True:
            command = input('Run again?(y/n):')
            if command in ('y', 'n'):
                break
        if command == 'n':
            break

    browser.driver.close()
