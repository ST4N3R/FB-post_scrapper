import mechanize
from urllib.error import HTTPError
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv 


def init(browser: mechanize.Browser, url: str):
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Chrome/120.0.0.0')]
    browser.set_handle_refresh(False)
    browser.open(url)
    return browser


def open_url(browser: mechanize.Browser, url: str):
    page = browser.follow_link(url_regex=re.compile('https://mbasic.facebook.com'))
    return browser, page


def submit_cookies(browser: mechanize.Browser):
    browser.select_form(nr = 0)
    page = browser.submit()
    return browser, page


def log_in(browser: mechanize.Browser):
    dotenvPath = join(dirname(__file__), '.env')
    load_dotenv(dotenvPath)

    email = str(os.environ.get('FAKE_FB_EMAIL'))
    password = str( os.environ.get('FAKE_FB_PASSWORD'))

    browser.select_form(nr = 0) 
    browser.form['email'] = email
    browser.form['pass'] = password
    page = browser.submit()
    return browser, page


def get_post_page(postUrl: str):
    browser = mechanize.Browser()
    page = None

    browser = init(browser, postUrl)
    browser, page = submit_cookies(browser)
    browser, page = log_in(browser)

    return page.get_data()


# todo: Dodać możliwość łączenia się ze stroną z osobami, które zareagowały na posta
def get_reactors_page(reactorsUrl: str):
    pass