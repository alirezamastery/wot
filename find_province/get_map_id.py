import requests

URL = 'https://api.worldoftanks.eu/wot/globalmap/provinces/'

request_payload = {
    'application_id': 'a833e8d1821776e7a529b934963bd019',
    'front_id':       'renaissance_eu_league1',
    'arena_id':       None,
    'landing_type':   'tournament',

}


def get_province():
    raw = requests.post(url=URL, data=request_payload)
    data = raw.json()
    maps = set()

    if data['status'] == 'ok':
        for d in data['data']:
            if len(d['competitors']) < 32:
                province = dict()
                province['arena_name'] = d['arena_name']
                province['arena_id'] = d['arena_id']
                maps.add((province['arena_name'], d['arena_id']))
    else:
        print(data)

    return maps


if __name__ == '__main__':
    maps = get_province()
    for m in maps:
        print(m)
