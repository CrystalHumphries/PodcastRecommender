
import pandas as pd
from clean_podcast_csv import PodcastCleaner
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import NMF
import numpy as np


class Podcast_Features(PodcastCleaner):

    def __init__(self, cleaned_df=None, text_vec_model=None):
        PodcastCleaner.__init__(self)
        if cleaned_df is None:
            self.df = self.get_clean_df()
        else:
            self.df = cleaned_df

        if text_vec_model is None:
            self._text_model_create()
            print("Creating Tf-idf")
        else:
            self.vec_model = text_vec_model

    def get_NMF_topics(self, model, text):
        tfidf_feature_names = self.vec_model.get_feature_names()
        topics = self.get_corresponding_topics(self.nmf, 
                                               tfidf_feature_names, 20)

        X = model.transform(text)
        ls = []
        for i, row in enumerate(X):
            n = np.argsort(row)[::-1][0]
            array = topics.values[n]
            ls.append(array)

        print("\nTopics in NMF model:")
        self.print_top_words(self.nmf, tfidf_feature_names, 20)
        return pd.DataFrame(pd.Series(ls))

    def print_top_words(self, model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i]
                  for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()

    def _text_model_create(self):
        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS.union(['www', 'podcast',
                                                       'talkshoe', 'href'])
        self.vec_model = TfidfVectorizer(max_df=0.95,
                                         ngram_range=(1, 3), min_df=3,
                                         stop_words=my_stop_words)

    def call_nmf(self, text):
        self.nmf = NMF(n_components=20, random_state=1, alpha=.1,
                       l1_ratio=.5).fit(text)

    def vectorize_text(self, col):
        if self.vec_model is None:
            self._text_model_create()
            print("hello")
        text = self.vec_model.fit_transform(self.df[col].values)
        self.vectorized_text = text
        return text

    def get_corresponding_topics(self, model, feature_names, n_top_words):
        ls = []
        for topic_idx, topic in enumerate(model.components_):
            features = ' '.join([feature_names[i] for i in
                                 topic.argsort()[:- n_top_words - 1:-1]])
            ls.append(features)
        return pd.DataFrame(pd.Series(ls))
