# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:27:58 2016

@author: Crystal.Humphries

'''grab list of podcasts that have twitter followwers'''
"""

from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix

CV = CountVectorizer()


class get_twitter_followers(object):

    def __init__(self):
        self.Podcast_twitter = self.intiate_mongo_client()
        self.Podcasts = self.Podcast_twitter.count()
        self.PodcastWithTw = None
        self.totalTwitters = None
        self.sparseMatrix = None
        self.list_of_followers = None
          
    def intiate_mongo_client(self):
        client = MongoClient()
        db = client['Podcast']
        return db['PodcastTwitter_handles']
        
    def create_sparse_matrix(self, list_of_followers):
        self.strings = []
        self.titles = []
        for ls in list_of_followers:
            x = ' '.join([str(x) for x in ls['TwitterFollowers']])
            self.strings.append(x)
            self.titles.append(ls['Title'])
        return list_of_strings, list_of_titles

    def list_followers(self):
        self.list_of_followers = []
        n = 0
        for pod in self.Podcast_twitter.find({}, {'Title': 1,
                                                  '_id': 0,
                                                  'TwitterFollowers': 1}):
            try:
                if 'TwitterFollowers' in pod and pod['TwitterFollowers']:
                    if pod['TwitterFollowers'][0] != 'None':
                        practice.append(pod)
                        n += 1
            except:
                pass
        self.PodcastWithTw = n

    def get_overlapping_users(self, Num=10):
        if self.list_of_followers is None:
            self.list_followers()
        strings,titles = self.create_sparse_matrix(self.list_of_followers)
        self.titles = titles
        final = CV.fit_transform(strings)
        rowsum_m = csr_matrix.sum(final, axis=0)
        self.totalTwitters = final.shape[1]
        rowsum_a = np.array(rowsum_m).reshape(rowsum_m.shape[1],)
        mask = rowsum_a >= Num
        u = np.where(mask)[0]
        sparse_mat = final.tocsc()[:, u]
        self.sparseMatrix = sparse_mat
        
    def trim_users(self, max_num=10000):
        if self.sparseMatrix is not None:
            mat = self.sparseMatrix.toarray()
            max_num = mat.shape[1]
            df = self._get_truncated_matrix(mat, max_num)
            return df
        else:
            print "SparseMatrix has not been generated"
            return
          
    def _get_truncated_matrix(self, mat, max_num):
        if mat.shape[1] > max_num:
            max_num = mat.shape[1]
        df = pd.DataFrame(mat[:, 0:max_num])
        df.index = titles
        a = df.sum(axis=1)
        mask2 = a > 0
        return df.loc[mask2, :]
