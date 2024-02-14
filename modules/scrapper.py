from bs4 import BeautifulSoup
import datetime
import re


class ChangeUrl():
    def __init__(self, url: str):
        self.url = url
        pass

    def get_postUrl(self):
        id = self.get_id()
        return f"https://mbasic.facebook.com/story.php?story_fbid={id}&id=100063532603663"
    
    def get_reactorsUrl(self):
        id = self.get_id()
        return f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=60&total_count=17&ft_ent_identifier={id}"
    
    def get_id(self):
        return self.url.split('/')[5]


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

            print(soup.abbr)
            print(soup.prettify())
            abbr = soup.abbr.contents[0]
            date = abbr.split(' ')
            
            if len(date) == 4:
                year = datetime.datetime.now().year
                month = months[date[1]]
                day = int(date[0])
                hour = int(date[3].split(':')[0])
                minute = int(date[3].split(':')[1])
            else:
                year = date[2]
                month = months[date[1]]
                day = int(date[0])
                hour = int(date[4].split(':')[0])
                minute = int(date[4].split(':')[1])

            self.info['release_date'] = [year, month, day, hour, minute]
        return self.info['release_date']


    def get_reaction_num(self, page):
        if self.info['reaction_num'] == 0:
            soup = BeautifulSoup(page, "html.parser")

            tags_a = soup.find_all('a')
            filtered_a = list(filter(lambda a: re.search('/ufi/', a['href']), tags_a))
            num = filtered_a[0].div.div
            num = int(num.contents[0])
            
            self.info['reaction_num'] = num
        return self.info['reaction_num']


    def get_all_info(self, post_page, reactors_page):
        self.get_reactors(reactors_page)
        self.get_date(post_page)
        self.get_reaction_num(post_page)
        return self.info