import requests
import xlsxwriter
# import json
from statics import LOGO, TIER_10, TANKS_COLORS_BY_ID, MUST_HAVE


CONNECTION_EXCEPTION_MSG = 'There was an error in connection to the server'
APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'


def get_player_vehicles(account_id):
    player_vehicles_url = f'https://api.worldoftanks.eu/wot/account/tanks/?application_id={APPLICATION_ID}&account_id={account_id}'
    player_vehicles_raw = requests.get(player_vehicles_url)
    player_vehicles = player_vehicles_raw.json()
    if player_vehicles['status'] != 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return player_vehicles['data'][str(account_id)]


def get_player_info(account_id):
    player_info_url = f'https://api.worldoftanks.eu/wot/account/info/?application_id={APPLICATION_ID}&account_id={account_id}'
    player_info_raw = requests.get(player_info_url)
    player_info = player_info_raw.json()
    if player_info['status'] != 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return player_info['data'][str(account_id)]


print(LOGO)

clan_details_url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
clan_details_raw = requests.get(clan_details_url)
clan_details = clan_details_raw.json()

if not clan_details['status'] == 'ok':
    raise RuntimeError(CONNECTION_EXCEPTION_MSG)

clan_members = clan_details['data']['500071718']['members']
clan_members_details = dict()

for member in clan_members:
    account_id = member['account_id']
    account_name = member['account_name']
    print(f' {account_name}')
    account_details = dict()
    account_info = get_player_info(account_id)
    account_details['role'] = member['role'].capitalize()
    account_details['Personal'] = account_info['global_rating']
    account_details['Battles'] = account_info['statistics']['all']['battles']
    account_tanks_10 = list()
    tanks = get_player_vehicles(account_id)
    for tank in tanks:
        if str(tank['tank_id']) in TIER_10:
            account_tanks_10.append(tank)
    account_details['tanks'] = account_tanks_10
    clan_members_details[account_name] = account_details

# print(clan_members_details)
# print(sorted(clan_members_details.items()))
clan_members_details = dict(sorted(clan_members_details.items(), key=lambda v: v[0].upper()))
# print(clan_members_details)

# with open('./players.json', 'w') as f:
#     json.dump(clan_members_details, f)

workbook = xlsxwriter.Workbook('tanks.xlsx')

header_format = workbook.add_format({
    'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
})
general_format = workbook.add_format({
    'border': True, 'align': 'left', 'valign': 'vcenter',
})
name_format = workbook.add_format({
    'border': True, 'align': 'left', 'valign': 'vcenter', 'bold': True
})
number_format = workbook.add_format({
    'border': True, 'align': 'left', 'valign': 'vcenter', 'num_format': '#,###'
})
color_format_FFFFFF = workbook.add_format({
    'bg_color': '#FFFFFF', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
})
color_formats = {
    'color_format_FFFFFF': workbook.add_format({
        'bg_color': '#FFFFFF', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_0594FF': workbook.add_format({
        'bg_color': '#0594FF', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_00B050': workbook.add_format({
        'bg_color': '#00B050', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_954ECA': workbook.add_format({
        'bg_color': '#954ECA', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_FFFF00': workbook.add_format({
        'bg_color': '#FFFF00', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_FFC000': workbook.add_format({
        'bg_color': '#FFC000', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
}
in_garage_format = workbook.add_format({
    'bg_color': '#92D050', 'border': True, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,###'
})
missing_important_format = workbook.add_format({'bg_color': '#FF0000', 'border': True})
not_having_tank_format = workbook.add_format({
    'bg_color': '#FFFFCC', 'border': True, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,###'
})
sum_format = workbook.add_format({
    'bg_color': '#FFFF00', 'border': True, 'align': 'center', 'valign': 'vcenter',
})

worksheet = workbook.add_worksheet()
worksheet.set_row(0, 35)
worksheet.set_column(1, 1, 20)
worksheet.set_column(0, 0, 5)
worksheet.freeze_panes(1, 2)
# write header
col = 0
for i in range(5):
    worksheet.write(0, col, '', color_format_FFFFFF)
    col += 1
for k, value in TIER_10.items():
    color = TANKS_COLORS_BY_ID[k]
    worksheet.write(0, col, value, color_formats[f'color_format_{color[1:]}'])
    col += 1
worksheet.write(0, col, 'Total Tanks', sum_format)

# write rows
row = 1
for i, (name, details) in enumerate(clan_members_details.items(), 1):
    worksheet.write(row, 0, i, general_format)
    worksheet.write(row, 1, name, name_format)
    worksheet.write(row, 2, details['role'], general_format)
    worksheet.write_number(row, 3, details['Personal'], number_format)
    worksheet.write_number(row, 4, details['Battles'], number_format)
    col = 5
    tanks = 0
    for tank_id in TIER_10.keys():
        if any(str(d['tank_id']) == tank_id for d in details['tanks']):
            index = next((index for (index, d) in enumerate(details['tanks']) if str(d['tank_id']) == tank_id), None)
            worksheet.write_number(row, col, details['tanks'][index]['statistics']['battles'], in_garage_format)
            tanks += 1
        else:
            if tank_id in MUST_HAVE:
                worksheet.write(row, col, '', missing_important_format)
            else:
                worksheet.write(row, col, '', not_having_tank_format)
        col += 1
    worksheet.write_number(row, col, tanks, sum_format)
    row += 1

workbook.close()

input('\nResults saved in "tanks.xlsx". press any key to exit\n')


