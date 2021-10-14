import datetime as dt
from operator import itemgetter
from pprint import pprint

from xlsxwriter import Workbook


DATA = {'Abozar2020':               ['111', '0', '0', '0', '0'],
        'AmirDL11':                 ['25', '0', '0', '25', '0'],
        'Az_evil':                  ['51', '0', '0', '0', '0'],
        'Black_Bulldozer':          ['0', '0', '0', '0', '0'],
        'CAPTAINalireza':           ['51', '0', '0', '23', '0'],
        'DWolfgang':                ['15', '0', '0', '0', '0'],
        'Danger_Tank_2018':         ['293', '0', '0', '25', '0'],
        'Eagle_Artillery':          ['0', '0', '0', '0', '0'],
        'Evil_D_ead':               ['162', '0', '0', '0', '0'],
        'F14tomcatD':               ['0', '0', '0', '0', '0'],
        'HAJJ_ABBAS':               ['0', '0', '0', '0', '0'],
        'HAJ_FARZAD':               ['67', '0', '0', '20', '0'],
        'HIV313':                   ['204', '0', '0', '0', '0'],
        'Hasti100':                 ['69', '0', '0', '0', '0'],
        'HaveMerccy':               ['0', '0', '0', '0', '0'],
        'Hmsmi96':                  ['0', '0', '0', '0', '0'],
        'IC_alpha':                 ['90', '0', '0', '16', '0'],
        'IronMamuTH':               ['12', '0', '0', '0', '0'],
        'IronWolf___FuryAlpha':     ['234', '0', '0', '0', '0'],
        'King_Arsaces':             ['49', '0', '0', '0', '0'],
        'MH66A':                    ['18', '0', '0', '0', '0'],
        'MKing_2013':               ['0', '0', '0', '0', '0'],
        'MohammadBzG':              ['0', '0', '0', '0', '0'],
        'Mojtaba1390':              ['114', '0', '0', '0', '0'],
        'NS710':                    ['0', '0', '0', '0', '0'],
        'Nash_Master':              ['19', '0', '0', '25', '0'],
        'OM222O':                   ['0', '0', '0', '25', '0'],
        'OluM__MeLeGi':             ['25', '0', '0', '0', '0'],
        'OosKarim':                 ['25', '0', '0', '0', '0'],
        'PERSIAN_ARTY':             ['90', '0', '0', '0', '0'],
        'PEYZ21':                   ['0', '0', '0', '0', '0'],
        'Pandaw_':                  ['15', '0', '0', '0', '0'],
        'PersianGuard':             ['59', '0', '0', '2', '0'],
        'Persian_c0mmander':        ['0', '0', '0', '0', '0'],
        'Persian_cheetah1975':      ['82', '0', '0', '34', '2'],
        'Pezh7man':                 ['0', '0', '0', '0', '0'],
        'Pezhman_mb2':              ['0', '0', '0', '0', '0'],
        'RQ170':                    ['0', '0', '0', '0', '0'],
        'Reichsmarschall':          ['0', '0', '0', '0', '0'],
        'Richie_haze':              ['0', '0', '0', '0', '0'],
        'SHAHDAD':                  ['0', '0', '0', '0', '0'],
        'SHAyANXxX':                ['0', '0', '0', '0', '0'],
        'S_A_P':                    ['73', '0', '0', '25', '0'],
        'S_A_Pplus':                ['0', '0', '0', '0', '0'],
        'SaeedTiaMo':               ['0', '0', '0', '0', '0'],
        'Sir_Mojtaba':              ['30', '0', '0', '0', '0'],
        'Stark_man':                ['52', '0', '0', '0', '0'],
        'Tp_Se7en':                 ['0', '0', '0', '0', '0'],
        'Vacillate':                ['0', '0', '0', '0', '0'],
        'WW2_42':                   ['0', '0', '0', '0', '0'],
        'Wasting_My_Hate':          ['0', '0', '0', '0', '0'],
        'XeNoNAxe':                 ['0', '0', '0', '0', '0'],
        '_BoogeyMan____':           ['0', '0', '0', '0', '0'],
        '_EzioAuditore_':           ['8', '0', '0', '0', '0'],
        '_O_h3ll_nO_':              ['45', '0', '0', '0', '0'],
        '_Sharaf_Shah___':          ['0', '0', '0', '0', '0'],
        '__LoneWolf':               ['79', '0', '0', '19', '0'],
        '__TheDarKnight__':         ['0', '0', '0', '0', '0'],
        '_b4V_':                    ['144', '0', '0', '36', '0'],
        '_persian_soldier_':        ['0', '0', '0', '0', '0'],
        'achee64':                  ['93', '0', '0', '21', '0'],
        'amirali':                  ['44', '0', '0', '0', '0'],
        'ariangunner':              ['0', '0', '0', '0', '0'],
        'cp_evil5':                 ['3', '0', '0', '0', '0'],
        'deadR90':                  ['0', '0', '0', '0', '0'],
        'farzad_sh_2020':           ['0', '0', '0', '0', '0'],
        'foroozesh':                ['22', '0', '0', '1', '0'],
        'hosein1':                  ['38', '0', '0', '0', '0'],
        'hrm70':                    ['115', '0', '0', '0', '0'],
        'jackkrauser_2000':         ['10', '0', '0', '0', '0'],
        'k00r0sh':                  ['110', '0', '0', '32', '5'],
        'keyhanzm':                 ['102', '0', '0', '8', '0'],
        'king_cyaxares':            ['90', '0', '0', '0', '0'],
        'l_Manticore_l':            ['16', '0', '0', '0', '0'],
        'l_Revenger_l':             ['0', '0', '0', '0', '0'],
        'leonAIR':                  ['0', '0', '0', '0', '0'],
        'mamolino665':              ['14', '0', '0', '0', '0'],
        'mehranmh7':                ['9', '0', '0', '0', '0'],
        'mohammad_72':              ['48', '0', '0', '25', '0'],
        'mosijoOokeR':              ['89', '0', '0', '0', '0'],
        'nawidahmadi0311':          ['0', '0', '0', '0', '0'],
        'persian_cheetah_comander': ['0', '0', '0', '0', '0'],
        'persian_miomio':           ['0', '0', '0', '0', '0'],
        'persusus':                 ['0', '0', '0', '0', '0'],
        'pezhmanS22':               ['0', '0', '0', '0', '0'],
        'reza009':                  ['0', '0', '0', '0', '0'],
        'reza_nopo':                ['69', '0', '0', '0', '0'],
        'roham7a':                  ['12', '0', '0', '0', '0'],
        'salim_sk66':               ['100', '0', '0', '11', '0'],
        'saman_hunterIRIN':         ['71', '0', '0', '0', '0'],
        'seeyamak':                 ['30', '0', '0', '21', '0'],
        'shazdeh1':                 ['0', '0', '0', '0', '0'],
        'tank_destroyer_231':       ['0', '0', '0', '0', '0'],
        'termix2015':               ['0', '0', '0', '0', '0'],
        'towkhc':                   ['6', '0', '0', '0', '0'],
        'wolf399':                  ['0', '0', '0', '0', '0'],
        'xX_Elitehunter_Xx':        ['29', '0', '0', '0', '0']}

