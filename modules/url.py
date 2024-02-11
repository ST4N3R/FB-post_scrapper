import os
from dotenv import load_dotenv
from os.path import join, dirname
from modules.connector import main


def load_payload():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    email = os.environ.get("FAKE_FB_EMAIL")
    password = os.environ.get("FAKE_FB_PASSWORD")

    return str(email), str(password)


def main():
    email, password = load_payload()
    url = "https://www.facebook.com/234Forteca/posts/pfbid02eQCxosEfhYBibKEUabQMZcp178pGknb9qvsDeMJ5kEsk1rKDawmM1LUGzHk8WJTVl"
    post_url = post_url(url)
    reactors_url = ''

    browser, html = connector_main(post_url, reactors_url, email, password)


class change_url():
    def __init__(self, url: str):
        self.url = url.split('/')[5]
        self.postUrl = f"https://mbasic.facebook.com/story.php?story_fbid={self.url}&id=100063532603663&eav=AfYvEHERrGYFnha7pRN-a037Z3t3tcE858rIRZq4V0Jd5raGOd1lPu32NFLwSl7R8f8&refid=17"
        self.reactorsUurl = f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=60&total_count=17&ft_ent_identifier={self.url}"

    def get_postUrl(self):
        return self.postUrl
    
    def get_reactorsUrl(self):
        return self.reactorsUurl 