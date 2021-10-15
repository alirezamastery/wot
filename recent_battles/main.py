import datetime as dt
from operator import itemgetter

import requests
from xlsxwriter import Workbook
from bs4 import BeautifulSoup

from assets.statics import LOGO


CONNECTION_EXCEPTION_MSG = 'There was an error in connection to the server'
APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'


def get_clan_member_ids():
    url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
    response = requests.get(url).json()
    if not response['status'] == 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return response['data']['500071718']['members']


ODD_COLOR = '#FCD5B4'


def get_workbook_formats(workbook):
    return {
        'name_even': workbook.add_format({
            'border': True,
            'align':  'center',
            'valign': 'vcenter',
            'bold':   True,
        }),
        'name_odd':  workbook.add_format({
            'border':   True,
            'align':    'center',
            'valign':   'vcenter',
            'bold':     True,
            'bg_color': ODD_COLOR,
        }),
    }


class Robot:
    excel_headers = ['#', 'Name', 'Random', 'GM 10', 'GM 8', 'Skirmish', 'Stronghold', 'Sum (without random)']

    def __init__(self):
        print(LOGO)
        print()
        print('Getting clan members battles in the last 7 days:\n')
        clan_members = get_clan_member_ids()
        self.members_data = {}
        for i, member in enumerate(clan_members):
            account_id = member['account_id']
            account_name = member['account_name']
            print(account_name)
            self.members_data[account_name] = self.get_member_data(account_id, account_name)
        self.create_excel()

    def get_member_data(self, account_id: int, account_name: str) -> list:
        url = f'https://en.wot-life.com/eu/player/{account_name}-{account_id}/'
        page_html = self.get_page(url)
        soup = BeautifulSoup(page_html, 'html.parser')
        tab_container = soup.find('div', class_='tab-container')
        data = []
        for i, tab in enumerate(tab_container):
            if i in [0, 1, 2, 6, 7]:
                tds = tab.findAll('td', attrs={'class': 'text-right'})
                data.append(tds[2].text)
        return data

    @staticmethod
    def get_page(url):
        while True:
            try:
                response = requests.get(url, timeout=10)
                return response.content
            except Exception as e:
                print(e)

    def create_excel(self):
        date_now = dt.date.today()
        one_weak = dt.timedelta(days=7)
        last_weak_date = date_now - one_weak

        workbook = Workbook(f'7days_battles_{date_now}.xlsx')
        worksheet = workbook.add_worksheet()
        formats = get_workbook_formats(workbook)

        worksheet.set_column(0, 1, 2)
        worksheet.set_column(1, 2, 30)
        worksheet.set_column(2, 6, 12)
        worksheet.set_column(6, 7, 20)
        worksheet.set_column(10, 12, 25)
        worksheet.freeze_panes(1, 2)

        # sort based on sum:
        for name, item in self.members_data.items():
            team_work_sum = sum([int(value) for index, value in enumerate(item) if index > 0])
            item.append(team_work_sum)
            item.insert(0, name)
        list_date = list(self.members_data.values())
        sorted_data = sorted(list_date, key=itemgetter(6), reverse=True)

        # write header
        for i, header in enumerate(self.excel_headers):
            worksheet.write(0, i, header, formats['name_even'])
        worksheet.write(0, 9, 'Date:', formats['name_even'])
        worksheet.write(0, 10, f'{last_weak_date} to {date_now}', formats['name_even'])
        # write rows
        row = 1
        for i, item in enumerate(sorted_data, 1):
            format_selector = 'even' if i % 2 == 0 else 'odd'
            worksheet.write_number(row, 0, row, formats[f'name_{format_selector}'])
            for j, stat in enumerate(item, 1):
                if j == 1:
                    worksheet.write(row, j, stat, formats[f'name_{format_selector}'])
                else:
                    worksheet.write_number(row, j, int(stat), formats[f'name_{format_selector}'])
            row += 1

        workbook.close()


if __name__ == '__main__':
    robot = Robot()
