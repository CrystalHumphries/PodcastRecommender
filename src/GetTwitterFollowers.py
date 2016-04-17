# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:44:54 2016

@author: Crystal Humphries


GetTwitterFollowers.py goes through a list of twitter handles
(supplied by "../data/twitter_handles_ids_4Mongo.pkl)
and retrieves 200 followers from each handle.
The retrieved handles are placed into a mongo database.
"""
import time
from pymongo import MongoClient
import pandas as pd
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import itertools
import re
from TwitterAPIs import get_twitter_APIs

'''set up twitter'''
Twitter_apis = get_twitter_APIs()
api_list = Twitter_apis.activate_APIs()
api_generator = itertools.cycle(api_list)

'''get mongoDB'''
client = MongoClient()
db = client['Podcast']
Podcast_twitter = db['PodcastTwitter_handles']

n = 0
new_df = pd.read_pickle("../data/twitter_handles_ids_4Mongo.pkl")
check_names = []
current_api = api_generator.next()


def add_none(title):
    '''adds None to mongodb database for twitter followers'''
    Podcast_twitter.update_one({'Title': title},
                               {'$set':
                               {"TwitterFollowers": ['None']}})

for ob_id in new_df.IDs:
    podcast = Podcast_twitter.find_one({'_id': {'$in': [ob_id]}})
    if 'Podcast_Twitter_handle' in podcast:
        handle = str(podcast['Podcast_Twitter_handle'])
        Title = podcast["Title"]
        if handle == 'NaN':
            add_none(Title)
        elif not re.match(r'@\w+', handle):
            add_none(Title)
        elif 'TwitterFollowers' in podcast:
            continue
        else:
            try:
                '''grab 200 followers from twitter'''
                n += 1
                people = current_api.followers_ids(screen_name=handle,
                                                   count=200)
                Podcast_twitter.update_one({'Title': Title},
                                           {'$set':
                                           {"TwitterFollowers": people}})
                if n == 15:
                    n = 0
                    time.sleep(45)
            except:
                current_api = api_generator.next()
                check_names.append(handle)
        current_api = api_generator.next()

keep_df = pd.DataFrame(check_names)
keep_df.to_json("save_names_didnt_check.json")
