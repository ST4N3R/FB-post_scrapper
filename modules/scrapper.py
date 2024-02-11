from bs4 import BeautifulSoup


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
        if self.info['release_date'] == []:
            pass
        return self.info['release_dat']


    def get_reaction_num(self, page):
        if self.info['reaction_num'] == 0:
            pass
        return self.info['reaction_num']


    def get_all_info(self, post_page, reactors_page):
        self.get_reactors(reactors_page)
        self.get_date(post_page)
        self.get_reaction_num(post_page)
        return self.info