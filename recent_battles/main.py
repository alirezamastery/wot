import requests
from pprint import pprint

from xlsxwriter import Workbook
from bs4 import BeautifulSoup


CONNECTION_EXCEPTION_MSG = 'There was an error in connection to the server'
APPLICATION_ID = '0ccfb285e3be979fc9d0ab20e7f05703'


def get_clan_member_ids():
    url = f'https://api.worldoftanks.eu/wot/clans/info/?application_id={APPLICATION_ID}&clan_id=500071718'
    response = requests.get(url).json()
    if not response['status'] == 'ok':
        raise RuntimeError(CONNECTION_EXCEPTION_MSG)
    return response['data']['500071718']['members']


class Robot:
    excel_headers = ['Name', 'Stats', 'GM 10', 'GM 8', 'Skirmish', 'Stronghold']

    def __init__(self):
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

        workbook = Workbook('7days.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 5, 10)
        worksheet.freeze_panes(1, 1)
        # write header
        for i, header in enumerate(self.excel_headers):
            worksheet.write(0, i, header, )
        # write rows
        row = 1
        for i, (name, stats) in enumerate(self.members_data.items(), 1):
            worksheet.write(row, 0, name)
            for j, stat in enumerate(stats, 1):
                worksheet.write_number(row, j, int(stat))
            row += 1
        workbook.close()


if __name__ == '__main__':
    robot = Robot()
