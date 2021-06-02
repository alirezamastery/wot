import ctypes
import requests
from xlsxwriter import Workbook

from clan_players.assets.utils import get_workbook_formats
from clan_players.assets.statics import LOGO, SELECTED_TANKS


# settings for console so it can show ANSI escape:
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
RESET = '\033[0m'
GREEN = '\033[38;5;40m'

CONNECTION_EXCEPTION_MSG = 'There was an error in connection to the server'
APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'


def get_clan_members():
    clan_details_url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
    clan_details_raw = requests.get(clan_details_url)
    clan_details = clan_details_raw.json()
    if not clan_details['status'] == 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return clan_details['data']['500071718']['members']


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


def flatten_tank_tiers(tank_tiers: dict):
    result = dict()
    for tier in tank_tiers.values():
        for group in tier['groups'].values():
            for tank_id, tank_name in group['tanks'].items():
                result[tank_id] = tank_name
    return result


def filter_player_tanks(tanks: dict):
    filtered_tanks = list()
    for tank in tanks:
        if str(tank['tank_id']) in SELECTED_TANKS_FLAT:
            filtered_tanks.append(tank)
    return filtered_tanks


print(LOGO)

SELECTED_TANKS_FLAT = flatten_tank_tiers(SELECTED_TANKS)

# +-----------------------------------------------------------------------+
# | Get Data from server                                                  |
# +-----------------------------------------------------------------------+
clan_members = get_clan_members()
clan_members_details = dict()

for i, member in enumerate(clan_members):
    account_id = member['account_id']
    account_name = member['account_name']
    if account_name == 'HAJJ_ABBAS':
        print(f' {GREEN}{account_name}{RESET}')
    else:
        print(f' {account_name}')
    account_details = dict()
    account_details['role'] = member['role'].capitalize()
    account_info = get_player_info(account_id)
    account_details['Personal'] = account_info['global_rating']
    account_details['Battles'] = account_info['statistics']['all']['battles']
    tanks = get_player_vehicles(account_id)
    account_details['tanks'] = filter_player_tanks(tanks)
    clan_members_details[account_name] = account_details

clan_members_details = dict(sorted(clan_members_details.items(), key=lambda v: v[0].upper()))

# +-----------------------------------------------------------------------+
# | Excel output                                                          |
# +-----------------------------------------------------------------------+
workbook = Workbook('tanks.xlsx')

formats = get_workbook_formats(workbook)

worksheet = workbook.add_worksheet()

header_general = ['No', 'Account', 'Rank', 'Personal', 'Battles']
tanks_number = list()
for tier, details in SELECTED_TANKS.items():
    groups_length = [len(group['tanks']) for group in details['groups'].values()]
    tanks_number.append(sum(groups_length))
table_end_col = sum(tanks_number) + len(header_general)

worksheet.set_row(0, 35)
worksheet.set_row(1, 45)
worksheet.set_row(2, 35)
worksheet.set_column(0, 0, 5)
worksheet.set_column(1, 2, 20)
worksheet.set_column(len(header_general), table_end_col, 12)
worksheet.freeze_panes(3, 2)

# write header
worksheet.merge_range(0, 0, 1, 4, '', formats['general_header'])
for i, header in enumerate(header_general):
    worksheet.write(2, i, header, formats['general_header'])

start_col = 5
for (tier, details) in SELECTED_TANKS.items():
    # tier name in first row
    groups_length = sum([len(group['tanks']) for group in details['groups'].values()])
    worksheet.merge_range(0, start_col, 0, start_col + groups_length - 1, tier,
                          formats[details['color']])
    # group names in second row
    group_merge_start = start_col
    for name, group in details['groups'].items():
        group_length = len(group['tanks'])
        worksheet.merge_range(1, group_merge_start, 1, group_merge_start + group_length - 1, name,
                              formats[group['color_header']])
        # each tank in third row
        for i, tank in enumerate(group['tanks'].values()):
            worksheet.write(2, group_merge_start + i, tank, formats[group['color_tank']])
        group_merge_start += group_length
    start_col += groups_length

worksheet.merge_range(0, table_end_col, 2, table_end_col, 'Total Tanks', formats['total_tanks'])
worksheet.set_column(table_end_col, table_end_col, 12)

# write rows
row = 3
for i, (name, details) in enumerate(clan_members_details.items(), 1):
    # player stats
    format_selector = 'even' if i % 2 == 0 else 'odd'
    worksheet.write(row, 0, i, formats[f'table_{format_selector}'])
    worksheet.write(row, 1, name, formats[f'name_{format_selector}'])
    worksheet.write(row, 2, details['role'], formats[f'table_{format_selector}'])
    worksheet.write_number(row, 3, details['Personal'], formats[f'number_{format_selector}'])
    worksheet.write_number(row, 4, details['Battles'], formats[f'number_{format_selector}'])
    # player tanks info
    col = 5
    tanks = 0
    for tank_id in SELECTED_TANKS_FLAT.keys():
        if any(str(d['tank_id']) == tank_id for d in details['tanks']):
            index = next((index for (index, d) in enumerate(details['tanks']) if str(d['tank_id']) == tank_id), None)
            worksheet.write_number(row, col, details['tanks'][index]['statistics']['battles'], formats['in_garage'])
            tanks += 1
        else:
            worksheet.write(row, col, '', formats[f'table_{format_selector}'])
        col += 1
    worksheet.write_number(row, col, tanks, formats['total_tanks'])
    row += 1

workbook.close()

input('\nResults saved in "tanks.xlsx". press any key to exit\n')
