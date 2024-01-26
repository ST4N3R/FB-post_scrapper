from urllib.error import HTTPError
import mechanize
import re


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
            print(self.browser)
            # self.page = self.browser.submit()
        except HTTPError:
            print("Log in does not work")
        # self.open_url()
        # self.submit_cookies()
        # self.log_in()

    #Get html page
    def get_page_data(self):
        return self.page.get_data()