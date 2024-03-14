from bs4 import BeautifulSoup
import datetime
import re
import json


class ChangeUrl():
    def __init__(self, url: str):
        self.url = url


    def get_postUrl(self):
        id, isPhoto = self.get_id()
        if isPhoto:
            return f"https://mbasic.facebook.com/photo.php?fbid={id}&id=100063532603663"
        else:
            return f"https://mbasic.facebook.com/story.php?story_fbid={id}&id=100063532603663"
    
    def get_reactorsUrl(self):
        id, isPhoto = self.get_id()
        return f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=50&total_count=50&ft_ent_identifier={id}"
    
    def get_id(self):
        try:
            return self.url.split('/')[5], False
        except:
            return self.url.split('/')[3].split('=')[1].split('&')[0], True


class Scrapper():
    def __init__(self, post_id):
        self.post_id = post_id
        self.info = {
            'post_id': self.post_id,
            'reaction_num': 0,
            'reactors': 0,
            'release_date': []
        }


    def get_reactors(self, page):
        if self.info['reactors'] == 0:
            soup = BeautifulSoup(page, "html.parser")
            reactors = []

            ul = soup.ul
            divs = ul.find_all('div')
            test = ''

            for div in divs:
                account = str(div.a.contents[0])
                reactors.append(account)

            self.info['reactors'] = reactors

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
            "grudnia": 12,
            "sty": 1,
            "lut": 2,
            "mar": 3,
            "kwi": 4,
            "maj": 5,
            "cze": 6,
            "lip": 7,
            "sie": 8,
            "wrz": 9,
            "paź": 10,
            "lis": 11,
            "gru": 12
        }

        if self.info['release_date'] == []:
            soup = BeautifulSoup(page, "html.parser")

            abbr = soup.abbr.contents[0]
            date = abbr.split(' ')
            
            if len(date) == 4:
                year = int(datetime.datetime.now().year)
                month = months[date[1]]
                day = int(date[0])
                hour = int(date[3].split(':')[0])
                minute = int(date[3].split(':')[1])
            else:
                year = int(date[2])
                month = months[date[1]]
                day = int(date[0])
                hour = int(date[4].split(':')[0])
                minute = int(date[4].split(':')[1])

            self.info['release_date'] = [year, month, day, hour, minute]
        return self.info['release_date']


    def get_reaction_num(self, page):
        if self.info['reaction_num'] == 0:
            soup = BeautifulSoup(page, "html.parser")

            print(soup.prettify())

            tags_a = soup.find_all('a')
            filtered_a = list(filter(lambda a: re.search('/ufi/', a['href']), tags_a))
            txt = filtered_a[0].div.div
            txt = txt.contents[0]

            if len(re.findall("\d", txt)) > 3:
                num = ''.join(re.findall("\d", txt)[3:])
            else:
                num = txt
            
            num = int(num)
            
            self.info['reaction_num'] = num
        return self.info['reaction_num']


    def get_all_info(self, post_page, reactors_page):
        self.get_reactors(reactors_page)
        self.get_date(post_page)
        self.get_reaction_num(post_page)
        return self.info