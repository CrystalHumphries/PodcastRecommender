"""
Created on Sun Apr 17 16:27:58 2016

@author: Crystal Humphries
"""

import pandas as pd
import nltk
english_vocab = set(w.lower() for w in nltk.corpus.words.words())


class PodcastCleaner(object):

    def __init__(self):
        self.df = pd.read_csv("../data/Podcast_additional_info.csv")
        self.cleaned_df = None

    def _remove_empty_strings_int(self):
        ''' removes empty strings,
            converts columns to
            ints/floats, and replaces missing vaules with -1'''
 
        self.df['AverageRating'] = self.df.AverageRating.fillna(-1.0)

        self.df['AverageRating'] = self.df['AverageRating']\
                                       .apply(lambda x: -1.0
                                              if x == '<null>' else x)\
                                       .astype(float)

        self.df['RatingCount'] = self.df['RatingCount']\
                                     .apply(lambda x:
                                            self._neg_one(x))\
                                     .astype(int)
                           
        self.df['CategoryRanking'] = self.df['CategoryRanking']\
                                         .apply(lambda x:
                                                self._neg_one(x))\
                                         .astype(int)

    def _neg_one(self, x):
        if x == '<null>':
            return -1
        else:
            return x

    def _format_dates(self):
        '''changes Date to datetime'''
   
        self.df['DateFirstEpisode'] = self.df.DateFirstEpisode\
                                          .apply(lambda x:
                                                 pd.to_datetime(str(x),
                                                                coerce=True))
        self.df['DateLastEpisode'] = self.df.DateLastEpisode\
                                         .apply(lambda x:
                                                pd.to_datetime(str(x),
                                                               coerce=True))

    def _remove_null(self):
        ''' replaces empty strings with <null>'''
     
        cols = ['iTunesSubtitle', 'iTunesSummary', 'iTunesKeywords',
                'iTunesAuthor', 'iTunesOwnerName', 'iTunesOwnerEmail',
                'Link', 'ImageUrl']
        for col in cols:
            self.df[col] = self.df[col].fillna("<null>")

    def get_clean_df(self, english=False):
        if english is True:
            pass
        self._remove_empty_strings_int()
        self._format_dates()
        self._remove_null()
        self.cleaned_df = self.df
        return self.cleaned_df

    def get_english_words(self, percentage=None):
       '''Returns vector of boolean vector of those rows that have 
            >=percentage of english words
    
       Parameters
        ----------
            input : float {"percentage"} text{'column name'}'''
      
        self.percentage = 0.9
        if percentage is not None:
            self.percentage = percentage
    
        if not self.cleaned_df:
            self.get_clean_df()

        return self.cleaned_df.apply(lambda x: True
                                     if self._find_percentage(x) >=
                                     self.percentage else False)
 
    def _find_percentage(self, x):
        '''Returns percentage of words that are english
        
        Parameters
        ----------
            input : string'''
        ls = list(x)
        return sum([1 if x in english_vocab else 0 for x in ls])/float(len(ls))
