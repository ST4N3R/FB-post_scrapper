import os
from dotenv import load_dotenv
from os.path import join, dirname
from sample.modules.connector import main as connector_main


def load_payload():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    email = os.environ.get("FAKE_FB_EMAIL")
    password = os.environ.get("FAKE_FB_PASSWORD")

    return str(email), str(password)


def change_url(url: str):
    url_id = url.split('/')[5]
    post_url = f"https://mbasic.facebook.com/story.php?story_fbid={url_id}&id=100063532603663&eav=AfYvEHERrGYFnha7pRN-a037Z3t3tcE858rIRZq4V0Jd5raGOd1lPu32NFLwSl7R8f8&refid=17"
    reactors_url = f"https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?limit=60&total_count=17&ft_ent_identifier={url_id}"
    return post_url, reactors_url


def main():
    email, password = load_payload()
    url = "https://www.facebook.com/234Forteca/posts/pfbid02eQCxosEfhYBibKEUabQMZcp178pGknb9qvsDeMJ5kEsk1rKDawmM1LUGzHk8WJTVl"
    post_url, reactors_url = change_url(url)

    browser, html = connector_main(post_url, reactors_url, email, password)


if __name__ == '__main__':
    main()