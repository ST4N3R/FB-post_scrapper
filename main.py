from flask import Flask, render_template, url_for, request
import os
from google.cloud import datastore
from modules.url import change_url
from modules.connector import get_post_page, get_reactors_page
from modules.scrapper import Scrapper


# todo: Zmienić nazwę fb_post_id na fb_post_url
def readData(client: datastore.Client):
    results = []

    query = client.query(kind='posts')
    query.add_filter('fb_post_id', '>', ' ')

    for result in query.fetch():
        results.append({
            'release_date': result['release_date'],
            'reaction_num': result['reaction_num'],
            'fb_post_id': result['fb_post_id']
        })
    return results


def addData(client: datastore.Client, post_id: str):
    changeUrl = change_url(post_id)
    url = changeUrl.get_postUrl()

    postPage = get_post_page(url)

    scrapper = Scrapper(changeUrl.get_id())
    date = scrapper.get_date(postPage)
    reaction_num = scrapper.get_reaction_num(postPage)

    try:
        entity = datastore.Entity(client.key('posts'))
        entity.update({
            'release_date': date,
            'reaction_num': reaction_num,
            'fb_post_id': changeUrl.get_id()
        })

        client.put(entity)

        return True
    except Exception:
        return False


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceKey.json'
    dataClient = datastore.Client()

    if request.method == 'POST':
        url = request.form['url_text']

        if addData(dataClient, url):
            return url
        else:
            return "Coś poszło nie tak"
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)