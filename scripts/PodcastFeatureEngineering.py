
import pandas as pd
from clean_podcast_csv import PodcastCleaner
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import NMF

class Podcast_Features(PodcastCleaner):
    
    def __init__(self, text_vec_model=None):
        self.df = 'blah'
        self.text_vec = text_vec_model
        
    def get_NMF_topics(self):
        
    def _print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()
    
    def __text_model_create(self):
        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS.union(['www', 'podcast', 'talkshoe', 'href'])
        self.text_vec = TfidfVectorizer(max_df=0.95, 
                                   ngram_range=(1, 3),
                                   min_df=3,
                                   stop_words=my_stop_words,
                                   )
    def call_nmf(self, text):
        nmf = NMF(n_components=20, random_state=1, alpha=.1, l1_ratio=.5).fit(text)
        print("\nTopics in NMF model:")
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        print_top_words(nmf, tfidf_feature_names, 20)