# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 08:18:51 2016

@author: CrystalHumphries
"""

from twython import Twython
import datetime
import json
import re

class Collect_Tweets_by_Hashtag(object):
    
    def __init__(self, searchterm):
        self.searchterm = searchterm
        timestamp       = str(datetime.datetime.now()).split()[0].replace('-','')
        file_trunk      = searchterm.strip('#')
        self.filename   = '_'.join([ timestamp, file_trunk, 'TwitterOutput.csv'])
        self.max_id     = None
        
    def _call_Twitter_api(self):
        twitter_api_info    = json.load(open('/root/.api_keys/Twitter_api.json'))
        CONSUMER_KEY        = twitter_api_info['API Key']
        CONSUMER_SECRET     = twitter_api_info['API Secret']
        self.twitterAPI     = Twython(CONSUMER_KEY, CONSUMER_SECRET)
        
    def get_twitter(self, counts = 100):
        self._call_Twitter_api()
        
        for r in range(counts):
            print (r)
            if self.max_id is None:
                self.tweets      = self.twitterAPI.search(q     = self.searchterm,
                                                     count = 100, lang='en')
            else:
                self.tweets      = self.twitterAPI.search(q = self.searchterm, count = 100, max_id = self.max_id,include_entities   = self.entities)

            self._write_file(self.tweets)
            if 'next_results' in self.tweets['search_metadata']:
                self._get_twitter_search_options(self.tweets)
            else:
                break
        
    def _write_file(self, tweets):
        print ("writing to file")
        with open(self.filename, 'a') as fh:
            for i in range(len(tweets['statuses'])):
                if str(tweets['statuses'][i]['metadata']['iso_language_code']) == 'en':
                    screenName  = tweets['statuses'][i]['user']['screen_name']
                    tweet_text  = tweets['statuses'][i]['text']
                    statusCount = tweets['statuses'][i]['user']['statuses_count']
                    line        = [screenName,str(statusCount), tweet_text ]
                    fh.write(','.join([x.encode('UTF8') for x in line]))

    def _get_twitter_search_options(self, tweets):
        meta          = str(tweets['search_metadata']['next_results'])
        m             = re.search('max_id=(\d+).*include_entities=(\d+)', meta)
        self.max_id   = m.group(1)
        self.entities = m.group(2)            
                
        
