# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:11:57 2016

@author: Crystal Humphries

Returns a list of activated Twitter APIs

"""
import tweepy
from tweepy import OAuthHandler
import json
import os

APIs = ['Twitter2_API.json',  'Twitter3_API.json', 'Twitter4_API.json',
        'Twitter_API.json',  'Twitter_API4.json', 'Twitter_API5.json',
        'Twitter_API6.json', 'Twitter_API7.json', 'Twitter_API8.json',
        'Twitter_API9.json', 'Twitter_API10.json', 'Twitter_API11.json',
        'Twitter_API12.json', 'Twitter_API13.json', 'Twitter_API14.json',
        'Twitter_API15.json', 'Twitter_API16.json', 'Twitter_API17.json',
        'Twitter_API18.json', 'Twitter_API19.json']

home = os.environ["HOME"]
loc = os.path.join(home, ".api/")


class get_twitter_APIs(object):
    """Returns a list of activated Twitter APIs given a json file of each key.

    Parameters
    ----------
    name : string
           names of JSON file(s) containing the following
           components for activating a Twitter API:
                Access Token
                Access Token Secret
                API Key
                API Secret

    Returns
    -------
    list: activated API for each key given

    Examples
    --------
    >>> twitter_api = get_twitter_APIs(api_list = ['Twitter_API.json'])
    >>> twitter_api.activate_APIs()
    [<tweepy.api.API at 0x104f2cf50>]
    """

    def __init__(self, api_list=None):
        if api_list is None:
            self.twitter_api_list = APIs
        else:
            self.twitter_api_list = api_list
        self.api_list = []

    def create_api(self, file_name):
        '''reads the json file and returns the tokens and keys
            for API activation'''
        twitter_api = json.load(open(file_name))
        access_token = twitter_api['Access Token']
        access_token_secret = twitter_api['Access Token Secret']
        consumer_key = twitter_api['API Key']
        consumer_secret = twitter_api['API Secret']
        return access_token, access_token_secret, consumer_key, consumer_secret

    def activate_APIs(self):
        '''uses keys and token to activate the API'''
        for api in self.twitter_api_list:
            file_name = loc + api
            AT, ATS, CK, CKS = self.create_api(file_name)
            auth = OAuthHandler(CK, CKS)
            auth.set_access_token(AT, ATS)
            api = tweepy.API(auth)
            self.api_list.append(api)
        return self.api_list
