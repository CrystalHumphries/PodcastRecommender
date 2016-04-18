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

'''Obtain list of rss websites'''
df = pd.read_csv("../data/Podcast_additional_info.csv")


def connect_bucket(bucket_name):
    '''uses api key to connect to bucket name'''
    home = os.environ['HOME']
    awi_loc = os.path.join(home, '.api/AWS.api')
    awi = json.load(open(awi_loc))

    access_key = str(awi['AWS_ACCESS_KEY'])
    secret_access_key = str(awi['AWS_SECRET_ACCESS_KEY'])

    conn = boto.connect_s3(access_key, secret_access_key)
    return conn.get_bucket(bucket_name, validate=False)


def folder_name(title):
    if re.search('|', title):
        title = title.split('|')[0].strip()
    folder = title.replace(' ', "_")
    return folder


def write_to_s3(filename, folder, bucket):
    loc = os.path.join(folder, filename)
    file_object = bucket.new_key(loc)
    file_object.set_contents_from_filename(filename, policy='public-read')

if __name__ == "__main__":
    broken_links = []
    for i, rl in enumerate(df.NormalizedUrl):
        url = 'https://' + rl
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content)
            list_rss = soup.findAll('media:content')
            bucket = connect_bucket('podcastrecommenderbucket')
            folder = folder_name(df.Title[i])
            for rss in list_rss:
                mp3 = rss.get('url')
                cmd = 'wget ' + mp3
                os.system(cmd)
                filename = os.path.basename(mp3)
                if os.path.exists(filename):
                    write_to_s3(filename, folder, bucket)
                else:
                    continue
            cmd_rm = 'rm ' + ' '.join(list_rss)
        except:
            broken_links.append(df.Title[i])
