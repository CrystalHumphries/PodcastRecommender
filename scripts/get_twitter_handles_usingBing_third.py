
import requests
from bs4 import BeautifulSoup
import re
from PodcastFeatureEngineering import Podcast_Features
import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient()
# Access/Initiate Database
db = client['Podcast']
# Access/Initiate Table
Podcast_twitter = db['PodcastTwitter_handles']

GF = Podcast_Features()
#df = GenerateFeatures.cleaned_df


ls=[]
n = 0
start = 37482+40000+40000
stop  = start + 40000 

if stop > 155804:
    stop = 155804
    
for i in GF.df.index[start:stop]:
    Title = GF.df.Title[i]
    if re.search('|', Title):
        Title = Title.split('|')[0].strip()
        
    a = Title.split()
    pName = '+'.join(a)
    site = 'https://www.bing.com/search?q=' + pName + '+site%3Atwitter.com'
    soup = BeautifulSoup(requests.get(site).content, 'html')
    try:
        result_step1 = soup.find('ol', {'id':'b_results'}).find('li', {'class':'b_algo'})
        result_step2 = result_step1.find('a').get('href')
        if re.match(r'https://twitter.com/', result_step2):
            '''get the twitter handle'''
            twitter_handle = "@" + result_step2.replace(r'https://twitter.com/', '')
            n +=1
            if n % 100 == 0:
                print "*",
        else:
            twitter_handle = 'NaN'
    except:
        twitter_handle = 'NaN'
    
    Podcast_twitter.insert_one({'Title':GF.df.Title[i], 
                                'PodcastRating':GF.df.RatingCount[i], 
                                'Podcast_Twitter_handle': twitter_handle})