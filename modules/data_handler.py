from google.cloud import datastore
from modules.connector import get_post_page, get_reactors_page
from modules.scrapper import Scrapper, ChangeUrl
import pandas as pd
import numpy as np
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
        reactors = []
        for result in query.fetch():
            release_date.append(datetime.datetime(year=result['release_date'][0],
                                        month=result['release_date'][1],
                                        day=result['release_date'][2],
                                        hour=result['release_date'][3],
                                        minute=result['release_date'][4]))
            reaction_num.append(result['reaction_num'])
            post_id.append(result['fb_post_url'])
            reactors.append(result['reactors'])
        
        self.data = pd.DataFrame({
            'release_date': release_date, 
            'reaction_num': reaction_num, 
            'fb_post_url': post_id,
            'reactors': reactors
            })
        return self.data


    def addData(self, post_id: str):
        changeUrl = ChangeUrl(post_id)
        url = changeUrl.get_postUrl()
        url_r = changeUrl.get_reactorsUrl()

        postPage = get_post_page(url)
        reactorsPage = get_reactors_page(url_r)

        id, isPhoto = changeUrl.get_id()
        scrapper = Scrapper(id)
        date = scrapper.get_date(postPage)
        reaction_num = scrapper.get_reaction_num(postPage)
        reactors = scrapper.get_reactors(reactorsPage)

        try:
            entity = datastore.Entity(self.dataClient.key('posts'))

            entity.update({
                    'release_date': date,
                    'reaction_num': reaction_num,
                    'fb_post_url': id,
                    'reactors': reactors
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
        
        return group.sort_index().to_list()
    

    def month_by_reactionNum(self, **kwargs):
        if self.data.empty:
            self.readData()
        else:
            self.data['month'] = self.data['release_date'].apply(lambda x: x.month)

        if 'startDate' in kwargs.keys():
            startDate = pd.Timestamp(kwargs['startDate'])
        else:
            startDate = self.data['release_date'].min()
        if 'endDate' in kwargs.keys():
            endDate = pd.Timestamp(kwargs['endDate'])
        else:
            endDate = pd.Timestamp.today()

        data_filtered = self.data[(self.data['release_date'] >= startDate) & (self.data['release_date'] <= endDate)]
        group = data_filtered.groupby('month')['reaction_num'].apply(np.average)

        for i in range(1, 13):
            try:
                group[i]
            except:
                group[i] = 0.0

        return group.sort_index().to_list()
    

    def hole_year(self, **kwargs):
        if self.data.empty:
            self.readData()
        
        if 'startDate' in kwargs.keys():
            startDate = pd.Timestamp(kwargs['startDate'])
        else:
            startDate = self.data['release_date'].min()
        if 'endDate' in kwargs.keys():
            endDate = pd.Timestamp(kwargs['endDate'])
        else:
            endDate = pd.Timestamp.today()

        dates = []
        nums = []

        data_filtered = self.data[(self.data['release_date'] >= startDate) & (self.data['release_date'] <= endDate)]
        data_filtered = data_filtered.sort_values('release_date')

        for i, j in zip(data_filtered['release_date'], data_filtered['reaction_num']):
            dates.append(i.strftime('%Y-%m-%d'))
            nums.append(j)

        if len(dates) > 30:
            dates = dates[:30]
            nums = nums[:30]

        return dates, nums
    

    def db_view(self):
        if self.data.empty:
            self.readData()

        lp = len(self.data)
        if lp > 10:
            df = self.data[:10]
        else:
            df = self.data

        postId = df['fb_post_url'].to_list()
        reactionNum = df['reaction_num'].to_list()
        releaseDate =df['release_date'].to_list()

        return lp, postId, reactionNum, releaseDate
    

    def reactors_list(self, **kwargs):
        if self.data.empty:
            self.readData()
        
        reactors = []
        lp = 20
        for row in self.data['reactors']:
            reactors += row
        
        df = pd.DataFrame(data=reactors, columns=["Name"])
        valuesCount = df.value_counts()[:lp]

        indxs = valuesCount.index.to_list()
        nums = valuesCount.values.tolist()

        return  indxs, nums, lp