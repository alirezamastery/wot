import json

# tier_10 = dict()
# with open('./vehicles.json', encoding='utf-8') as file:
#     data = json.load(file)
#     for k, value in data['data'].items():
#         if value['tier'] == 10:
#             tier_10[k] = value['name']

# for k, v in tier_10.items():
#     print(k, v)

# with open('./tier_10.json', 'w') as f:
#     json.dump(tier_10, f)

# with open('./tier_10.json', encoding='utf-8') as f:
#     tier_10 = json.load(f)
#     print(tier_10)

# with open('./players.json', encoding='utf-8') as f:
#     tier_10 = json.load(f)
#     print(tier_10)
#     tier_10 = sorted(tier_10, key=lambda v: v.upper())
#     print(tier_10)

from clan_players.assets.statics import TIER_10_LONGNAME


tier_10 = dict()
with open('jsons/vehicles.json', encoding='utf-8') as file_vehicles:
    vehicles = json.load(file_vehicles)
    for k, v in TIER_10_LONGNAME.items():
        tier_10[k] = vehicles['data'][k]['short_name']
    for k, v in tier_10.items():
        print(f"'{k}' : '{v}',")
