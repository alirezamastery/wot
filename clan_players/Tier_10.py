import ctypes
from xlsxwriter import Workbook

from assets import utils
from clan_players.assets.workbook_formats import get_workbook_formats
from clan_players.assets.statics import LOGO, SELECTED_TANKS


# settings for console so it can show ANSI escape:
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
RESET = '\033[0m'
GREEN = '\033[38;5;40m'

print(LOGO)

SELECTED_TANKS_FLAT = utils.flatten_tank_tiers(SELECTED_TANKS)

# +-----------------------------------------------------------------------+
# | Get Data from server                                                  |
# +-----------------------------------------------------------------------+
member_identifiers = utils.get_clan_member_ids()
member_details = dict()

for i, member in enumerate(member_identifiers):
    account_id = member['account_id']
    account_name = member['account_name']
    if account_name == 'HAJJ_ABBAS':
        print(f' {GREEN}{account_name}{RESET}')
    else:
        print(f' {account_name}')
    account_details = dict()
    account_details['role'] = member['role'].capitalize()
    account_stats = utils.get_player_stats(account_id)
    account_details['Personal'] = account_stats['global_rating']
    account_details['Battles'] = account_stats['statistics']['all']['battles']
    tanks = utils.get_player_vehicles(account_id)
    account_details['tanks'] = utils.filter_player_tanks(tanks, SELECTED_TANKS_FLAT)
    member_details[account_name] = account_details

member_details = dict(sorted(member_details.items(), key=lambda v: v[0].upper()))

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
    worksheet.merge_range(0, start_col, 0, start_col + groups_length - 1, tier, formats[details['color']])
    # group names in second row
    group_start = start_col
    for name, group in details['groups'].items():
        group_length = len(group['tanks'])
        worksheet.merge_range(1, group_start, 1, group_start + group_length - 1, name, formats[group['color_header']])
        # each tank in third row
        for i, tank in enumerate(group['tanks'].values()):
            worksheet.write(2, group_start + i, tank, formats[group['color_tank']])
        group_start += group_length
    start_col += groups_length

worksheet.merge_range(0, table_end_col, 2, table_end_col, 'Total Tanks', formats['total_tanks'])
worksheet.set_column(table_end_col, table_end_col, 12)

# write rows
row = 3
for i, (name, details) in enumerate(member_details.items(), 1):
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
