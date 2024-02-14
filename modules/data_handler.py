from google.cloud import datastore
from modules.connector import get_post_page, get_reactors_page
from modules.scrapper import Scrapper, ChangeUrl
import pandas as pd
import os
import datetime

class DataHandler():
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceKey.json'
        self.dataClient = datastore.Client()
        self.data = pd.DataFrame()


    def readData(self):
        query = self.dataClient.query(kind='posts')
        query.add_filter('fb_post_url', '>', ' ')

        release_date = []
        reaction_num = []
        post_id = []
        for result in query.fetch():
            release_date.append(datetime.datetime(year=result['release_date'][0],
                                        month=result['release_date'][1],
                                        day=result['release_date'][2],
                                        hour=result['release_date'][3],
                                        minute=result['release_date'][4]))
            reaction_num.append(result['reaction_num'])
            post_id.append(result['fb_post_url'])
        
        self.data = pd.DataFrame({
            'release_date': release_date, 
            'reaction_num': reaction_num, 
            'fb_post_url': post_id
            })
        return self.data


    def addData(self, post_id: str):
        changeUrl = ChangeUrl(post_id)
        url = changeUrl.get_postUrl()

        postPage = get_post_page(url)

        scrapper = Scrapper(changeUrl.get_id())
        date = scrapper.get_date(postPage)
        reaction_num = scrapper.get_reaction_num(postPage)

        try:
            entity = datastore.Entity(self.dataClient.key('posts'))
            entity.update({
                'release_date': date,
                'reaction_num': reaction_num,
                'fb_post_url': changeUrl.get_id()
            })

            self.dataClient.put(entity)

            return True
        except Exception:
            return False
        

    def dayOfWeek_by_reactionNum(self, **kwargs):
        if self.data.empty:
            self.readData()
        else:
            self.data['dayOfWeek'] = self.data['release_date'].apply(lambda x: x.dayofweek + 1)

        if 'startDate' in kwargs.keys():
            startDate = pd.Timestamp(kwargs['startDate'])
        else:
            startDate = self.data['release_date'].min()
        if 'endDate' in kwargs.keys():
            endDate = pd.Timestamp(kwargs['endDate'])
        else:
            endDate = pd.Timestamp.today()

        data_filtered = self.data[(self.data['release_date'] >= startDate) & (self.data['release_date'] <= endDate)]
        group = data_filtered.groupby('dayOfWeek')['reaction_num'].apply(np.average)

        for i in range(1, 8):
            try:
                group[i]
            except:
                group[i] = 0.0
        
        return group.sort_index()