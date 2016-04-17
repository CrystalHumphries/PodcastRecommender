# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:00:30 2016

@author: Crystal.Humphries

ObtainTwitterHandles.py does a bing search for bing handles and
retrieves the top find. This is likely to be the handle for the
'binged' podcast. The retrieved twitter handle is placed into
a mongo database.
"""
import requests
from bs4 import BeautifulSoup
import re
from PodcastFeatureEngineering import Podcast_Features
import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client['Podcast']
Podcast_twitter = db['PodcastTwitter_handles']

'''obtained cleaned data frame which contains podcast titles'''
GF = Podcast_Features()

ls = []
n = 0
start = 37482
end = start + 40000

if end > 155804:
    end = 155804

for i in GF.df.index[start:stop]:
    Title = GF.df.Title[i]
    if re.search('|', Title):
        Title = Title.split('|')[0].strip()

    a = Title.split()
    pName = '+'.join(a)
    site = 'https://www.bing.com/search?q=' + pName + '+site%3Atwitter.com'
    soup = BeautifulSoup(requests.get(site).content, 'html')
    try:
        result_step1 = soup.find('ol', {'id': 'b_results'})\
                                .find('li', {'class': 'b_algo'})
        result_step2 = result_step1.find('a').get('href')
        if re.match(r'https://twitter.com/', result_step2):
            '''get the twitter handle'''
            t_name = result_step2.replace(r'https://twitter.com/', '')
            twitter_handle = "@" + t_name
            n += 1
            if n % 100 == 0:
                print "*",
        else:
            twitter_handle = 'NaN'
    except:
        twitter_handle = 'NaN'

    Podcast_twitter.insert_one({'Title': GF.df.Title[i],
                                'PodcastRating': GF.df.RatingCount[i],
                                'Podcast_Twitter_handle': twitter_handle})
