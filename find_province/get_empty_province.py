import datetime
import requests

MAP_IDs = ['04_himmelsdorf', '36_fishing_bay']
URL = 'https://api.worldoftanks.eu/wot/globalmap/provinces/'

request_payload = {
    'application_id': 'a833e8d1821776e7a529b934963bd019',
    'front_id':       'renaissance_eu_league1',
    'arena_id':       None,  # assign value to this
    'landing_type':   'tournament',

}


def get_province(payload):
    raw = requests.post(url=URL, data=payload)
    data = raw.json()
    provinces = {
        '21:30': list(),
        '21:45': list(),
        '22:30': list(),
        '22:45': list(),
        '23:30': list(),
        '23:45': list(),
        '00:30': list(),
        '00:45': list(),
    }

    if data['status'] == 'ok':
        for d in data['data']:
            if len(d['competitors']) < 32:
                province = dict()
                province['province_name'] = d['province_name']
                utc_dt = datetime.datetime.strptime(d['battles_start_at'], '%Y-%m-%dT%H:%M:%S')
                date = utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
                time = date.strftime('%H:%M')
                province['time'] = time
                provinces[time].append(province)
    else:
        print(data)

    return provinces


if __name__ == '__main__':
    for map_id in MAP_IDs:
        print(f'{map_id:-^50}')
        request_payload['arena_id'] = map_id
        available_provinces = get_province(request_payload)
        for time, provinces in available_provinces.items():
            print(f' {time}')
            for province in provinces:
                print(f'   {province["province_name"]}')
            print('-' * 50)
