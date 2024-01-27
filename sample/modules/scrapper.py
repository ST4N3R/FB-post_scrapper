from bs4 import BeautifulSoup


class Scrapper():
    def __init__(self, post_id):
        self.post_id = post_id
        self.info = [self.post_id, [], []]


    def get_reactors(self, page):
        soup = BeautifulSoup(page, "html.parser")

        ul = soup.ul
        divs = ul.find_all('div')

        for div in divs:
            account = div.a.contents
            self.info[2].append(account)
        return self.info[2]
        

    def get_date(self, page):
        pass


    def get_all_info(self, post_page, reactors_page):
        self.get_reactors(reactors_page)
        self.get_date(post_page)
        return self.info