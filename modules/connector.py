import mechanize
from urllib.error import HTTPError
import re


def init(browser: mechanize.Browser):
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Chrome/120.0.0.0')]
    browser.set_handle_refresh(False)
    return browser


def open_url(browser: mechanize.Browser, url: str):
    browser.open(url)
    page = browser.follow_link(url_regex=re.compile('https://mbasic.facebook.com'))
    return browser, page


def submit_cookies(browser: mechanize.Browser):
    browser.select_form(nr = 0)
    page = browser.submit()
    return browser, page


def log_in(browser: mechanize.Browser, email: str, password: str):
    browser.select_form(nr = 0) 
    browser.form['email'] = "staneeeer@gmail.com"
    browser.form['pass'] = "#Waldemar5"
    page = browser.submit()
    return browser, page


def main(post_url: str, reactors_url: str, email: str, password: str):
    browser = mechanize.Browser()
    page = None

    browser = init(browser)
    browser, page = open_url(browser, post_url)
    browser, page = submit_cookies(browser)
    browser, page = log_in(browser, email, password)
    return browser, page.get_data()