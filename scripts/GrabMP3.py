# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:38:10 2016

@author: Crystal.Humphries

GrabMP3.py uses a list of RSS websites and
grabs the first 5 MP3s and places them into
the bucket s3://podcastrecommender
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto
import re
import os
import json
from twitter_followers_list import get_twitter_followers

'''Obtain list of rss websites'''


class Grab_MP3S(object):
    
    def __init__(self):
        self.bucket = None
        self.df = None
        self.broken_links = []
        
    def connect_bucket(self, bucket_name):
        '''uses api key to connect to bucket name'''
        home = os.environ['HOME']
        awi_loc = os.path.join(home, '.api/AWS.api')
        awi = json.load(open(awi_loc))
    
        access_key = str(awi['AWS_ACCESS_KEY'])
        secret_access_key = str(awi['AWS_SECRET_ACCESS_KEY'])
    
        conn = boto.connect_s3(access_key, secret_access_key)
        self.bucket = conn.get_bucket(bucket_name, validate=False)

    def _folder_name(self, title):
        if re.search('|', title):
            title = title.split('|')[0].strip()
        folder = title.replace(' ', "_")
        return folder

    def _write_to_s3(self, filename, folder, bucket):
        loc = os.path.join(folder, filename)
        file_object = bucket.new_key(loc)
        file_object.set_contents_from_filename(filename, policy='public-read')

    def _trim_names(self):
        df = pd.read_csv("../data/Podcast_additional_info.csv")
        tweets = get_twitter_followers()
        tweets.get_overlapping_users()
        df_followers = tweets.trim_users()
        titles = df_followers.index
        has_followers = df.Title.isin(titles)
        self.df = df.loc[has_followers, :]

    def send_to_S3(self):
        self._trim_names()
        for i, rl in enumerate(self.df.NormalizedUrl):
            url = 'https://' + rl
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content)
                list_rss = soup.findAll('media:content')
                self.connect_bucket('podcastrecommenderbucket')
                folder = self._folder_name(self.df.Title[i])
 
                if len(list_rss) > 5:
                    list_rss = list_rss[0:5]
               
                for rss in list_rss:
                    mp3 = rss.get('url')
                    cmd = 'wget ' + mp3
                    os.system(cmd)
                    filename = os.path.basename(mp3)
                    if os.path.exists(filename):
                        self._write_to_s3(filename, folder, self.bucket)
                    else:
                        continue
                cmd_rm = 'rm ' + ' '.join(list_rss)
                os.system(cmd_rm)
            except:
                self.broken_links.append(self.df.Title[i])
