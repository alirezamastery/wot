import json
import xlsxwriter

from statics import TANKS_COLORS_BY_ID, MUST_HAVE, TIER_10


with open('./players.json', ) as player_file:
    players = json.load(player_file)

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
    'color_format_954ECA': workbook.add_format({
        'bg_color': '#954ECA', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_0594FF': workbook.add_format({
        'bg_color': '#0594FF', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_00B050': workbook.add_format({
        'bg_color': '#00B050', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_FFFF00': workbook.add_format({
        'bg_color': '#FFFF00', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
    'color_format_FFC000': workbook.add_format({
        'bg_color': '#FFC000', 'border': True, 'align': 'left', 'valign': 'vcenter', 'font_size': '9', 'text_wrap': True
    }),
}
in_garage_format = workbook.add_format({'bg_color': '#92D050', 'border': True})
missing_important_format = workbook.add_format({'bg_color': '#FF0000', 'border': True})
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
    print(color)
    worksheet.write(0, col, value, color_formats[f'color_format_{color[1:]}'])
    col += 1
worksheet.write(0, col, 'sum', sum_format)

# write rows
row = 1
for i, (name, details) in enumerate(players.items(), 1):
    worksheet.write(row, 0, i, general_format)
    worksheet.write(row, 1, name, name_format)
    worksheet.write(row, 2, details['role'], general_format)
    worksheet.write_number(row, 3, details['Personal'], number_format)
    worksheet.write_number(row, 4, details['Battles'], number_format)
    col = 5
    tanks = 0
    for tank_id in TIER_10.keys():
        # print(TIER_10[tank_id])
        if any(str(d['tank_id']) == tank_id for d in details['tanks']):
            worksheet.write(row, col, '', in_garage_format)
            tanks += 1
        else:
            if tank_id in MUST_HAVE:
                worksheet.write(row, col, '', missing_important_format)
            else:
                worksheet.write(row, col, '', general_format)
        col += 1
    worksheet.write_number(row, col, tanks, sum_format)
    row += 1

workbook.close()
