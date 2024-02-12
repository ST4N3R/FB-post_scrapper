from bs4 import BeautifulSoup
import datetime


class Scrapper():
    def __init__(self, post_id):
        self.post_id = post_id
        self.info = {
            'post_id': self.post_id,
            'reaction_num': 0,
            'reactors': [],
            'release_date': []
        }


    def get_reactors(self, page):
        if self.info['reactors'] == []:
            soup = BeautifulSoup(page, "html.parser")

            ul = soup.ul
            divs = ul.find_all('div')

            for div in divs:
                account = div.a.contents
                self.info['reactors'].append(account)
        return self.info['reactors']
        

    def get_date(self, page):
        months = {
            "stycznia": 1,
            "lutego": 2,
            "marca": 3,
            "kwietnia": 4,
            "maja": 5,
            "czerwca": 6,
            "lipca": 7,
            "sierpnia": 8,
            "września": 9,
            "października": 10,
            "listopada": 11,
            "grudnia": 12
        }

        if self.info['release_date'] == []:
            soup = BeautifulSoup(page, "html.parser")

            abbr = soup.abbr.contents[0]
            date = abbr.split(' ')
            
            if len(date) == 4:
                year = datetime.datetime.now().year
                month = months[date[1]]
                day = date[0]
                hour = date[3].split(':')[0]
                minute = date[3].split(':')[1]
            else:
                year = date[2]
                month = months[date[1]]
                day = date[0]
                hour = date[4].split(':')[0]
                minute = date[4].split(':')[1]

            self.info['release_date'] = datetime.datetime(year, month, day, hour, minute)
        return self.info['release_date']


    def get_reaction_num(self, page):
        if self.info['reaction_num'] == 0:
            pass
        return self.info['reaction_num']


    def get_all_info(self, post_page, reactors_page):
        self.get_reactors(reactors_page)
        self.get_date(post_page)
        self.get_reaction_num(post_page)
        return self.info