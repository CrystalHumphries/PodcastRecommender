
import time
from pymongo import MongoClient
import requests
import pandas as pd
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import itertools

'''set up twitter'''
APIs = ['Twitter2_API.json',  'Twitter3_API.json', 'Twitter4_API.json', 
        'Twitter_API.json',  'Twitter_API4.json', 'Twitter_API5.json',
         'Twitter_API6.json', 'Twitter_API7.json', 'Twitter_API8.json', 
        'Twitter_API9.json']

loc = '/home/ubuntu/.api/'

def create_api(file_name):
    twitter_api = json.load(open(file_name))

    access_token        = twitter_api['Access Token']
    access_token_secret = twitter_api['Access Token Secret']
    consumer_key        = twitter_api['API Key']
    consumer_secret     = twitter_api['API Secret']
    return access_token, access_token_secret, consumer_key, consumer_secret

api_list = []
for api in APIs:
    file_name = loc + api
    AT,ATS,CK,CKS = create_api(file_name)
    auth = OAuthHandler(CK,CKS)
    auth.set_access_token(AT,ATS)
    api = tweepy.API(auth)
    api_list.append(api)

api_generator = itertools.cycle(api_list)

'''get mongoDB'''
client = MongoClient()
# Access/Initiate Database
db = client['Podcast']
# Access/Initiate Table
#Podcasts = db['PodcastFinal_new']
Podcast_twitter = db['PodcastTwitter_handles']

n=0

check_names=[]

for podcast in Podcast_twitter.find({}):
    if 'Podcast_Twitter_handle' in podcast:
        handle = str(podcast['Podcast_Twitter_handle'])
        Title = podcast["Title"]
        if handle == 'NaN':
            Podcast_twitter.update_one({'Title': Title}, 
                                { '$set': { "TwitterFollowers": ['None'] } })
        elif 'TwitterFollowers' in podcast: # and podcast['TwitterFollowers'][0]!='None':
            continue
        else:
            n+=1
            try:
                people, cursor = current_api.followers_ids(screen_name = handle, 
                                                           count = 200) 
                                                           #cursor = -1)
                Podcast_twitter.update_one({'Title': Title}, { '$set': 
                                                             { "TwitterFollowers": people}})
                                                              #"TwitterCounter":cursor }})
                if n==15:
                    n = 0
                    time.sleep(90)
            except:
                current_api = api_generator.next()
                check_names.append(handle)
        current_api = api_generator.next()  

keep_df = pd.DataFrame(check_names)
keep_df.to_json("save_names_didnt_check.json")