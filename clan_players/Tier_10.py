import requests
import xlsxwriter

from statics import LOGO, TIER_10, MUST_HAVE, SELECTED_TANKS


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

SELECTED_TANKS_FLAT = dict()
for tier in SELECTED_TANKS.values():
    for group in tier['groups'].values():
        for tank_id, tank_name in group['tanks'].items():
            SELECTED_TANKS_FLAT[tank_id] = tank_name

clan_details_url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
clan_details_raw = requests.get(clan_details_url)
clan_details = clan_details_raw.json()

if not clan_details['status'] == 'ok':
    raise RuntimeError(CONNECTION_EXCEPTION_MSG)

clan_members = clan_details['data']['500071718']['members']
clan_members_details = dict()

for i, member in enumerate(clan_members):
    if i > 5:
        break
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
        if str(tank['tank_id']) in SELECTED_TANKS_FLAT:
            account_tanks_10.append(tank)
    account_details['tanks'] = account_tanks_10
    clan_members_details[account_name] = account_details

clan_members_details = dict(sorted(clan_members_details.items(), key=lambda v: v[0].upper()))

# +-----------------------------------------------------------------------+
# | Excel output                                                          |
# +-----------------------------------------------------------------------+
workbook = xlsxwriter.Workbook('tanks.xlsx')

ODD_COLOR = '#FABF8F'
general_header_format = workbook.add_format({
    'bg_color':  '#DA9694',
    'border':    True,
    'align':     'center',
    'valign':    'vcenter',
    'font_size': '12',
    'text_wrap': True,
    'bold':      True
})
general_format = workbook.add_format({
    'border': True, 'align': 'left', 'valign': 'vcenter',
})
table_formats = {
    'name_format_even':   workbook.add_format({
        'border': True, 'align': 'left', 'valign': 'vcenter', 'bold': True
    }),
    'name_format_odd':    workbook.add_format({
        'border': True, 'align': 'left', 'valign': 'vcenter', 'bold': True, 'bg_color': ODD_COLOR
    }),
    'number_format_even': workbook.add_format({
        'border': True, 'align': 'left', 'valign': 'vcenter', 'num_format': '#,###'
    }),
    'number_format_odd':  workbook.add_format({
        'border': True, 'align': 'left', 'valign': 'vcenter', 'num_format': '#,###', 'bg_color': ODD_COLOR
    }),
    'table_format_even':  workbook.add_format({
        'bg_color': '#FFFFFF', 'border': True, 'align': 'left', 'valign': 'vcenter'
    }),
    'table_format_odd':   workbook.add_format({
        'bg_color': '#FABF8F', 'border': True, 'align': 'left', 'valign': 'vcenter'
    }),
}

color_formats = {
    '#FFFFFF': workbook.add_format({
        'bg_color':  '#FFFFFF', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '11',
        'text_wrap': True, 'bold': True
    }),
    '#0594FF': workbook.add_format({
        'bg_color':  '#0594FF', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '9',
        'text_wrap': True, 'bold': True
    }),
    '#00B050': workbook.add_format({
        'bg_color':  '#00B050', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '9',
        'text_wrap': True, 'bold': True
    }),
    '#954ECA': workbook.add_format({
        'bg_color':  '#954ECA', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '9',
        'text_wrap': True, 'bold': True
    }),
    '#FFFF00': workbook.add_format({
        'bg_color':  '#FFFF00', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16',
        'text_wrap': True, 'bold': True
    }),
    '#B1A0C7': workbook.add_format({
        'bg_color':  '#B1A0C7', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16',
        'text_wrap': True, 'bold': True
    }),
    '#8DB4E2': workbook.add_format({
        'bg_color':  '#8DB4E2', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16',
        'text_wrap': True, 'bold': True
    }),
    '#C4D79B': workbook.add_format({
        'bg_color':  '#C4D79B', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16',
        'text_wrap': True, 'bold': True
    }),
    '#FFC000': workbook.add_format({
        'bg_color':  '#FFC000', 'border': True, 'align': 'center', 'valign': 'vcenter', 'font_size': '16',
        'text_wrap': True, 'bold': True
    }),
}

in_garage_format = workbook.add_format({
    'bg_color': '#92D050', 'border': True, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,###'
})
missing_important_format = workbook.add_format({'bg_color': '#FF0000', 'border': True})
sum_format = workbook.add_format({
    'bg_color': '#FFFF00', 'border': True, 'align': 'center', 'valign': 'vcenter',
})

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
worksheet.merge_range(0, 0, 1, 4, '', general_header_format)
for i, header in enumerate(header_general):
    worksheet.write(2, i, header, general_header_format)

start_col = 5
for (tier, details) in SELECTED_TANKS.items():
    # tier name in first row
    groups_length = sum([len(group['tanks']) for group in details['groups'].values()])
    worksheet.merge_range(0, start_col, 0, start_col + groups_length - 1, tier,
                          color_formats[details['color']])
    # group names in second row
    group_merge_start = start_col
    for name, group in details['groups'].items():
        group_length = len(group['tanks'])
        worksheet.merge_range(1, group_merge_start, 1, group_merge_start + group_length - 1, name,
                              color_formats[group['color_header']])
        # each tank in third row
        for i, tank in enumerate(group['tanks'].values()):
            worksheet.write(2, group_merge_start + i, tank, color_formats[group['color_tank']])
        group_merge_start += group_length
    start_col += groups_length

worksheet.merge_range(0, table_end_col, 2, table_end_col, 'Total Tanks', sum_format)
worksheet.set_column(table_end_col, table_end_col, 12)

# write rows
row = 3
for i, (name, details) in enumerate(clan_members_details.items(), 1):
    format_selector = 'even' if i % 2 == 0 else 'odd'
    worksheet.write(row, 0, i, table_formats[f'table_format_{format_selector}'])
    worksheet.write(row, 1, name, table_formats[f'name_format_{format_selector}'])
    worksheet.write(row, 2, details['role'], table_formats[f'table_format_{format_selector}'])
    worksheet.write_number(row, 3, details['Personal'], table_formats[f'number_format_{format_selector}'])
    worksheet.write_number(row, 4, details['Battles'], table_formats[f'number_format_{format_selector}'])
    col = 5
    tanks = 0
    for tank_id in SELECTED_TANKS_FLAT.keys():
        if any(str(d['tank_id']) == tank_id for d in details['tanks']):
            index = next((index for (index, d) in enumerate(details['tanks']) if str(d['tank_id']) == tank_id), None)
            worksheet.write_number(row, col, details['tanks'][index]['statistics']['battles'], in_garage_format)
            tanks += 1
        else:
            if tank_id in MUST_HAVE:
                worksheet.write(row, col, '', missing_important_format)
            else:
                worksheet.write(row, col, '', table_formats[f'table_format_{format_selector}'])
        col += 1
    worksheet.write_number(row, col, tanks, sum_format)
    row += 1

workbook.close()

input('\nResults saved in "tanks.xlsx". press any key to exit\n')
