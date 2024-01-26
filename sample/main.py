from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from os.path import join, dirname
# from modules.scrapper import ScrappFb
import mechanize
import re
from urllib.error import HTTPError


def load_payload():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    email = os.environ.get("FAKE_FB_EMAIL")
    password = os.environ.get("FAKE_FB_PASSWORD")

    return str(email), str(password)


def change_url(url: str):
    url_id = url.split('/')[5]
    return f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=60&total_count=17&ft_ent_identifier={url_id}"


def main():
    email, password = load_payload()
    url = "https://www.facebook.com/234Forteca/posts/pfbid02eQCxosEfhYBibKEUabQMZcp178pGknb9qvsDeMJ5kEsk1rKDawmM1LUGzHk8WJTVl"
    correc_url = change_url(url)

    scrapper = ScrappFb(correc_url, email, password)
    scrapper.init_page()
    # result = scrapper.get_page_data()
    
    # soup = BeautifulSoup(result, "html.parser")
    # print(soup.prettify())


# main()

def test():
    import mechanize


    url_page = 'https://mbasic.facebook.com/234Forteca?v=timeline&lst=100002609298316%3A100063532603663%3A1706200664&eav=AfZgA8gZYSeTYiWam4BC4COKD5OZJvmOpwgmAfUXNOmFwNonh_rXGTxR0LWsB0my1No&paipv=0'
    url_correct = "https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=30&total_count=17&ft_ent_identifier=pfbid0MeEjt7MYoe2pjUmpNiqaPT46bq8eq5kTVDbQGp3Ue26r2k4Q2ydcUEamAMG6mXq5l"
    #            f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit={limit}&total_count=17&ft_ent_identifier={url_id}"

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Chrome/121.0.0.0')]
    browser.set_handle_refresh(False)

    #Przejście przez powiadomienie o logowaniu
    res = browser.open(url_correct)

    #Zaakceptowanie ciasteczek
    res = browser.follow_link(url_regex=re.compile('https://mbasic.facebook.com'))
    browser.select_form(nr = 0)
    res = browser.submit()

    #Logowanie się
    browser.select_form(nr = 0) 
    browser.form['email'] = "staneeeer@gmail.com"
    browser.form['pass'] = "#Waldemar5"
    print(browser)
    res = browser.submit()

    soup = BeautifulSoup(res.get_data(), "html.parser")

    ul = soup.ul
    divs = ul.find_all('div')

    for id, div in enumerate(divs):
        a = div.a.contents
        print(id, a)

class ScrappFb:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.browser = mechanize.Browser()
        self.page = None
    
    #Open an url and get past login requirment info
    def open_url(self):
        self.browser.open(self.url)
        self.page = self.browser.follow_link(url_regex=re.compile('https://mbasic.facebook.com'))

    #Get past information about cookiers
    def submit_cookies(self):
        self.browser.select_form(nr=0)
        self.page = self.browser.submit()

    #Log in to the facebook
    def log_in(self):
        try:
            self.browser.select_form(nr=0)
            self.browser.form['email'] = "staneeeer@gmail.com"
            self.browser.form['pass'] = "#Waldemar5"
            self.page = self.browser.submit()
        except HTTPError:
            print("Niestety logowanie nie działa")

    def init_page(self):
        try:
            self.browser.set_handle_robots(False)
            self.browser.set_handle_refresh(False)
            self.browser.addheaders = [('User-agent', 'Chrome/121.0.0.0')]
        except HTTPError:
            print("mechnize.Browser initialization does not work")

        try:
            self.browser.open(self.url)
            self.page = self.browser.follow_link(url_regex=re.compile('https://mbasic.facebook.com'))
        except HTTPError:
            print("Initial opening does not work")

        try:
            self.browser.select_form(nr=0)
            self.page = self.browser.submit()
        except HTTPError:
            print("Cookies handler does not work")

        try:
            self.browser.select_form(nr=0)
            self.browser.form['email'] = "staneeeer@gmail.com"
            self.browser.form['pass'] = "#Waldemar5"
            # print(self.browser)
            self.page = self.browser.submit()
        except HTTPError:
            print("Log in does not work")
        # self.open_url()
        # self.submit_cookies()
        # self.log_in()

    #Get html page
    def get_page_data(self):
        return self.page.get_data()
    

email, password = load_payload()
url = "https://www.facebook.com/234Forteca/posts/pfbid02eQCxosEfhYBibKEUabQMZcp178pGknb9qvsDeMJ5kEsk1rKDawmM1LUGzHk8WJTVl"
correc_url = change_url(url)

scrapper = ScrappFb(correc_url, email, password)
scrapper.init_page()

# test()