ODD_COLOR = '#FCD5B4'
ODD_COLOR_LIGHT = '#92CDDC'


def get_workbook_formats(workbook):
    return {
        'name_even':      workbook.add_format({
            'border': True,
            'align':  'center',
            'valign': 'vcenter',
            'bold':   True,
        }),
        'name_odd':       workbook.add_format({
            'border':   True,
            'align':    'center',
            'valign':   'vcenter',
            'bold':     True,
            'bg_color': ODD_COLOR,
        }),
        'name_odd_light': workbook.add_format({
            'border':   True,
            'align':    'center',
            'valign':   'vcenter',
            'bold':     True,
            'bg_color': ODD_COLOR_LIGHT,
        }),
    }


class ExcelOutput:
    headers = ['Name', 'Random', 'GM 10', 'GM 8', 'Skirmish', 'Stronghold', 'Sum (without random)']

    def __init__(self, data: dict):
        date_now = dt.date.today()
        one_weak = dt.timedelta(days=7)
        last_weak_date = date_now - one_weak

        workbook = Workbook('tanks.xlsx')
        worksheet = workbook.add_worksheet()
        formats = get_workbook_formats(workbook)

        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 5, 12)
        worksheet.set_column(5, 6, 20)
        worksheet.set_column(9, 11, 25)
        worksheet.freeze_panes(1, 0)

        for name, item in data.items():
            team_work_sum = sum([int(value) for index, value in enumerate(item) if index > 0])
            item.append(team_work_sum)
            item.insert(0, name)
        list_date = list(data.values())
        sorted_data = sorted(list_date, key=itemgetter(6), reverse=True)
        pprint(sorted_data)

        # write header
        for i, header in enumerate(self.headers):
            worksheet.write(0, i, header, formats['name_even'])
        worksheet.write(0, 8, 'Date:', formats['name_even'])
        worksheet.write(0, 9, f'{last_weak_date} to {date_now}', formats['name_even'])

        # write rows
        row = 1
        for i, item in enumerate(sorted_data, 1):
            format_selector = 'even' if i % 2 == 0 else 'odd'
            for j, stat in enumerate(item):
                if j == 0:
                    worksheet.write(row, j, stat, formats[f'name_{format_selector}'])
                else:
                    worksheet.write_number(row, j, int(stat), formats[f'name_{format_selector}'])
            row += 1

        workbook.close()


if __name__ == '__main__':
    excel = ExcelOutput(data=DATA)
